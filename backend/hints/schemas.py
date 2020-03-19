from backend import ma
from backend.steps.schemas import StepSchema
from marshmallow import fields


# This schema is used to validate the card form data
class HintFormSchema(ma.ModelSchema):
    name = fields.Str(required=True)
    gems = fields.Int(required=True)
    order = fields.Int(required=True)
    filename = fields.Str(required=True)
    parent_filename = fields.Str(required=True)
    is_card_hint = fields.Bool(required=True)
    github_raw_data = fields.Str(required=True)
    content = fields.Dict(required=False)

    class Meta:
        # Fields to show when sending data
        fields = ("name", "gems", "order", "filename", "parent_filename", "is_card_hint", "github_raw_data", "content")
        ordered = True


# This schema is used to keep track of hint data
class HintSchema(ma.ModelSchema):
    id = fields.Int(required=True)
    contentful_id = fields.Str(required=True)
    name = fields.Str(required=True)
    order = fields.Int(required=True)
    parent = fields.Int(missing=None, required=False)
    steps = fields.Nested(StepSchema, many=True)
    hints = fields.Nested("HintSchema", only=("id", "contentful_id", "order", "hints"), many=True)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "contentful_id", "name", "order", "parent", "steps", "hints")
        ordered = True


class HintStatusSchema(ma.ModelSchema):
    hint = fields.Nested("HintSchema", only=("id", "contentful_id"), many=False, required=True)
    hints = fields.Nested("HintStatusSchema", only=("is_unlocked", "hint", "hints"), many=True)
    is_unlocked = fields.Boolean(required=True)

    class Meta:
        # Fields to show when sending data
        fields = ("hint", "hints", "is_unlocked")
        ordered = True


hint_form_schema = HintFormSchema()
hint_schema = HintSchema()
hint_status_schemas = HintStatusSchema(many=True)
