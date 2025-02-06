from jwt import decode as jwt_decode
from fast_zero.security import create_access_token, SECRET_KEY


def test_jwt():
    data = {"test": "test"}
    token = create_access_token(data)

    decoded = jwt_decode(token, SECRET_KEY, algorithms=["HS256"])

    assert decoded["test"] == data["test"]
    assert decoded["exp"]
