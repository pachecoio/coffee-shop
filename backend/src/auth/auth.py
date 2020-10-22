import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen
from src.error_handlers import AuthError


AUTH0_DOMAIN = "thisk8brd.auth0.com"
ALGORITHMS = ["RS256"]
API_AUDIENCE = "http://localhost:4200/drinks"

## Auth Header


def get_token_auth_header():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise AuthError(message="You must be logged in.")
    try:
        return auth_header.split(" ")[1]
    except:
        raise AuthError(message="Authorization malformed.")


def check_permissions(permission, payload):
    if permission != "" and permission not in payload["permissions"]:
        raise AuthError(message="User must have the apropriate permissions.")


def verify_decode_jwt(token):
    jsonurl = urlopen(f"https://{AUTH0_DOMAIN}/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())

    unverified_header = jwt.get_unverified_header(token)

    rsa_key = {}
    if "kid" not in unverified_header:
        raise AuthError(message="Authorization malformed.")

    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"],
            }

    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer="https://" + AUTH0_DOMAIN + "/",
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError(message="Token expired.")

        except jwt.JWTClaimsError:
            raise AuthError(
                message="Incorrect claims. Please, check the audience and issuer."
            )
        except Exception:
            raise AuthError(
                message="Unable to parse authentication token.",
                status_code=400,
            )
    raise AuthError(message="Unable to find the appropriate key.")


def requires_auth(permission=""):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper

    return requires_auth_decorator