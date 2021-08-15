def test_user_basic_flow(client):

    # sign up
    response = client.post(
        "/users/signup", json={"email": "test@test.com", "password": "TestPass123!"}
    )
    assert response.status_code == 201

    # login and get token
    response = client.post(
        "/users/login", json={"email": "test@test.com", "password": "TestPass123!"}
    )
    assert response.status_code == 200
    token = response.json()["token"]

    # create run
    response = client.post("/runs", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    run_id = response.json()["id"]

    # create locations
    response = client.post(
        "/locations",
        headers={"Authorization": f"Bearer {token}"},
        json={"run_id": run_id, "lat": 60.5, "lon": 100.5},
    )
    assert response.status_code == 201

    # pause run
    response = client.patch(
        "/runs",
        headers={"Authorization": f"Bearer {token}"},
        json={"id": run_id, "status": "PAUSED"},
    )
    assert response.status_code == 200

    # end run
    response = client.patch(
        "/runs",
        headers={"Authorization": f"Bearer {token}"},
        json={"id": run_id, "status": "ENDED"},
    )
    assert response.status_code == 200

