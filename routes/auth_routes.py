from flask import Blueprint, request
from models.user import User
from extensions import db, jwt_blocklist
from schemas.user_schema import UserSchema
from utils.response_wrapper import success_response, error_response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from marshmallow import ValidationError
auth_bp = Blueprint("auth_bp", __name__)
user_schema = UserSchema()


@auth_bp.route("/register", methods=["POST"])
def register():
    json_data = request.get_json()

    if not json_data:
        return error_response("No input data provided", 400)

    try:
        data = user_schema.load(json_data)
    except ValidationError as e:
        print(e)
        return error_response(str(e.messages), 400)

    if User.query.filter_by(email=data["email"]).first():
        return error_response("Email already registered", 409)

    user = User(email=data["email"])
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()

    # 🔐 Сразу создаём токен
    token = create_access_token(identity=str(user.id))

    return success_response({
        "message": "User registered successfully",
        "token": token
    }, status=201)

    # return success_response("User registered successfully", status=201)


@auth_bp.route("/login", methods=["POST"])
def login():
    json_data = request.get_json()
    if not json_data:
        return error_response("No input data provided", 400)

    try:
        data = user_schema.load(json_data)
    except ValidationError as e:
        return error_response(str(e.messages), 400)

    user = User.query.filter_by(email=data["email"]).first()

    if not user or not user.check_password(data["password"]):
        return error_response("Invalid email or password", 401)

    token = create_access_token(identity=str(user.id))
    return success_response({"token": token})


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]  # JWT ID
    jwt_blocklist.add(jti)
    return success_response("Logged out successfully")