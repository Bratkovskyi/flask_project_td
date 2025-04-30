import redis
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, get_jwt_identity
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import timedelta

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
jwt_blocklist = set()  # for checking
migrate = Migrate()
limiter = Limiter(key_func=get_remote_address,  storage_uri="redis://localhost:6379")

redis_conn = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)


def add_token_to_blocklist(jti: str, expires_in_seconds: int):
    redis_conn.setex(f"bl:{jti}", timedelta(seconds=expires_in_seconds), "revoked")


def is_token_revoked(jti: str) -> bool:
    return redis_conn.exists(f"bl:{jti}") == 1
