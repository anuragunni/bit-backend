from backend import db
from backend.hooks.utils import call_step_routes
from backend.models import Card, Hint, HintStatus


# Function to assign children hints to a parent
def assign_hint_to_parent(hint, data):
    if data["is_card_hint"]:
        parent = Card.query.filter_by(filename=data["parent_filename"]).first()
        hint.card_id = parent.id
    else:
        parent = Hint.query.filter_by(filename=data["parent_filename"]).first()
        parent.hints.append(hint)

    return


# Function to create a hint
def create_hint(data):
    hint = Hint(name=data["name"],
                gems=data["gems"],
                order=data["order"],
                filename=data["filename"],
                github_raw_data=data["github_raw_data"]
                )

    return hint


# Function to create a list of HintStatus Models based on an array of hints
def create_hint_status(activity_prog, hints):
    for hint in hints:
        hint_status = HintStatus(activity_progress_id=activity_prog.id,
                                 is_unlocked=False,
                                 card_id=hint.card_id)
        hint_status.hint = hint

        db.session.commit()

        for children_hint in hint.hints:
            child_hint_status = HintStatus(activity_progress_id=activity_prog.id,
                                           parent_hint_id=hint_status.id,
                                           is_unlocked=False)
            child_hint_status.hint = children_hint

    return


# Function to edit a hint
def edit_hint(hint, data):
    hint.name = data["name"]
    hint.gems = data["gems"]
    hint.order = data["order"]
    hint.filename = data["filename"]
    hint.github_raw_data = data["github_raw_data"]
    assign_hint_to_parent(hint, data)
    call_step_routes(data["content"]["steps"], hint.id, "hint", data["content"]["image_folder"])

    # hint.steps = get_steps(contentful_data["parameters"]["steps"]["en-US"])

    # if "children_hints" in contentful_data["parameters"]:
    #     hint.hint_children = assign_hints_to_parent_hint(contentful_data["parameters"]["children_hints"]["en-US"])

    return


# Function to sort a cards hints
def sort_hints(hints):
    hints.sort(key=lambda x: x.id)

    for hint in hints:
        if hint.hints:
            sort_hints(hint.hints)

    return


# A function to sort a HintStatus objects
def sort_hint_status(hints):
    hints.sort(key=lambda x: x.hint.id)

    for hint in hints:
        if hint.hints:
            sort_hint_status(hint.hints)

    return
