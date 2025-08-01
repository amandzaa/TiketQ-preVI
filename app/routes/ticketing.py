from flask import Blueprint, request, jsonify, abort
from ..models.tiketq import Ticket
from ..schemas.ticket_schema import TicketSchema
from ..extensions import db
from marshmallow import ValidationError

tickets_bp = Blueprint('tickets', __name__)
ticket_schema = TicketSchema()
tickets_schema = TicketSchema(many=True)

@tickets_bp.route('/tickets', methods=['GET'])
def get_tickets():
    is_used = request.args.get('isUsed')
    query = Ticket.query
    if is_used is not None:
        if is_used.lower() == 'true':
            query = query.filter_by(isUsed=True)
        elif is_used.lower() == 'false':
            query = query.filter_by(isUsed=False)
    tickets = query.all()
    return jsonify(tickets_schema.dump(tickets))

@tickets_bp.route('/tickets/<int:ticket_id>', methods=['GET'])
def get_ticket(ticket_id):
    ticket = Ticket.query.get(ticket_id)
    if not ticket:
        abort(404, description=f'Ticket with id {ticket_id} not found')
    return ticket_schema.jsonify(ticket)

@tickets_bp.route('/tickets', methods=['POST'])
def create_ticket():
    json_data = request.get_json()
    if not json_data:
        abort(400, description='No input data provided')
    try:
        data = ticket_schema.load(json_data)
    except ValidationError as err:
        return jsonify({'error': 'Bad Request', 'messages': err.messages}), 400
    ticket = Ticket(**data)
    db.session.add(ticket)
    db.session.commit()
    return ticket_schema.jsonify(ticket), 201

@tickets_bp.route('/tickets/<int:ticket_id>', methods=['PATCH'])
def mark_ticket_used(ticket_id):
    ticket = Ticket.query.get(ticket_id)
    if not ticket:
        abort(404, description=f'Ticket with id {ticket_id} not found')
    json_data = request.get_json()
    if not json_data or 'isUsed' not in json_data:
        abort(400, description='Missing isUsed field')
    ticket.isUsed = bool(json_data['isUsed'])
    db.session.commit()
    return ticket_schema.jsonify(ticket)

@tickets_bp.route('/tickets/<int:ticket_id>', methods=['DELETE'])
def delete_ticket(ticket_id):
    ticket = Ticket.query.get(ticket_id)
    if not ticket:
        abort(404, description=f'Ticket with id {ticket_id} not found')
    db.session.delete(ticket)
    db.session.commit()
    return jsonify({'message': f'Ticket {ticket_id} deleted'}) 