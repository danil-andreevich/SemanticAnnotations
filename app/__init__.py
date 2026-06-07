from flask import Flask
from app.config import Config
from app.extensions import db, migrate
from app.routes.projects import projects_bp
from app.routes.documents import documents_bp
from app.routes.main import main_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(projects_bp)
    app.register_blueprint(documents_bp)
    app.register_blueprint(main_bp)
    return app
