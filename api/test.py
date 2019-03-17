import api


def user_by_id(id: int):
    """
    :rtype: api.Response
    """
    url = api.build_endpoint("user/{id}".format(id=id))
    return api.Sender.get(url)


def users_by_gender(gender: str):
    """
    :rtype: api.Response
    """
    url = api.build_endpoint("users")
    return api.Sender.get(url, params=dict(gender=gender))
