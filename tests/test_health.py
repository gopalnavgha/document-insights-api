from fastapi.testclient import TestClient
import sys
import os
from app.main import app



# sys.path.append(
#     os.path.abspath(
#         os.path.join(
#             os.path.dirname(__file__),
#             ".."
#         )
#     )
# )

#client = TestClient(app)

# def test_health():
#
#     response = client.get(
#         "/health"
#     )
#
#     assert response.status_code == 200
#

def test_health():

    with TestClient(app) as client:

        response = client.get(
            "/health"
        )

        assert response.status_code == 200