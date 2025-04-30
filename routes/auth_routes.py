from flask import Blueprint, request, jsonify
from models.user import User
from extensions import db, jwt_blocklist, limiter
from schemas.user_schema import UserSchema
from utils.response_wrapper import success_response, error_response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, create_refresh_token, get_jwt_identity, \
    set_refresh_cookies, unset_jwt_cookies
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
        return error_response(str(e.messages), 400)

    if User.query.filter_by(email=data["email"]).first():
        return error_response("Email already registered", 409)

    user = User(email=data["email"])
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()

    access_token = create_access_token(identity=str(user.id))
    refresh_token_value = create_refresh_token(identity=str(user.id))

    response = success_response({
        "message": "User registered successfully",
        "access_token": access_token
    }, 201)

    set_refresh_cookies(response, refresh_token_value)
    return response


@auth_bp.route("/login", methods=["POST"])
@limiter.limit("5/minute")
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

    access_token = create_access_token(identity=str(user.id), additional_claims={"role": user.role})
    refresh_token_value = create_refresh_token(identity=str(user.id), additional_claims={"role": user.role})

    response = success_response({
        "message": "User logged in successfully",
        "access_token": access_token
    }, 201)

    set_refresh_cookies(response, refresh_token_value)
    return response


@auth_bp.route("/logout", methods=["POST"])
@jwt_required(verify_type=False)
def logout():
    jwt_data = get_jwt()
    jti = jwt_data["jti"]
    token_type = jwt_data["type"]

    jwt_blocklist.add(jti)

    response = success_response(f"{token_type.capitalize()} token has been revoked.")
    unset_jwt_cookies(response)
    return response


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True, locations=["cookies"])
def refresh_token():
    current_user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user_id)

    return success_response({
        "access_token": new_access_token
    })