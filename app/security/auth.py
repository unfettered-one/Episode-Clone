# security/auth.py
import jwt
from fastapi import Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from models.security import AuthenticatedUser
from configuration import settings

from errorhub.exceptions import (
    UnauthorizedException,
    ForbiddenException,
)
from errorhub.models import ErrorSeverity


security_scheme = HTTPBearer(auto_error=False)


def verify_access_token(
    credentials: HTTPAuthorizationCredentials = Security(security_scheme),
) -> AuthenticatedUser:
    if credentials is None:
        raise UnauthorizedException(
            service="Episode Game",
            message="Authorization credentials not provided",
            severity=ErrorSeverity.LOW,
            environment=settings.get_environment(),
            context={
                "detail": "No authorization credentials were provided in the request.",
            },
        )

    token = credentials.credentials
    jwt_secret_key = settings.get_secret_key()
    try:
        payload = jwt.decode(
            token,
            jwt_secret_key,
            algorithms=[settings.get_jwt_algorithm()],
        )
    except jwt.ExpiredSignatureError:
        raise UnauthorizedException(
            service="Episode Game",
            message="Token has expired",
            severity=ErrorSeverity.LOW,
            environment=settings.get_environment(),
            context={
                "detail": "The provided token has expired.",
            },
        )
    except jwt.InvalidTokenError:
        raise UnauthorizedException(
            service="Episode Game",
            message="Token is invalid",
            severity=ErrorSeverity.LOW,
            environment=settings.get_environment(),
            context={
                "detail": "The provided token is invalid.",
            },
        )
    if "sub" not in payload:
        raise UnauthorizedException(
            service="Episode Game",
            message="Invalid token payload",
            severity=ErrorSeverity.LOW,
            environment=settings.get_environment(),
            context={"detail": "`sub` is missing from token payload."},
        )
    # Enforce access token
    if payload.get("type") != "access":
        raise ForbiddenException(
            service="Episode Game",
            message="Invalid token type",
            severity=ErrorSeverity.LOW,
            environment=settings.get_environment(),
            context={
                "detail": "The provided token is not an access token.",
            },
        )
    apps = payload.get("apps", [])
    service_name = settings.get_service_name()
    if not any(app.lower() == service_name.lower() for app in apps):
        raise ForbiddenException(
            service="Episode Game",
            message="App access not allowed",
            severity=ErrorSeverity.LOW,
            environment=settings.get_environment(),
            context={
                "detail": "The token does not grant access to the Episode app.",
            },
        )

    return AuthenticatedUser(
        user_id=payload["sub"],
        email=payload.get("email"),
        apps=apps,
    )
