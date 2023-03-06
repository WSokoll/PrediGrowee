import json
import os

from flask import current_app


# Function created to find missing photos
def photos_not_found(ort_data_model):
    not_found = {
        'count_found': 0,
        'count_not_found': 0,
        'photos_not_found': []
    }

    ort_data = ort_data_model.query.order_by(ort_data_model.id).all()

    for data in ort_data:
        ort_path = data.path if data.path[0] != '\\' else data.path[1:]
        path = os.path.join(current_app.config['ORT_FOLDER_PATH'], ort_path)

        if not os.path.exists(path):
            not_found['photos_not_found'].append({
                'patient_id': data.patient_id,
                'path': data.path
            })
            not_found['count_not_found'] += 1
        else:
            not_found['count_found'] += 1

    json_not_found = json.dumps(not_found, indent=4)
    with open('not_found.json', 'w') as f:
        print(json_not_found, file=f)
