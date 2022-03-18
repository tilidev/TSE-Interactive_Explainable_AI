# To run these tests, cd to the API folder, run the main app
# and once the API has finished startup, run pytest in another terminal session
import requests
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY, HTTP_404_NOT_FOUND, HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST

# Helper methods

api_path = "http://localhost:8000/"

def route(path: str):
    """Will return the appended root path with the input string"""
    return api_path + path

def r_get(path: str):
    """Will return the requests response object.
    
    :param: path: The request's path relative to the server root."""
    return requests.get(route(path))

def r_post(path: str, json):
    """Will return the requests response object for a post request.
    
    :param: path: The request's path relative to the server root.
    :param: json: The data (request body) that should be passed to the post request"""
    return requests.post(route(path), json=json)

# Test methods

def test_get_instance_by_id():
    res = r_get("instance/0").json()
    assert res["id"] == 0
    assert len(res.keys()) == 21
    res = r_get("instance/-12")
    assert res.status_code == HTTP_404_NOT_FOUND
    res = r_get("instance/1000")
    assert res.status_code == HTTP_404_NOT_FOUND
    res = r_get("instance/124asghla") # gibberish query
    assert res.status_code == HTTP_422_UNPROCESSABLE_ENTITY

def test_table_bad_request():
    request_data = {
        "filter" : [
            {"attribute" : "balance", "lower_bound" : 2000, "upper_bound" : 5000} # should be categorical
        ],
        "attributes" : ["amount"],
        "limit" : 10,
        "offset" : 0
    }

    res = r_post("table", request_data)
    assert res.status_code == HTTP_400_BAD_REQUEST