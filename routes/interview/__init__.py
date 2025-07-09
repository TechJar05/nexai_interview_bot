from flask import Blueprint

# Import each modular route blueprint
from .start_interview import start_bp
from .question_routes import question_bp
from .pause_check import pause_bp
from .answer_processing import answer_bp
from .interview_view import view_bp

# Create main interview blueprint
interview_bp = Blueprint('interview', __name__, url_prefix='/jobs/interview')

# Register sub-blueprints under /interview
interview_bp.register_blueprint(start_bp)
interview_bp.register_blueprint(question_bp)
interview_bp.register_blueprint(pause_bp)
interview_bp.register_blueprint(answer_bp)
interview_bp.register_blueprint(view_bp)