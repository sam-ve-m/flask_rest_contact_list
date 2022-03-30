from typing import Any, Iterable

from pytest_steps import test_steps

from test.api import Api


@test_steps("clean_database", "register", "list_by_letter", "list_all", "update", "count", "delete", "find", "list_available", "count_available", "recover_contact", "empty_database")
def test_api():
    api = Api("http://localhost:4445")
    _clean_database(api)
    yield

    try:
        _insert_dummies(api)
        yield

        letters_ids = _get_ids_per_letter(api)
        yield

        registers_ids = _get_all_registers(api)
        yield

        _update_and_check_registers(api, registers_ids)
        yield

        _check_phones_count(api, percentage=100)
        yield

        _delete_contacts(api, letters_ids.values(), divider=2)
        yield

        _check_find_details(api, letters_ids)
        yield

        _check_half_available_by_letter(api)
        yield

        _check_phones_count(api, percentage=50)
        yield

        _recover_deleted_contact(api)
        yield

        _return_none_when_database_empty(api)
        yield
    except AssertionError as error:
        _clean_database(api)
        raise error


def _clean_database(api: Api):
    responses = api.find_all()
    registers = [contact.get('contactId') for contact in responses.get("contactsList")]
    _delete_contacts(api, [registers], 1)


def _check_status(response: dict, status: bool, message: str):
    assert response.get("status") == ("1001" if status else "1004"), f"Not expected status {message}"


def _check_field(response: dict, field: Any, value: Any, check_method=lambda x, y: x == y):
    response_value = response.get(field)
    assert check_method(response_value, value), f"Wrong value for field {field}"
    return response_value


def _check_list_amount(return_list: list, expected_amount: int):
    assert len(return_list) == expected_amount, (
            f"Returned {'more' if len(return_list) > expected_amount else 'less'} registers. "
            + "Maybe something with the soft delete active field happened"
    )


def _check_phone(phone: dict):
    _check_field(phone, "number", "1111-1111", lambda x, y: y in x)
    _check_field(phone, "type", ("residential", "mobile", "commercial"), lambda x, y: x in y)


def _check_contact(contact: dict, last_name_values: tuple = ("Dummy", "Altered Dummy"), address: str = None):
    _check_field(contact, "lastName", last_name_values, lambda x, y: x in y)
    _check_field(contact, "email", "Dummy")
    _check_field(contact, "address", address)
    _check_field(contact, "phoneList", list, lambda x, y: isinstance(x, y))
    _check_field(contact, "contactId", None, lambda x, y: x is not y)
    phone_list = contact.get("phoneList")
    for phone in phone_list:
        _check_phone(phone)


def _insert_dummies(api: Api):
    responses = [api.insert(i, "a", 3) for i in range(10)]
    responses += [api.insert(i, "b", 2) for i in range(10, 20)]
    responses += [api.insert(i, "c", 1) for i in range(20, 30)]
    for status in responses:
        _check_status(status, True, message="inserting")


def _get_ids_per_letter(api: Api, expected_amount: int = 10) -> dict:
    letters_ids = {}
    for letter in ("a", "b", "c"):
        response = api.find_by_letter(letter)
        _check_status(response, True, message="listing by letter")
        registers = response.get("contactsList")
        _check_list_amount(registers, expected_amount)
        registers_ids = []
        for contact in registers:
            _id = contact.get("contactId")
            _check_contact(contact)
            registers_ids.append(_id)
        letters_ids.update({letter: registers_ids})
    return letters_ids


def _find_all_registers(api: Api):
    response = api.find_all()
    _check_status(response, True, message="listing all")
    registers = response.get("contactsList")
    _check_list_amount(registers, 30)
    return registers


def _get_all_registers(api: Api) -> list:
    registers_ids = [
        _check_field(contact, "contactId", None, lambda x, y: x is not y)
        for contact in _find_all_registers(api)
    ]
    return registers_ids


def _update_and_check_registers(api: Api, registers_ids: list):
    for _id in registers_ids:
        response = api.update(_id)
        _check_status(response, True, message="updating")
        response = api.update(_id)
        _check_status(response, False, message="updating again in sequence")
    for contact in _find_all_registers(api):
        _check_contact(contact, ("Altered Dummy",))


def _check_phones_count(api: Api, percentage: int = 100):
    multiple = percentage/100
    response = api.find_phones()
    _check_status(response, bool(multiple), "counting phones")
    contacts_amount = response.get("countContacts")
    _check_list_amount(range(contacts_amount), int(30*multiple))
    phones_types = {phone.get("_id"): phone.get("Count") for phone in response.get("countType")}
    assert phones_types == {
            "mobile": 20*multiple,
            "commercial": 10*multiple,
            "residential": 30 * multiple,
    }


def _try_to_delete_expecting_status(api: Api, id_lists: Iterable, divider: int, status: bool, message: str):
    for id_list in id_lists:
        for _id in id_list[:len(id_list) // divider]:
            _check_status(api.delete(_id), status, message)


def _delete_contacts(api: Api, id_lists: Iterable, divider: int = 2):
    _try_to_delete_expecting_status(api, id_lists, divider, True, message="deleting")
    _try_to_delete_expecting_status(api, id_lists, divider, False, message="deleting again")


def _check_available_details(api: Api, id_list: list):
    for _id in id_list:
        contact = api.find_one(_id)
        _check_status(contact, True, message="getting contact")
        _check_contact(contact, ("Altered Dummy",), "Dummy")


def _check_unavailable_details(api: Api, id_list: list):
    for _id in id_list:
        _check_status(api.find_one(_id), False, message="getting unavailable contact")


def _check_find_details(api: Api, letters_ids: dict):
    for id_list in letters_ids.values():
        _check_available_details(api, id_list[len(id_list) // 2:])
        _check_unavailable_details(api, id_list[:len(id_list) // 2])


def _check_half_available_by_letter(api: Api):
    for letter in ("a", "b", "c"):
        response = api.find_by_letter(letter)
        _check_status(response, True, message="list by letter")
        _check_list_amount(response.get("contactsList"), 5)


def _recover_deleted_contact(api: Api):
    for i in range(5):
        _check_status(api.insert(i, "a", 2, "00"), True, message="recovering contact")
    response = api.find_by_letter("a")
    _check_status(response, True, message="list by letter")
    registers = response.get("contactsList")
    _check_list_amount(registers, 10)
    for contact in registers[:5]:
        phone_list = contact.get("phoneList")
        _check_list_amount(phone_list, 3)
        assert phone_list[1].get("number") == "(00) 1111-1111", "Not updated second phone in recover"


def _return_none_when_database_empty(api: Api):
    _clean_database(api)
    _check_phones_count(api, percentage=0)
