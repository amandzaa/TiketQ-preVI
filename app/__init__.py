from flask import Flask
from flask_cors import CORS
from .extensions import db, ma, migrate
from .api import api


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    
    # Enable CORS
    CORS(app)

    # Initialize API with Swagger
    api.init_app(app)

    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Not Found', 'message': str(error)}, 404

    @app.errorhandler(400)
    def bad_request(error):
        return {'error': 'Bad Request', 'message': str(error)}, 400

    @app.errorhandler(500)
    def internal_error(error):
        return {'error': 'Internal Server Error', 'message': str(error)}, 500

    return app
