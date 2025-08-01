from marshmallow import fields, validates, ValidationError
from ..extensions import ma
from datetime import datetime

class TicketSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    eventName = fields.Str(required=True, validate=lambda s: 1 <= len(s) <= 200)
    location = fields.Str(required=True, validate=lambda s: 1 <= len(s) <= 200)
    time = fields.DateTime(required=True, format='iso')
    isUsed = fields.Bool(missing=False)

    @validates('time')
    def validate_time(self, value):
        if value < datetime.utcnow():
            raise ValidationError('Time must be in the future.') 