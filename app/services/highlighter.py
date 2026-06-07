# app/services/highlighter.py

from markupsafe import Markup, escape


COLOR_CLASSES = [
    "ann-color-1",
    "ann-color-2",
    "ann-color-3",
    "ann-color-4",
    "ann-color-5",
    "ann-color-6",
]


def build_highlighted_text(document):
    text = document.content

    annotations = sorted(
        document.annotation_items,
        key=lambda x: x.start_position
    )

    annotations = remove_overlaps(annotations)

    result = []
    cursor = 0

    class_color_map = {}

    for ann in annotations:
        start = ann.start_position
        end = ann.end_position

        if start < cursor:
            continue

        class_id = ann.class_id

        color_index = (ann.class_id % len(COLOR_CLASSES)) + 1
        css_class = f"ann-color-{color_index}"

        #текст для аннотации
        result.append(escape(text[cursor:start]))

        #аннотированный фрагмент
        fragment = escape(text[start:end])
        label = escape(ann.annotation_class.name)

        result.append(
            Markup(
                f'<span class="annotation {css_class}" '
                f'title="{label}">{fragment}</span>'
            )
        )

        cursor = end

    result.append(escape(text[cursor:]))

    return Markup("").join(result)


#функция для выбора пересекающихся аннотаций
def remove_overlaps(annotations):

    sorted_annotations = sorted(
        annotations,
        key=lambda x: (x.start_position, -(x.end_position - x.start_position))
    )

    result = []
    last_end = -1

    for ann in sorted_annotations:
        if ann.start_position >= last_end:
            result.append(ann)
            last_end = ann.end_position

    return result