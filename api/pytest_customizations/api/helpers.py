def build_main_response(result: list or dict):
    return {
        "errorCode": 0,
        "errorMessage": None,
        "result": result,
        "success": True
    }


def get_expected_success_response(ids: list):
    return build_main_response(ids)


keys_for_user = ["id", "name", "gender", "age", "city", "registrationDate"]


def get_expected_success_response_for_user_by_id(data: list):
    result = dict()
    for key, value in zip(keys_for_user, data):
        result[key] = value
    return build_main_response(result)
