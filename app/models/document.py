from app.extensions import db

class Document(db.Model):
    __tablename__ = 'documents'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)

    project_id = db.Column(
        db.Integer,
        db.ForeignKey('projects.id', ondelete='CASCADE'),
        nullable=False
    )
    project = db.relationship("Project", back_populates="documents")

    annotation_items = db.relationship(
        'AnnotationItem',
        back_populates="document",
        cascade='all, delete-orphan',
    )

