import pytest

from constants import reqres_url

service = reqres_url

@pytest.fixture(scope='function', autouse=False)
def create_test_user():
    from helpers import send_request_api
    response = send_request_api(
        service,
        "post",
        url="/users",
        json={
            "name": "morpheus",
            "job": "leader"
        }
    )
    user_id = response.json()['id']

    return user_id
