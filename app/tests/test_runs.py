from datetime import datetime

from app.middlewares.auth import VerifyUserToken


def test_create_run_201(client, create_user, create_token):
    user_id = create_user()
    token = create_token(user_id=user_id)

    url = "/runs"
    response = client.post(url, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201


def test_create_run_403(client):
    url = "/runs"
    token = "1234"
    response = client.post(url, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403


def test_create_run_while_another_is_running(client, create_user, create_token):
    user_id = create_user()
    token = create_token(user_id=user_id)

    url = "/runs"
    response = client.post(url, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201

    response = client.post(url, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 400


def test_get_user_runs_200(client, create_user, create_token):
    user_id = create_user()
    token = create_token(user_id=user_id)

    url = "/runs"
    response = client.post(url, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201

    response = client.get(url, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert len(response.json()["runs"]) == 1


def test_get_user_runs_403_invalid_token(client):
    url = "/runs"
    token = "1234"
    response = client.get(url, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403


def test_patch_user_run_200(client, create_user, create_token):
    user_id = create_user()
    token = create_token(user_id=user_id)

    url = "/runs"
    response = client.post(url, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    response_json = response.json()
    response_json["description"] = "best run ever"
    response = client.patch(
        url,
        headers={"Authorization": f"Bearer {token}"},
        json=response_json,
    )
    assert response.status_code == 200


def test_patch_user_run_200_end_update_weather(
    client, create_user, create_token, create_run, add_run_locations
):
    user_id = create_user()
    token = create_token(user_id=user_id)
    run_id = create_run(user_id)
    add_run_locations(run_id, user_id)

    url = "/runs"
    response = client.patch(
        url,
        headers={"Authorization": f"Bearer {token}"},
        json={"id": run_id, "status": "ENDED"},
    )
    assert response.status_code == 200
    assert "weather" in response.json()


def test_patch_user_run_403_other_user_run(client, create_user, create_token):
    user_id_1 = create_user(email="user1@test.com")
    token_1 = create_token(user_id=user_id_1)

    user_id_2 = create_user(email="user2@test.com")
    token_2 = create_token(user_id=user_id_2)

    url = "/runs"
    response = client.post(url, headers={"Authorization": f"Bearer {token_1}"})
    assert response.status_code == 201
    response_json = response.json()
    response_json["description"] = "best run ever"

    response = client.patch(
        url,
        headers={"Authorization": f"Bearer {token_2}"},
        json=response_json,
    )
    assert response.status_code == 403


def test_runs_reports_200(
    client, create_user, create_token, create_run, add_run_locations
):
    user_id = create_user()
    token = create_token(user_id=user_id)

    # create and end run 1
    run_id_1 = create_run(user_id)
    add_run_locations(run_id_1, user_id)

    response = client.patch(
        "/runs",
        headers={"Authorization": f"Bearer {token}"},
        json={"id": run_id_1, "status": "ENDED"},
    )
    assert response.status_code == 200

    # create and end run 2
    run_id_2 = create_run(user_id)
    add_run_locations(run_id_2, user_id)

    response = client.patch(
        "/runs",
        headers={"Authorization": f"Bearer {token}"},
        json={"id": run_id_2, "status": "ENDED"},
    )
    assert response.status_code == 200

    # get their summaries
    url = "/runs"
    response = client.get(url, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    response_json = response.json()

    assert "runs" in response_json
    assert len(response_json["runs"]) == 2
    assert response_json["runs"][0]["distance"] > 0.0
    assert response_json["runs"][0]["speed"] > 0.0
    assert "summary" in response_json
    assert response_json["summary"]["distance"]["mean"] > 0.0
    assert response_json["summary"]["distance"]["min"] > 0.0
    assert response_json["summary"]["distance"]["max"] > 0.0
    assert response_json["summary"]["speed"]["mean"] > 0.0
    assert response_json["summary"]["speed"]["min"] > 0.0
    assert response_json["summary"]["speed"]["max"] > 0.0


def test_runs_reports_200_with_query(
    client, create_user, create_token, create_run, add_run_locations
):
    user_id = create_user()
    token = create_token(user_id=user_id)

    # create and end run 1
    run_id_1 = create_run(user_id)
    add_run_locations(run_id_1, user_id)

    response = client.patch(
        "/runs",
        headers={"Authorization": f"Bearer {token}"},
        json={"id": run_id_1, "status": "ENDED"},
    )
    assert response.status_code == 200

    time_checkpoint = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

    # create and end run 2
    run_id_2 = create_run(user_id)
    add_run_locations(run_id_2, user_id)

    response = client.patch(
        "/runs",
        headers={"Authorization": f"Bearer {token}"},
        json={"id": run_id_2, "status": "ENDED"},
    )
    assert response.status_code == 200

    # query to return only the first
    url = f'/runs?query=created_at < "{time_checkpoint}"'
    response = client.get(url, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    response_json = response.json()

    assert "runs" in response_json
    assert "summary" in response_json
    assert len(response_json["runs"]) == 1

    # query to return both runs
    url = f'/runs?query=created_at < "{time_checkpoint}" or distance > 0.0'
    response = client.get(url, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    response_json = response.json()

    assert "runs" in response_json
    assert "summary" in response_json
    assert len(response_json["runs"]) == 2


def test_runs_reports_400_with_query(
    client, create_user, create_token, create_run, add_run_locations
):
    user_id = create_user()
    token = create_token(user_id=user_id)

    # create and end run 1
    run_id_1 = create_run(user_id)
    add_run_locations(run_id_1, user_id)

    response = client.patch(
        "/runs",
        headers={"Authorization": f"Bearer {token}"},
        json={"id": run_id_1, "status": "ENDED"},
    )
    assert response.status_code == 200

    time_checkpoint = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

    url = f'/runs?query=some_random_field < "{time_checkpoint}"'
    response = client.get(url, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 400

    url = f'/runs?query=created_at < "definitely not a timestamp"'
    response = client.get(url, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 400
