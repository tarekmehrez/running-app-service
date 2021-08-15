def test_user_signup_422_missing_details(client):
    url = "/users/signup"
    response = client.post(url, json={})
    assert response.status_code == 422


def test_user_signup_422_incorrect_email(client):
    url = "/users/signup"
    response = client.post(url, json={"email": "test", "password": "TestPass123!"})
    assert response.status_code == 422


def test_user_signup_422_incorrect_password(client):
    url = "/users/signup"
    response = client.post(url, json={"email": "test@test.com", "password": "abc"})
    assert response.status_code == 422


def test_user_signup_201(client):
    url = "/users/signup"
    response = client.post(
        url, json={"email": "test@test.com", "password": "TestPass123!"}
    )
    assert response.status_code == 201


def test_user_login_404(client):
    url = "/users/login"
    response = client.post(
        url, json={"email": "test@test.com", "password": "TestPass123!"}
    )
    assert response.status_code == 404


def test_user_login_401(client):
    url = "/users/signup"
    response = client.post(
        url, json={"email": "test@test.com", "password": "TestPass123!"}
    )
    assert response.status_code == 201
    url = "/users/login"
    response = client.post(
        url, json={"email": "test@test.com", "password": "wrong password"}
    )
    assert response.status_code == 401


def test_user_login_200(client):
    url = "/users/signup"
    response = client.post(
        url, json={"email": "test@test.com", "password": "TestPass123!"}
    )
    assert response.status_code == 201
    url = "/users/login"
    response = client.post(
        url, json={"email": "test@test.com", "password": "TestPass123!"}
    )
    assert response.status_code == 200

