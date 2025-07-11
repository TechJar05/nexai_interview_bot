# from .interview import interview_bp
# from .report import report_bp
# from .session import session_bp

# def register_routes(app):
#     app.register_blueprint(interview_bp)
#     app.register_blueprint(report_bp)
#     app.register_blueprint(session_bp)


from .interview import interview_bp
from .report import report_bp
from .interview.interview_view import view_bp

def register_routes(app):
    app.register_blueprint(interview_bp)     # All API routes (e.g., start_interview, get_question)
    app.register_blueprint(report_bp)        # Report generation (e.g., generate_report)
    app.register_blueprint(view_bp)          # Interview page with token (e.g., /<token>/)
