from .health import health_bp
from .ticketing import tickets_bp as ticketing_bp

def register_blueprints(app):
    app.register_blueprint(health_bp, url_prefix='/api')
    app.register_blueprint(ticketing_bp)

__all__ = ['register_blueprints', 'health_bp', 'ticketing_bp']
