import json
import os

import allure
from requests import sessions
from allure_commons.types import AttachmentType
from curlify import to_curl
from jsonschema.validators import validate


def send_request_api(service, method, url, **kwargs):
    new_url = service + url
    method = method.upper()
    with allure.step(f" {method} {service}{url} "):
        with sessions.Session() as session:
            response = session.request(method=method, url=new_url, **kwargs)
            message = to_curl(response.request)

            allure.attach(body=message.encode("utf8"), name="Curl", attachment_type=AttachmentType.TEXT,
                          extension='txt')

        if ("Content-Type" in response.headers and "text/html" in response.headers[
            "Content-Type"]) or not response.content:
            # if not response.json():
            allure.attach(body='empty response', name='Empty Response', attachment_type=AttachmentType.TEXT,
                          extension='txt')
        else:
            allure.attach(body=json.dumps(response.json(), indent=4).encode("utf8"), name="Response Json",
                          attachment_type=AttachmentType.JSON, extension='json')
    return response


def return_full_path(file_name, folder_name=None):
    parent_path = (os.path.dirname(__file__))
    if folder_name is None:
        folder_name = "data/files/json_schemas_reqres"
    if file_name is None:
        return os.path.abspath(os.path.join(parent_path, folder_name))
    else:
        return os.path.abspath(os.path.join(parent_path, folder_name, file_name))


def validate_json_against_schema(file_name_schema, folder_schema, response_json):
    with open(return_full_path(file_name_schema, folder_schema)) as file:
        schema = json.loads(file.read())
    with allure.step(f"validate json with schema from file {file_name_schema}"):
        validate(instance=response_json, schema=schema)
