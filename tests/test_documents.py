# from fastapi.testclient import TestClient
#
# from app.main import app
#
# client = TestClient(app)
#
#
# def test_create_document():
#
#     payload = {
#
#         "user_id": "pytest_user",
#
#         "title": "Test Document",
#
#         "content": "This is pytest content"
#     }
#
#     response = client.post(
#         "/documents",
#         json=payload
#     )
#
#     assert response.status_code in [
#         201,
#         429
#     ]


from fastapi.testclient import TestClient
from app.main import app


def test_create_document():

    payload = {
        "user_id": "pytest_user",
        "title": "Test Document",
        "content": "This is pytest content"
    }

    with TestClient(app) as client:

        response = client.post(
            "/documents",
            json=payload
        )

        assert response.status_code in [201, 429]