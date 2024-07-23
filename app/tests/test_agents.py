from app.models.validators.users import UserType


def test_agent_list_users_200(
    client, seed_users_agents_admins, create_user, create_token
):
    seed_users_agents_admins()
    user_id = create_user(user_type=UserType.AGENT)
    token = create_token(user_id=user_id, user_type=UserType.AGENT)

    url = "/agents/users"
    response = client.get(url, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert len(response.json()["results"]) == 1


def test_agent_list_users_403_normal_user(client, create_user, create_token):
    user_id = create_user(user_type=UserType.USER)
    token = create_token(user_id=user_id, user_type=UserType.USER)

    url = "/agents/users"
    response = client.get(url, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 403


def test_agent_create_user_200(client, create_user, create_token):
    user_id = create_user(user_type=UserType.AGENT)
    token = create_token(user_id=user_id, user_type=UserType.AGENT)

    url = "/agents/users"
    response = client.post(
        url,
        headers={"Authorization": f"Bearer {token}"},
        json={"email": "email@email.com", "password": "password123456"},
    )
    assert response.status_code == 200


def test_agent_create_user_403_normal_user(client, create_user, create_token):
    user_id = create_user(user_type=UserType.USER)
    token = create_token(user_id=user_id, user_type=UserType.USER)

    url = "/agents/users"
    response = client.post(
        url,
        headers={"Authorization": f"Bearer {token}"},
        json={"email": "email@email.com", "password": "password123456"},
    )
    assert response.status_code == 403
