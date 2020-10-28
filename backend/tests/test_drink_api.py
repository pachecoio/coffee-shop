import json

def test_get_drinks(app, client):
    res = client.get('/drinks')
    assert res.status_code == 200