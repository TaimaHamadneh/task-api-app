import pytest
from app import db, create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.create_all()
        with app.test_client() as client:
            yield client
        db.drop_all()

def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}
    
def test_create_task(client):
    response = client.post('/tasks', json={'title': 'Learn K8s'})
    assert response.status_code == 201
    data = response.get_json()
    assert data['title'] == 'Learn K8s'
    assert data['description'] == ''
    assert data['done'] is False

def test_get_tasks(client):
    client.post('/tasks', json={'title': 'Task 1'})
    client.post('/tasks', json={'title': 'Task 2'})

    response = client.get('/tasks')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2
    assert data[0]['title'] == 'Task 1'
    assert data[1]['title'] == 'Task 2'

def test_update_task(client):
    response = client.post('/tasks', json={'title': 'Old Task'})
    task_id = response.get_json()['id']

    response = client.put(f'/tasks/{task_id}', json={'title': 'Updated Task', 'done': True})
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == 'Updated Task'
    assert data['done'] is True

def test_delete_task(client):
    response = client.post('/tasks', json={'title': 'Task to Delete'})
    task_id = response.get_json()['id']

    response = client.delete(f'/tasks/{task_id}')
    assert response.status_code == 200
    assert response.get_json() == {"message": "Task deleted"}

    response = client.get('/tasks')
    data = response.get_json()
    assert all(task['id'] != task_id for task in data)