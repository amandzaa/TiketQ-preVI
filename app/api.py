from flask_restx import Api, Resource, fields, Namespace
from flask import request, abort
from .models import Ticket
from .extensions import db
from datetime import datetime

# Create API instance
api = Api(
    title='TiketQ API',
    version='1.0',
    description='A simple REST API for managing tickets',
    doc='/docs'
)

# Health check endpoint
@api.route('/health')
class HealthCheck(Resource):
    def get(self):
        """Health check endpoint"""
        return {'status': 'healthy', 'message': 'TiketQ API is running'}

# Create namespace for tickets
tickets_ns = Namespace('tickets', description='Ticket operations')

# Define models for Swagger documentation
ticket_model = api.model('Ticket', {
    'id': fields.Integer(readonly=True, description='Ticket ID'),
    'eventName': fields.String(required=True, description='Event name', example='Rock Concert'),
    'location': fields.String(required=True, description='Event location', example='Stadium Arena'),
    'time': fields.DateTime(required=True, description='Event time', example='2025-06-15T20:00:00'),
    'isUsed': fields.Boolean(description='Whether ticket is used', example=False)
})

ticket_input_model = api.model('TicketInput', {
    'eventName': fields.String(required=True, description='Event name', example='Rock Concert'),
    'location': fields.String(required=True, description='Event location', example='Stadium Arena'),
    'time': fields.String(required=True, description='Event time (ISO format)', example='2025-06-15T20:00:00'),
    'isUsed': fields.Boolean(description='Whether ticket is used', example=False)
})

ticket_update_model = api.model('TicketUpdate', {
    'isUsed': fields.Boolean(required=True, description='Whether ticket is used', example=True)
})

@tickets_ns.route('/')
class TicketList(Resource):
    @tickets_ns.doc('list_tickets')
    @tickets_ns.param('isUsed', 'Filter by usage status (true/false)')
    @tickets_ns.marshal_list_with(ticket_model)
    def get(self):
        """List all tickets"""
        is_used = request.args.get('isUsed')
        query = Ticket.query
        
        if is_used is not None:
            if is_used.lower() == 'true':
                query = query.filter_by(isUsed=True)
            elif is_used.lower() == 'false':
                query = query.filter_by(isUsed=False)
        
        tickets = query.all()
        return tickets

    @tickets_ns.doc('create_ticket')
    @tickets_ns.expect(ticket_input_model)
    @tickets_ns.marshal_with(ticket_model, code=201)
    def post(self):
        """Create a new ticket"""
        data = request.get_json()
        
        if not data:
            abort(400, description='No input data provided')
        
        # Validate required fields
        required_fields = ['eventName', 'location', 'time']
        for field in required_fields:
            if field not in data:
                abort(400, description=f'Missing required field: {field}')
        
        # Validate string lengths
        if len(data['eventName']) < 1 or len(data['eventName']) > 200:
            abort(400, description='eventName must be between 1 and 200 characters')
        
        if len(data['location']) < 1 or len(data['location']) > 200:
            abort(400, description='location must be between 1 and 200 characters')
        
        # Parse and validate datetime
        try:
            event_time = datetime.fromisoformat(data['time'])
            if event_time < datetime.utcnow():
                abort(400, description='Time must be in the future')
        except ValueError:
            abort(400, description='Invalid datetime format. Use ISO format (YYYY-MM-DDTHH:MM:SS)')
        
        # Create ticket
        ticket = Ticket(
            eventName=data['eventName'],
            location=data['location'],
            time=event_time,
            isUsed=data.get('isUsed', False)
        )
        
        db.session.add(ticket)
        db.session.commit()
        
        return ticket, 201

@tickets_ns.route('/<int:ticket_id>')
@tickets_ns.param('ticket_id', 'The ticket identifier')
class TicketResource(Resource):
    @tickets_ns.doc('get_ticket')
    @tickets_ns.marshal_with(ticket_model)
    def get(self, ticket_id):
        """Get a specific ticket"""
        ticket = Ticket.query.get(ticket_id)
        if not ticket:
            abort(404, description=f'Ticket with id {ticket_id} not found')
        return ticket

    @tickets_ns.doc('update_ticket')
    @tickets_ns.expect(ticket_update_model)
    @tickets_ns.marshal_with(ticket_model)
    def patch(self, ticket_id):
        """Mark a ticket as used/unused"""
        ticket = Ticket.query.get(ticket_id)
        if not ticket:
            abort(404, description=f'Ticket with id {ticket_id} not found')
        
        data = request.get_json()
        if not data or 'isUsed' not in data:
            abort(400, description='Missing isUsed field')
        
        ticket.isUsed = bool(data['isUsed'])
        db.session.commit()
        
        return ticket

    @tickets_ns.doc('delete_ticket')
    def delete(self, ticket_id):
        """Delete a ticket"""
        ticket = Ticket.query.get(ticket_id)
        if not ticket:
            abort(404, description=f'Ticket with id {ticket_id} not found')
        
        db.session.delete(ticket)
        db.session.commit()
        
        return {'message': f'Ticket {ticket_id} deleted'}, 200

# Add namespace to API
api.add_namespace(tickets_ns) 