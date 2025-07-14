




# # Step 1: app.py

# from flask import Flask, render_template, session
# from flask_session import Session
# import os
# import logging
# from logging.handlers import RotatingFileHandler
# from flask_cors import CORS
# from routes import register_routes
# from utils.helpers import init_interview_data

# def create_app():
#     app = Flask(__name__)
#     app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')

#     app.config['SESSION_TYPE'] = 'filesystem'
#     app.config['SESSION_COOKIE_NAME'] = 'session'
#     session_dir = os.path.join(os.getcwd(), 'flask_session_data')
#     os.makedirs(session_dir, exist_ok=True)
#     app.config['SESSION_FILE_DIR'] = session_dir
#     CORS(app, supports_credentials=True)
#     Session(app)

#     logs_dir = os.path.join(os.getcwd(), 'logs')
#     os.makedirs(logs_dir, exist_ok=True)
#     log_file = os.path.join(logs_dir, 'interview_app.log')
#     handler = RotatingFileHandler(log_file, maxBytes=10_000_000, backupCount=5)
#     handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

#     if not app.logger.handlers:
#         app.logger.addHandler(handler)

#     app.logger.setLevel(logging.DEBUG)

#     register_routes(app)

#     @app.route('/')
#     def home():
#         app.logger.info("Home page accessed")
#         session.clear()
#         session['interview_data'] = init_interview_data()

#         data = {
#             "user_name": "Guest",
#             "email": "",
#             "match_score": "",
#             "jd_text": "",
#             "resume_text": ""
#         }

#         return render_template('index.html', data=data)

#     @app.errorhandler(404)
#     def not_found(error):
#         return render_template('404.html'), 404

#     return app

# if __name__ == '__main__':

#     app = create_app()

#     for rule in app.url_map.iter_rules():
#      print(f"{rule.rule} → {rule.endpoint} [{', '.join(rule.methods)}]")
#     app.run(debug=True, use_reloader=False)





from flask import Flask, render_template, session, jsonify
from flask_session import Session
import os
import logging
from logging.handlers import RotatingFileHandler
from flask_cors import CORS
from routes import register_routes
from utils.helpers import init_interview_data

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')

    # Enable server-side sessions
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_COOKIE_NAME'] = 'session'
    session_dir = os.path.join(os.getcwd(), 'flask_session_data')
    os.makedirs(session_dir, exist_ok=True)
    app.config['SESSION_FILE_DIR'] = session_dir

    # ✅ CORS: allow React frontend to access APIs with cookies
    CORS(app, supports_credentials=True, origins=[
        "http://localhost:5173",               # local React
        "https://your-react-domain.com",       # deployed React domain
    ])

    Session(app)

    # Logging setup
    logs_dir = os.path.join(os.getcwd(), 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    log_file = os.path.join(logs_dir, 'interview_app.log')
    handler = RotatingFileHandler(log_file, maxBytes=10_000_000, backupCount=5)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    if not app.logger.handlers:
        app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG)

    # Register blueprints
    register_routes(app)

    # ✅ Base API check route (required for axios initSession)
    @app.route('/api/ping')
    def ping():
        return jsonify({"status": "ok", "message": "Flask server is running."})

    # Optional: fallback view for root
    @app.route('/')
    def home():
        session.clear()
        session['interview_data'] = init_interview_data()

        data = {
            "user_name": "Guest",
            "email": "",
            "match_score": "",
            "jd_text": "",
            "resume_text": ""
        }

        return render_template('index.html', data=data)

    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404

    return app


if __name__ == '__main__':
    app = create_app()

    # Print available routes
    for rule in app.url_map.iter_rules():
        print(f"{rule.rule} → {rule.endpoint} [{', '.join(rule.methods)}]")

    app.run(debug=True, use_reloader=False, host="0.0.0.0", port=5000)
