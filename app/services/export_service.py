import io
import csv
from flask import send_file, Response
import pandas as pd

def export_csv(document, document_id):
    output = io.StringIO()
    writer = csv.writer(output, delimiter=';', quoting=csv.QUOTE_MINIMAL)

    #заголовки Excel
    output.write('\ufeff')
    writer.writerow(['Класс сущности', 'Текст фрагмента', 'Старт (индекс)', 'Конец (индекс)'])

    # Записываем данные аннотаций
    for ann in document.annotation_items:
        writer.writerow([
            ann.annotation_class.name,
            ann.text_word,
            ann.start_position,
            ann.end_position
        ])

    #ретурн файла
    response = Response(output.getvalue(), mimetype='text/csv')
    #имя
    filename = f"document_{document_id}_annotations.csv"
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    return response

def export_excel(document, document_id):
    #словари для дата фрейма
    data = []
    for ann in document.annotation_items:
        data.append({
            'Класс сущности': ann.annotation_class.name,
            'Текст фрагмента': ann.text_word,
            'Старт (индекс)': ann.start_position,
            'Конец (индекс)': ann.end_position
        })

    df = pd.DataFrame(data)


    if df.empty:
        df = pd.DataFrame(columns=['Класс сущности', 'Текст фрагмента', 'Старт (индекс)', 'Конец (индекс)'])


    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Извлеченные сущности', index=False)


        workbook = writer.book
        worksheet = writer.sheets['Извлеченные сущности']
        for col in worksheet.columns:
            max_len = max(len(str(cell.value or '')) for cell in col)
            col_letter = col[0].column_letter
            worksheet.column_dimensions[col_letter].width = max(max_len + 3, 12)

    output.seek(0)

    filename = f"document_{document_id}_annotations.xlsx"
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=filename
    )