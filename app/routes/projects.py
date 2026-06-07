from flask import Blueprint, render_template,flash, request, redirect, url_for
from app.extensions import db
from app.models.project import Project
from app.models.annotation_class import AnnotationClasses
from app.models.document import Document
from app.models.annotation_item import AnnotationItem

projects_bp = Blueprint('projects', __name__, url_prefix='/projects')

@projects_bp.route('/')
def list_projects():
    projects = Project.query.all()
    return render_template("projects/list.html", projects=projects)

@projects_bp.route('/create', methods=['GET', 'POST'])
def create_project():
    if request.method == 'POST':
        project_name = request.form.get('name')
        class_names_raw = request.form.get('classes')

        project = Project(name=project_name)
        db.session.add(project)
        db.session.flush()

        class_names = [
            item.strip()
            for item in class_names_raw.split(',')
            if item.strip()
        ]
        for class_name in class_names:
            annotation_class = AnnotationClasses(
                project_id = project.id,
                name = class_name
            )
            db.session.add(annotation_class)
        db.session.commit()
        return redirect(url_for('projects.project_detail', project_id = project.id))
    return render_template("projects/create.html")

@projects_bp.route("/<int:project_id>")
def project_detail(project_id):
    project = Project.query.get(project_id)

    return render_template(
        "projects/detail.html",
        project=project,
        documents = project.documents,
        classes = project.classes
    )

@projects_bp.route('/project/<int:project_id>/delete', methods=['POST'])
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)

    try:
        db.session.delete(project)
        db.session.commit()
        flash(f'Проект "{project.name}" успешно удален.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Ошибка при удалении проекта.', 'error')

    return redirect(url_for('projects.list_projects'))


@projects_bp.route('/document/<int:document_id>/delete', methods=['POST'])
def delete_document(document_id):
    document = Document.query.get_or_404(document_id)
    project_id = document.project_id

    try:

        AnnotationItem.query.filter_by(document_id=document.id).delete()

        db.session.delete(document)
        db.session.commit()
        flash(f'Документ "{document.name}" успешно удален.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Ошибка при удалении документа.', 'error')

    return redirect(url_for('projects.project_detail', project_id=project_id))
