import json


def test_get_weather_forecast_200(client, create_user, create_token, mock_weather_api):
    user_id = create_user()
    token = create_token(user_id=user_id)

    with open("app/tests/mocks/get_weather_forecast.json") as f:
        mocked_response = json.load(f)
    mock_weather_api(response=mocked_response)

    url = "/weather?lat=30.044420&lon=31.235712"
    response = client.get(url, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200


def test_get_weather_forecast_400(client, create_user, create_token):
    user_id = create_user()
    token = create_token(user_id=user_id)

    url = "/weather?lat=5000000&lon=500000"
    response = client.get(url, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 400


def test_get_weather_forecast_403(client):  
    url = "/weather?lat=30.044420&lon=31.235712"
    response = client.get(url)
    assert response.status_code == 403
