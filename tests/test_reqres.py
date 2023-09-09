import json
import allure

from datetime import datetime

from constants import timestamp_threshold, reqres_url
from helpers import return_full_path, send_request_api, validate_json_against_schema

service = reqres_url


def test_users_per_page():
    per_page = 6

    response = send_request_api(
        service,
        "get",
        url=f"/users",
        params={"per_page": per_page}
    )
    with allure.step(f"verify status code"):
        assert response.status_code == 200

    with allure.step(f"verify per_page value is {per_page}"):
        assert response.json()['per_page'] == per_page

    with allure.step(f"verify item amount in data node is {per_page}"):
        assert len(response.json()['data']) == per_page


def test_users_schema():
    response = send_request_api(
        service,
        "get",
        f"/users")

    validate_json_against_schema('get_users.json', None, response.json())


def test_create_user():
    response = send_request_api(
        service,
        "post",
        url=f"/users",
        json={
            "name": "morpheus",
            "job": "leader"
        }
    )
    with allure.step(f"verify status code"):
        assert response.status_code == 201

    with allure.step(f"verify name"):
        assert response.json()['name'] == "morpheus"

    with allure.step(f"verify job"):
        assert response.json()['job'] == "leader"


# Verify that duplicate user can be created + verify user schema
# timestamp verification is rough due to not precise server time
def test_create_user_schema_timestamp():
    timestamp_before = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")

    response = send_request_api(
        service,
        "post",
        url="/users",
        json={
            "name": "morpheus",
            "job": "leader"
        }
    )
    validate_json_against_schema('create_user.json', None, response.json())

    timestamp_before = datetime.strptime(timestamp_before, "%Y-%m-%dT%H:%M:%S.%f")
    timestamp_response = datetime.strptime(response.json()['createdAt'][:-1], "%Y-%m-%dT%H:%M:%S.%f")

    with allure.step(f"verify timestamp"):
        assert abs((timestamp_response - timestamp_before).total_seconds()) < timestamp_threshold


def test_get_single_user():
    user_id_to_test = 2
    response = send_request_api(
        service,
        "get",
        url=f"/users/{user_id_to_test}",
    )

    with open(return_full_path('user_id_2.json', "data/files/jsons_reqres")) as file:
        sample_json = json.loads(file.read())
    with allure.step(f"verify response json"):
        assert response.json() == sample_json


def test_delete_user(create_test_user):
    user_id = create_test_user
    response = send_request_api(
        service,
        "delete",
        url=f"/users/{user_id}",
    )
    with allure.step(f"verify response status code"):
        assert response.status_code == 204
    with allure.step(f"verify response text is empty"):
        assert response.text == ""


def test_delete_user_invalid_id():
    user_id = "999999999999"
    response = send_request_api(
        service,
        "delete",
        url=f"/users/{user_id}",
    )
    with allure.step(f"verify status code"):
        assert response.status_code == 204
    assert response.text == ""


def test_delete_user_invalid_id_spec_symbols():
    user_id = "~!$#$#&#$@&%()(*&:{}?><"
    response = send_request_api(
        service,
        "delete",
        url=f"/users/{user_id}",
    )
    with allure.step(f"verify status code"):
        assert response.status_code == 204
    assert response.text == ""


# update user and verify it's been updated
def test_update_user_schema(create_test_user):
    user_id = create_test_user
    response = send_request_api(
        service,
        "put",
        url=f"/users/{user_id}",
        json={
            "name": "morpheus",
            "job": "zion resident"
        }
    )

    validate_json_against_schema('update_user.json', None, response.json())
    with allure.step(f"verify status code"):
        assert response.status_code == 200

def test_update_user_empty_json(create_test_user):
    user_id = create_test_user
    response = send_request_api(
        service,
        "put",
        url=f"/users/{user_id}",
        json={
        }
    )
    with allure.step(f"verify status code"):
        assert response.status_code == 200


def test_update_user_patch_schema(create_test_user):
    user_id = create_test_user
    response = send_request_api(
        service,
        "patch",
        url=f"/users/{user_id}",
        json={
            "name": "morpheus",
            "job": "zion resident"
        }
    )
    validate_json_against_schema('update_user.json', None, response.json())
    with allure.step(f"verify status code"):
        assert response.status_code == 200


def test_update_user_patch_empty_json_(create_test_user):
    user_id = create_test_user
    response = send_request_api(
        service,
        "patch",
        url=f"/users/{user_id}",
        json={
        }
    )

    with allure.step(f"verify status code"):
        assert response.status_code == 200
