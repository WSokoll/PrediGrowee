# import json

# import pandas as pd
# from app.models import Patients
#
#
# def dir_of_growth_update(db, new_data_file):
#     with open(new_data_file, 'r') as json_file:
#         data = json.load(json_file)
#
#     for patient_id, dir_of_growth in data.items():
#         patient = Patients.query.filter_by(id=patient_id).one_or_none()
#
#         if not patient:
#             print(patient_id + ' not found in the database')
#         else:
#             patient.direction_of_growth = dir_of_growth
#             db.session.commit()

# def extract_from_xlsx(xlsx_file, json_file):
#     df = pd.read_excel(xlsx_file, sheet_name='labels')
#
#     patients_to_labels = dict(zip(df['Name'], df['growth direction']))
#
#     for name, direction in patients_to_labels.items():
#         if direction == 'normal':
#             patients_to_labels[name] = 'mixed'
#         elif direction == 'horizontal':
#             patients_to_labels[name] = 'predominantly horizontal'
#         elif direction == 'vertical':
#             patients_to_labels[name] = 'predominantly vertical'
#         else:
#             patients_to_labels[name] = 'unknown'
#
#     with open(json_file, 'w') as json_file:
#         json.dump(patients_to_labels, json_file, indent=4)
