from .interview import interview_bp
from .report import report_bp
from .session import session_bp

def register_routes(app):
    app.register_blueprint(interview_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(session_bp)
