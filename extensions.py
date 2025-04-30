from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, get_jwt_identity
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
jwt_blocklist = set()  # for checking
migrate = Migrate()
# limiter = Limiter(get_remote_address)
limiter = Limiter(key_func=lambda: str(get_jwt_identity() or "anonymous"))

