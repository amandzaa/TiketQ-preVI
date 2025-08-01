#!/usr/bin/env python3
"""
Database initialization script for TiketQ-preVI
"""

from app import create_app
from app.extensions import db
from app.models import Ticket
from datetime import datetime

def init_db():
    """Initialize the database and create tables"""
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✅ Database tables created successfully!")
        
        # Optional: Add some sample data
        sample_tickets = [
            {
                'eventName': 'Rock Concert',
                'location': 'Stadium Arena',
                'time': datetime.fromisoformat('2025-06-15T20:00:00'),
                'isUsed': False
            },
            {
                'eventName': 'Jazz Festival',
                'location': 'City Park',
                'time': datetime.fromisoformat('2025-07-20T18:30:00'),
                'isUsed': True
            }
        ]
        
        for ticket_data in sample_tickets:
            ticket = Ticket(**ticket_data)
            db.session.add(ticket)
        
        db.session.commit()
        print("✅ Sample tickets added to database!")

if __name__ == '__main__':
    init_db() 