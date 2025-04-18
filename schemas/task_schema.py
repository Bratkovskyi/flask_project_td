from marshmallow import Schema, fields, ValidationError, validates


class TaskSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.String(required=True)
    done = fields.Boolean(missing=False)

    @validates("title")
    def validate_title(self, value):
        if not value.strip():
            raise ValidationError("Title cannot be empty")
