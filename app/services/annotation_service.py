import re

from app.extensions import db
from app.models.document import Document
from app.models.annotation_item import AnnotationItem
from app.services.qwen_service import get_model_response


def annotate_document(document_id):
    document = Document.query.get_or_404(document_id)
    project = document.project

    class_names = [cls.name for cls in project.classes]
    class_map = {cls.name: cls.id for cls in project.classes}
    print(f"Классы для разметки -{class_names}")

    model_result = get_model_response(
        text=document.content,
        annotation_classes=class_names
    )
    print(f"Результат модели - {model_result}")

    #при условии, что документ размечен - удаление старых аннот.
    AnnotationItem.query.filter_by(document_id=document.id).delete()

    for class_name, values in model_result.items():
        class_id = class_map.get(class_name)

        if not class_id:
            continue

        for item in values:
            value = item.get("text") if isinstance(item, dict) else item

            if not value:
                continue

            positions = find_all_occurrences(document.content, value)

            for start, end in positions:
                item = AnnotationItem(
                    document_id=document.id,
                    class_id=class_id,
                    text_word=value,
                    start_position=start,
                    end_position=end
                )
                db.session.add(item)

    db.session.commit()


def find_all_occurrences(text, fragment):

    if not fragment:
        return []

    positions = []

    pattern = re.escape(fragment)

    for match in re.finditer(pattern, text):
        positions.append((match.start(), match.end()))

    return positions