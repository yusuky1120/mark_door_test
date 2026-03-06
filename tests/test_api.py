from fastapi.testclient import TestClient

from app.main import create_app


def test_crud_flow(tmp_path):
    db_path = tmp_path / "test.db"
    app = create_app(f"sqlite:///{db_path}")
    client = TestClient(app)

    create_res = client.post("/api/tasks", json={"title": "task1", "description": "desc"})
    assert create_res.status_code == 201
    task_id = create_res.json()["id"]

    list_res = client.get("/api/tasks")
    assert list_res.status_code == 200
    assert len(list_res.json()) == 1

    update_res = client.put(f"/api/tasks/{task_id}", json={"completed": True, "title": "updated"})
    assert update_res.status_code == 200
    assert update_res.json()["completed"] is True
    assert update_res.json()["title"] == "updated"

    filtered = client.get("/api/tasks?completed=true")
    assert filtered.status_code == 200
    assert len(filtered.json()) == 1

    delete_res = client.delete(f"/api/tasks/{task_id}")
    assert delete_res.status_code == 204

    empty_res = client.get("/api/tasks")
    assert empty_res.status_code == 200
    assert empty_res.json() == []


def test_title_validation(tmp_path):
    db_path = tmp_path / "test2.db"
    app = create_app(f"sqlite:///{db_path}")
    client = TestClient(app)

    bad_res = client.post("/api/tasks", json={"title": "   "})
    assert bad_res.status_code == 400
