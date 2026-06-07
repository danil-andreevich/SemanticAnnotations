from app.extensions import db

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)

    classes = db.relationship(
        'AnnotationClasses',
        back_populates='project',
        cascade='all, delete-orphan'
    )
    documents = db.relationship(
        "Document",
        back_populates='project',
        cascade='all, delete-orphan'
    )