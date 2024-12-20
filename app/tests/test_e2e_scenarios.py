from datetime import datetime


def test_user_basic_flow(client):
    time_checkpoint = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

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

    response = client.post(
        "/locations",
        headers={"Authorization": f"Bearer {token}"},
        json={"run_id": run_id, "lat": 60.6, "lon": 100.6},
    )
    assert response.status_code == 201

    response = client.post(
        "/locations",
        headers={"Authorization": f"Bearer {token}"},
        json={"run_id": run_id, "lat": 60.7, "lon": 100.7},
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

    # get runs
    response = client.get(
        f'/runs?query=created_at < "{time_checkpoint}"',
        headers={"Authorization": f"Bearer {token}"},
        json={"id": run_id, "status": "ENDED"},
    )
    assert response.status_code == 200
