from flask import Blueprint, render_template, request, redirect, url_for
from app.extensions import db
from app.models.project import Project
from app.models.document import Document
from app.services.annotation_service import annotate_document
from app.services.highlighter import build_highlighted_text
from app.services.export_service import export_csv
from app.services.export_service import export_excel
documents_bp = Blueprint("documents", __name__, url_prefix="/documents")

@documents_bp.route("/upload/<int:project_id>", methods=["GET", "POST"])
def upload_document(project_id):
    project = Project.query.get(project_id)
    if request.method == "POST":
        name = request.form.get("name")
        content = request.form.get("content")
        document = Document(
            name=name,
            content = content,
            project_id=project.id
        )
        db.session.add(document)
        db.session.commit()
        annotate_document(document.id)

        return redirect(url_for("documents.document_detail", document_id=document.id))
    return render_template("documents/upload.html", project=project)

@documents_bp.route("/<int:document_id>")
def document_detail(document_id):
    document = Document.query.get_or_404(document_id)
    highlighted_text = build_highlighted_text(document)
    return render_template(
        "documents/detail.html",
        document=document,
        highlighted_text=highlighted_text
    )


@documents_bp.route('/document/<int:document_id>/export/csv')
def export_to_csv(document_id):
    document = Document.query.get_or_404(document_id)
    response = export_csv(document, document_id)
    return response

@documents_bp.route('/document/<int:document_id>/export/excel')
def export_to_excel(document_id):
    document = Document.query.get_or_404(document_id)
    return export_excel(document, document_id)

