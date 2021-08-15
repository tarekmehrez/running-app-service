from app.models.validators.users import UserType


def test_admin_list_users_200(
    client, seed_users_agents_admins, create_user, create_token
):
    seed_users_agents_admins()
    user_id = create_user(user_type=UserType.ADMIN)
    token = create_token(user_id=user_id, user_type=UserType.ADMIN)

    url = "/admins/users"
    response = client.get(url, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert len(response.json()["results"]) == 1


def test_admin_list_users_200_pagination(
    client, seed_users_agents_admins, create_user, create_token
):
    seed_users_agents_admins(count=10)
    user_id = create_user(user_type=UserType.ADMIN)
    token = create_token(user_id=user_id, user_type=UserType.ADMIN)

    url = "/admins/users?page=1&page_count=5"
    response = client.get(url, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert len(response.json()["results"]) == 5

    url = "/admins/users?page=2&page_count=5"
    response = client.get(url, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert len(response.json()["results"]) == 5


def test_admin_list_users_403_normal_user(client, create_user, create_token):
    user_id = create_user(user_type=UserType.USER)
    token = create_token(user_id=user_id, user_type=UserType.USER)

    url = "/admins/users"
    response = client.get(url, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 403


def test_admin_list_users_403_agent(client, create_user, create_token):
    user_id = create_user(user_type=UserType.AGENT)
    token = create_token(user_id=user_id, user_type=UserType.AGENT)

    url = "/admins/users"
    response = client.get(url, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 403


def test_admin_list_agents_200(
    client, seed_users_agents_admins, create_user, create_token
):
    seed_users_agents_admins()
    user_id = create_user(user_type=UserType.ADMIN)
    token = create_token(user_id=user_id, user_type=UserType.ADMIN)

    url = "/admins/agents"
    response = client.get(url, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert len(response.json()["results"]) == 1


def test_admin_list_agents_403_normal_user(client, create_user, create_token):
    user_id = create_user(user_type=UserType.USER)
    token = create_token(user_id=user_id, user_type=UserType.USER)

    url = "/admins/agents"
    response = client.get(url, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 403


def test_admin_list_agents_403_agent(client, create_user, create_token):
    user_id = create_user(user_type=UserType.AGENT)
    token = create_token(user_id=user_id, user_type=UserType.AGENT)

    url = "/admins/agents"
    response = client.get(url, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 403


def test_admin_list_admins_200(
    client, seed_users_agents_admins, create_user, create_token
):
    seed_users_agents_admins()
    user_id = create_user(user_type=UserType.ADMIN)
    token = create_token(user_id=user_id, user_type=UserType.ADMIN)

    url = "/admins/admins"
    response = client.get(url, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert len(response.json()["results"]) == 2


def test_admin_list_admins_403_normal_user(client, create_user, create_token):
    user_id = create_user(user_type=UserType.USER)
    token = create_token(user_id=user_id, user_type=UserType.USER)

    url = "/admins/admins"
    response = client.get(url, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 403


def test_admin_list_admins_403_agent(client, create_user, create_token):
    user_id = create_user(user_type=UserType.AGENT)
    token = create_token(user_id=user_id, user_type=UserType.AGENT)

    url = "/admins/admins"
    response = client.get(url, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 403


def test_admin_create_user_200(client, create_user, create_token):
    user_id = create_user(user_type=UserType.ADMIN)
    token = create_token(user_id=user_id, user_type=UserType.ADMIN)

    url = "/admins/users"
    response = client.post(
        url,
        headers={"Authorization": f"Bearer {token}"},
        json={"email": "email@email.com", "password": "password123456"},
    )
    assert response.status_code == 200


def test_admin_create_user_403_normal_user(client, create_user, create_token):
    user_id = create_user(user_type=UserType.USER)
    token = create_token(user_id=user_id, user_type=UserType.USER)

    url = "/admins/users"
    response = client.post(
        url,
        headers={"Authorization": f"Bearer {token}"},
        json={"email": "email@email.com", "password": "password123456"},
    )

    assert response.status_code == 403


def test_admin_create_user_403_agent(client, create_user, create_token):
    user_id = create_user(user_type=UserType.AGENT)
    token = create_token(user_id=user_id, user_type=UserType.AGENT)

    url = "/admins/users"
    response = client.post(
        url,
        headers={"Authorization": f"Bearer {token}"},
        json={"email": "email@email.com", "password": "password123456"},
    )

    assert response.status_code == 403


def test_admin_create_agent_200(client, create_user, create_token):
    user_id = create_user(user_type=UserType.ADMIN)
    token = create_token(user_id=user_id, user_type=UserType.ADMIN)

    url = "/admins/agents"
    response = client.post(
        url,
        headers={"Authorization": f"Bearer {token}"},
        json={"email": "email@email.com", "password": "password123456"},
    )
    assert response.status_code == 200


def test_admin_create_agent_403_normal_user(client, create_user, create_token):
    user_id = create_user(user_type=UserType.USER)
    token = create_token(user_id=user_id, user_type=UserType.USER)

    url = "/admins/agents"
    response = client.post(
        url,
        headers={"Authorization": f"Bearer {token}"},
        json={"email": "email@email.com", "password": "password123456"},
    )

    assert response.status_code == 403


def test_admin_create_agent_403_agent(client, create_user, create_token):
    user_id = create_user(user_type=UserType.AGENT)
    token = create_token(user_id=user_id, user_type=UserType.AGENT)

    url = "/admins/agents"
    response = client.post(
        url,
        headers={"Authorization": f"Bearer {token}"},
        json={"email": "email@email.com", "password": "password123456"},
    )

    assert response.status_code == 403


def test_admin_create_admin_200(client, create_user, create_token):
    user_id = create_user(user_type=UserType.ADMIN)
    token = create_token(user_id=user_id, user_type=UserType.ADMIN)

    url = "/admins/admins"
    response = client.post(
        url,
        headers={"Authorization": f"Bearer {token}"},
        json={"email": "email@email.com", "password": "password123456"},
    )
    assert response.status_code == 200


def test_admin_create_admin_403_normal_user(client, create_user, create_token):
    user_id = create_user(user_type=UserType.USER)
    token = create_token(user_id=user_id, user_type=UserType.USER)

    url = "/admins/admins"
    response = client.post(
        url,
        headers={"Authorization": f"Bearer {token}"},
        json={"email": "email@email.com", "password": "password123456"},
    )

    assert response.status_code == 403


def test_admin_create_admin_403_agent(client, create_user, create_token):
    user_id = create_user(user_type=UserType.AGENT)
    token = create_token(user_id=user_id, user_type=UserType.AGENT)

    url = "/admins/admins"
    response = client.post(
        url,
        headers={"Authorization": f"Bearer {token}"},
        json={"email": "email@email.com", "password": "password123456"},
    )

    assert response.status_code == 403
