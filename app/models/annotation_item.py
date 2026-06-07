from app.extensions import db


class AnnotationItem(db.Model):
    __tablename__ = "annotation_items"

    id = db.Column(db.Integer, primary_key=True)

    document_id = db.Column(
        db.Integer,
        db.ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False
    )

    class_id = db.Column(
        db.Integer,
        db.ForeignKey("annotation_classes.id", ondelete="CASCADE"),
        nullable=False
    )

    text_word = db.Column(db.Text, nullable=False)

    start_position = db.Column(db.Integer, nullable=False)

    end_position = db.Column(db.Integer, nullable=False)

    document = db.relationship("Document", back_populates="annotation_items")

    annotation_class = db.relationship(
        "AnnotationClasses",
        back_populates="annotation_items"
    )