import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'postgresql://postgres:1234@localhost:5432/semantic_annotation'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")