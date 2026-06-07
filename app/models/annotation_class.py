from app.extensions import db
from app.models.annotation_item import AnnotationItem

class AnnotationClasses(db.Model):
    __tablename__ = 'annotation_classes'

    id = db.Column(db.Integer, primary_key=True)

    project_id = db.Column(
        db.Integer,
        db.ForeignKey('projects.id', ondelete='CASCADE'),
        nullable=False
    )
    name = db.Column(db.Text, nullable=False)
    project = db.relationship("Project", back_populates="classes")

    annotation_items = db.relationship(
        "AnnotationItem",
        back_populates="annotation_class",
        cascade="all, delete-orphan",
    )