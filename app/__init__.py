from flask import Flask
from config import Config
from extensions import db, jwt, bcrypt, jwt_blocklist, migrate
from routes.task_routes import task_bp
from errors.handlers import register_error_handlers
from routes.auth_routes import auth_bp
from extensions import limiter
from flask_cors import CORS

from models.user import User
from models.task import Task


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initial extensions
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": app.config['CORS_ORIGINS']}},
         supports_credentials=app.config['CORS_SUPPORTS_CREDENTIALS'])

    # Registration blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)

    # Registration error handlers
    register_error_handlers(app)

    # Check revoked tokens
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        return jti in jwt_blocklist

    return app
