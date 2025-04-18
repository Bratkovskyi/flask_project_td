from marshmallow import Schema, fields, validates, ValidationError


class UserSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

    @validates('email')
    def validate_email(self, value):
        if " " in value:
            raise ValidationError("Email cannot contain spaces")
        if len(value) < 5:
            raise ValidationError("Email is too short")

    @validates('password')
    def validate_password(self, password):
        if len(password) < 8:
            raise ValidationError('Password must be at least 8 characters')