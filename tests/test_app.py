from .conftest import client


def test_post():
    r = client.post("api/send", json={"message": "hello"})
    assert r.status_code == 200
    assert r.json()["message"] == "Hello I am NiftyBridge AI assistant. How could I help you?"
