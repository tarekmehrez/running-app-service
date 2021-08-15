def test_add_location_200(client, create_user, create_token, create_run):
    user_id = create_user()
    token = create_token(user_id=user_id)
    run_id = create_run(user_id)

    url = "/locations"
    response = client.post(
        url,
        headers={"Authorization": f"Bearer {token}"},
        json={"run_id": run_id, "lat": 60.5, "lon": 100.5},
    )
    assert response.status_code == 201


def test_add_location_400_run_halted(client, create_user, create_token, create_run):
    user_id = create_user()
    token = create_token(user_id=user_id)
    run_id = create_run(user_id)

    # pause run
    response = client.patch(
        "/runs",
        headers={"Authorization": f"Bearer {token}"},
        json={"id": run_id, "status": "PAUSED"},
    )

    url = "/locations"
    response = client.post(
        url,
        headers={"Authorization": f"Bearer {token}"},
        json={"run_id": run_id, "lat": 60.5, "lon": 100.5},
    )
    assert response.status_code == 400


def test_add_location_200_two_locations(client, create_user, create_token, create_run):
    user_id = create_user()
    token = create_token(user_id=user_id)
    run_id = create_run(user_id)

    url = "/locations"
    response = client.post(
        url,
        headers={"Authorization": f"Bearer {token}"},
        json={"run_id": run_id, "lat": 60.5, "lon": 100.5},
    )
    assert response.status_code == 201

    response = client.post(
        url,
        headers={"Authorization": f"Bearer {token}"},
        json={"run_id": run_id, "lat": 60.5, "lon": 100.5},
    )
    assert response.status_code == 201


def test_add_location_422_invalid_lat(client, create_user, create_token, create_run):
    user_id = create_user()
    token = create_token(user_id=user_id)
    run_id = create_run(user_id)

    url = "/locations"
    response = client.post(
        url,
        headers={"Authorization": f"Bearer {token}"},
        json={"run_id": run_id, "lat": 500.5, "lon": 500.5},
    )
    assert response.status_code == 422


def test_add_location_404(client, create_user, create_token):
    user_id = create_user()
    token = create_token(user_id=user_id)

    url = "/locations"
    response = client.post(
        url,
        headers={"Authorization": f"Bearer {token}"},
        json={"run_id": "12345", "lat": 60.5, "lon": 100.5},
    )
    assert response.status_code == 404


def test_add_location_403(client, create_user, create_token, create_run):
    user_id_1 = create_user(email="user1@test.com")
    user_id_2 = create_user(email="user2@test.com")
    token_2 = create_token(user_id=user_id_2)
    run_id = create_run(user_id_1)

    url = "/locations"
    response = client.post(
        url,
        headers={"Authorization": f"Bearer {token_2}"},
        json={"run_id": run_id, "lat": 60.5, "lon": 100.5},
    )
    assert response.status_code == 403


def test_get_run_locations_200(client, create_user, create_token, create_run):
    user_id = create_user()
    token = create_token(user_id=user_id)
    run_id = create_run(user_id)

    url = f"/locations?run_id={run_id}"
    response = client.get(
        url,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200


def test_get_run_locations_404(client, create_user, create_token):
    user_id = create_user()
    token = create_token(user_id=user_id)

    url = f"/locations?run_id=1234"
    response = client.get(
        url,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404


def test_get_run_locations_403(client, create_user, create_token, create_run):
    user_id_1 = create_user(email="user1@test.com")
    user_id_2 = create_user(email="user2@test.com")
    token_2 = create_token(user_id=user_id_2)
    run_id = create_run(user_id_1)

    url = f"/locations?run_id={run_id}"
    response = client.get(
        url,
        headers={"Authorization": f"Bearer {token_2}"},
    )
    assert response.status_code == 403