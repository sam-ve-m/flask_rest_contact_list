from src.core.enums.status import ResponseStatus


def label_status(status: bool) -> dict:
    status_enum_schema = {
        False: ResponseStatus.ERROR,
        True: ResponseStatus.SUCCESS,
    }
    status_enum = status_enum_schema.get(status)
    return {"status": status_enum.value}
