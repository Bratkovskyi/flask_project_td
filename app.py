from flask import Flask
from config import Config
from extensions import db, jwt, bcrypt, jwt_blocklist
from routes.task_routes import task_bp
from errors.handlers import register_error_handlers
from routes.auth_routes import auth_bp

from models.user import User
from models.task import Task


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return jti in jwt_blocklist


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
jwt.init_app(app)
bcrypt.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(task_bp)
register_error_handlers(app)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
