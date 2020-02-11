from flask import (Blueprint, request)
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from backend import api, db
from backend.events.decorators import event_exists, has_rsvp, owns_event, valid_event_form
from backend.events.schemas import event_schema
from backend.events.utils import create_event, edit_event
from backend.models import Event, User
from backend.organizations.decorators import organization_exists

# Blueprint for events
events_bp = Blueprint("events", __name__)


# Class for event CRUD routes
class EventCRUD(Resource):
    method_decorators = [jwt_required, event_exists]

    def get(self, event_id):
        event = Event.query.get(event_id)

        return event_schema.dump(event)

    # Function to edit a event
    @owns_event
    @valid_event_form
    def put(self, event_id):
        event = Event.query.get(event_id)
        form_data = request.get_json()
        edit_event(event, form_data)

        db.session.commit()

        return {"message": "Event successfully updated"}, 202

    # Function to delete a event!!
    @owns_event
    def delete(self, event_id):
        event = Event.query.get(event_id)

        db.session.delete(event)
        db.session.commit()

        return {
                   "message": "Event successfully deleted"
               }, 200


# This class is used to delete an event with a POST request
class EventCreate(Resource):
    method_decorators = [jwt_required, organization_exists, valid_event_form]

    # Function to create a event
    def post(self, organization_id):
        form_data = request.get_json()
        event = create_event(form_data, organization_id)

        db.session.add(event)
        db.session.commit()

        return {
                   "message": "Event successfully created"
               }, 202


# Class to control when a user RSVPs for an event
class EventJoin(Resource):
    method_decorators = [jwt_required, event_exists]

    @has_rsvp
    def put(self, event_id):
        event = Event.query.get(event_id)
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        event.rsvp_list.append(user)
        db.session.commit()

        return {
            "message": user.name + " has RSVP'd for " + event.name
        }, 201


# Creates the routes for the classes
api.add_resource(EventCRUD, "/events/<int:event_id>")
api.add_resource(EventCreate, "/organizations/<int:organization_id>/events/create")
api.add_resource(EventJoin, "/events/<int:event_id>/rsvp")
