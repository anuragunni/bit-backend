from backend import db
from backend.models import MCChoice


# Function to create a mc_choice
def create_mc_choice(data):
    mc_choice = MCChoice(content=data["content"],
                         choice_key=data["choice_key"])

    print(data["is_correct_choice"])
    if data["is_correct_choice"]:
        mc_choice.correct_checkpoint_id = data["checkpoint_id"]
    else:
        mc_choice.checkpoint_id = data["checkpoint_id"]

    return mc_choice


# Function to edit a mc_choice
def edit_mc_choice(mc_choice, data):
    mc_choice.content = data["content"]
    print(data["is_correct_choice"])
    if data["is_correct_choice"]:
        mc_choice.correct_checkpoint_id = data["checkpoint_id"]
    else:
        mc_choice.checkpoint_id = data["checkpoint_id"]

    return


# Function to format data for a mc_choice
def format_mc_choice_data(content, key, checkpoint_id, is_correct):
    data = {
        "content": content,
        "checkpoint_id": checkpoint_id,
        "choice_key": key
    }

    if is_correct:
        data["is_correct_choice"] = True
    else:
        data["is_correct_choice"] = False

    return data


# Function to get a MCChoice whether it is the correct choice or not
def get_mc_choice(data):
    mc_choice = None

    if data["is_correct_choice"]:
        mc_choice = MCChoice.query.filter_by(choice_key=data["choice_key"],
                                             correct_checkpoint_id=data["checkpoint_id"]).first()
    else:
        mc_choice = MCChoice.query.filter_by(choice_key=data["choice_key"],
                                             checkpoint_id=data["checkpoint_id"]).first()

    return mc_choice
