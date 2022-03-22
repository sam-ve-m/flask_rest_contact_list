from pytest_steps import test_steps

from test.api import Api


@test_steps("register", "list_by_letter", "list_all", "update", "count", "delete", "find", "list_available", "count_available", "recover_contact", "empty_database")
def test_api():
    api = Api("http://localhost:4445")
    _insert_dummies(api)
    yield

    letters_ids = _get_ids_per_letter(api)
    yield

    registers_ids = _get_all_registers(api)
    yield

    _update_and_check_registers(api, registers_ids)
    yield

    _check_phones_count(api)
    yield

    _delete_contacts(api, letters_ids, 2)
    yield

    _check_find_details(api, letters_ids)
    yield

    _check_half_available_by_letter(api)
    yield

    _check_phones_count(api, 1/2)
    yield

    _recover_deleted_contact(api)
    yield

    _empty_database(api)
    yield


def _insert_dummies(api: Api):
    responses = [api.insert(i, "a", 3) for i in range(10)]
    responses += [api.insert(i, "b", 2) for i in range(10, 20)]
    responses += [api.insert(i, "c", 1) for i in range(20, 30)]
    for status in responses:
        assert status.get("status") == "1001"


def _get_ids_per_letter(api: Api) -> dict:
    letters_ids = {}
    for letter in ("a", "b", "c"):
        response = api.find_by_letter(letter)
        assert response.get("status") == "1001"
        registers = response.get("contactsList")
        assert len(registers) in [10, 5]
        registers_ids = []
        for contact in registers:
            _id = contact.get("contactId")
            phone_list = contact.get("phoneList")
            assert contact.get("lastName") in ["Dummy", "Altered Dummy"]
            assert contact.get("email") == "Dummy"
            assert contact.get("address") is None
            assert isinstance(phone_list, list)
            assert _id is not None
            registers_ids.append(_id)
            for phone in phone_list:
                assert phone.get("type") in ("residential", "mobile", "commercial")
                assert "1111-1111" in phone.get("number")
        letters_ids.update({letter: registers_ids})
    return letters_ids


def _get_all_registers(api: Api) -> list:
    response = api.find_all()
    assert response.get("status") == "1001"
    registers = response.get("contactsList")
    assert len(registers) == 30
    registers_ids = [contact.get("contactId") for contact in registers]
    for _id in registers_ids:
        assert _id is not None
    return registers_ids


def _update_and_check_registers(api: Api, registers_ids: list):
    for _id in registers_ids:
        response = api.update(_id)
        assert response.get("status") == "1001"
        response = api.update(_id)
        assert response.get("status") == "1004"
    response = api.find_all()
    assert response.get("status") == "1001"
    registers = response.get("contactsList")
    assert len(registers) == 30
    for contact in registers:
        assert contact.get("lastName") == "Altered Dummy"
        phone_list = contact.get("phoneList")
        assert contact.get("email") == "Dummy"
        assert contact.get("address") is None
        assert isinstance(phone_list, list)
        assert contact.get("contactId") is not None
        for phone in phone_list:
            assert phone.get("type") in ("residential", "mobile", "commercial")
            assert "1111-1111" in phone.get("number")


def _check_phones_count(api: Api, multiple: float = 1):
    response = api.find_phones()
    assert response.get("status") == ("1001" if multiple else "1004")
    contacts_amount = response.get("countContacts")
    phones_types = {phone.get("_id"): phone.get("Count") for phone in response.get("countType")}
    assert contacts_amount == 30*multiple
    assert phones_types == {
            "mobile": 20*multiple,
            "commercial": 10*multiple,
            "residential": 30 * multiple,
    }


def _delete_contacts(api: Api, letters_ids: dict, divider: int = 2):
    responses = []
    for id_list in letters_ids.values():
        responses += [api.delete(_id) for _id in id_list[:len(id_list)//divider]]
    for status in responses:
        assert status.get("status") == "1001"

    responses = []
    for id_list in letters_ids.values():
        responses += [api.delete(_id) for _id in id_list[:len(id_list)//divider]]
    for status in responses:
        assert status.get("status") == "1004"


def _check_find_details(api: Api, letters_ids: dict):
    successful_responses = []
    unavailable_responses = []
    for id_list in letters_ids.values():
        successful_responses += [api.find_one(_id) for _id in id_list[len(id_list)//2:]]
        unavailable_responses += [api.find_one(_id) for _id in id_list[:len(id_list) // 2]]
    for index in range(len(successful_responses)):
        assert unavailable_responses[index].get("status") == "1004"
        contact = successful_responses[index]
        assert contact.get("status") == "1001"
        _id = contact.get("contactId")
        phone_list = contact.get("phoneList")
        assert contact.get("lastName") == "Altered Dummy"
        assert contact.get("email") == "Dummy"
        assert contact.get("address") == "Dummy"
        assert isinstance(phone_list, list)
        assert _id is not None
        for phone in phone_list:
            assert phone.get("type") in ("residential", "mobile", "commercial")
            assert "1111-1111" in phone.get("number")


def _check_half_available_by_letter(api: Api):
    for letter in ("a", "b", "c"):
        response = api.find_by_letter(letter)
        assert response.get("status") == "1001"
        registers = response.get("contactsList")
        assert len(registers) == 5


def _recover_deleted_contact(api: Api):
    responses = [api.insert(i, "a", 2, "00") for i in range(5)]
    for status in responses:
        assert status.get("status") == "1001"
    response = api.find_by_letter("a")
    assert response.get("status") == "1001"
    registers = response.get("contactsList")
    assert len(registers) == 10
    for contact in registers[:5]:
        phone_list = contact.get("phoneList")
        assert len(phone_list) == 3
        assert phone_list[1].get("number") == "(00) 1111-1111"


def _empty_database(api: Api):
    letters_ids = _get_ids_per_letter(api)
    _delete_contacts(api, letters_ids, 1)
    _check_phones_count(api, 0)
