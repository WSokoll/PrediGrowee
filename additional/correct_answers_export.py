import xlrd  # xlrd version == 1.2.0 (pip install xlrd==1.2.0)

from app.models import Patients


# this function was created to transfer data (correct answer (category, e.g. mixed) for each patient)
# from xlsx file to database
#
# xlsx file structure:
#   column A -> patient ID
#   column C -> category (category number assigment hardcoded below)
def correct_answers_export(db, excel_path):

    category = {
        1: 'predominantly horizontal',
        2: 'mixed',
        3: 'predominantly vertical'
    }

    # reading xlsx file
    excel_data = xlrd.open_workbook(excel_path)
    worksheet = excel_data.sheet_by_index(0)

    for row in range(1, 463):
        patient_id = worksheet.cell_value(row, 0)
        cat = int(worksheet.cell_value(row, 2))

        patient = Patients.query.filter_by(id=patient_id).one_or_none()

        if not patient:
            print(patient_id + ' not found in the database')
        else:
            patient.direction_of_growth = category[cat]
            db.session.commit()
