import allure

from constants import catfacts_url
from helpers import send_request_api, validate_json_against_schema

service = catfacts_url


def test_get_breeds():
    limit = 3

    response = send_request_api(
        service,
        "get",
        url=f"/breeds",
        params={"limit": {limit}}
    )
    with allure.step(f"verify status code"):
        assert response.status_code == 200

    with allure.step(f"verify breed number is {limit}"):
        assert len(response.json()["data"]) == limit


def test_get_breeds_schema():
    limit = 6

    response = send_request_api(
        service,
        "get",
        url=f"/breeds",
        params={"limit": {limit}}
    )
    validate_json_against_schema('get_breeds_schema.json', "data/files/json_schemas_catfacts", response.json())


def test_get_facts():
    limit = 7

    response = send_request_api(
        service,
        "get",
        url=f"/facts",
        params={"limit": {limit}}
    )
    with allure.step(f"verify status code"):
        assert response.status_code == 200

    with allure.step(f"verify facts amount is {limit}"):
        assert len(response.json()["data"]) == limit
