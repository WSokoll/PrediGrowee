# xlrd, beautifulsoup4, lxml - required libs
import re

import xlrd  # xlrd version == 1.2.0
from bs4 import BeautifulSoup
from app.models import Patients, OrtData


# this function was created to transfer data from xlsx and XML files to the database
def export(db, excel_path, xml_path):

    # reading xlsx file
    excel_data = xlrd.open_workbook(excel_path)
    worksheet = excel_data.sheet_by_index(0)

    # saving data to dict (key == (patient_id, age))
    ed_dict = {}
    for row in range(1, 1363):
        ed_dict[(worksheet.cell_value(row, 0), int(worksheet.cell_value(row, 1)))] = {
            'patient_id': worksheet.cell_value(row, 0),
            'age': int(worksheet.cell_value(row, 1)),
            'sn_mp': worksheet.cell_value(row, 2),
            'facial_axis': worksheet.cell_value(row, 3),
            'y_axis': worksheet.cell_value(row, 4),
            'point_a_to_nasion_perp': worksheet.cell_value(row, 5),
            'pog_to_nasion_perp': worksheet.cell_value(row, 6),
            'antegonial_notch_depth': worksheet.cell_value(row, 7),
            'mn_base_angle': worksheet.cell_value(row, 8),
            'mn_ramus_angle': worksheet.cell_value(row, 9),
            'sn_pog': worksheet.cell_value(row, 10),
            'snb': worksheet.cell_value(row, 11),
            'sna': worksheet.cell_value(row, 12),
            'sn_pp': worksheet.cell_value(row, 13),
            'anb': worksheet.cell_value(row, 15),
            'afh_pfh': worksheet.cell_value(row, 16),
            'point_a_to_pog_along_fh': worksheet.cell_value(row, 17)
        }

    # reading xml file
    with open(xml_path, 'r') as f:
        xml_data = f.read()

    bs_data = BeautifulSoup(xml_data, 'xml')

    for patient in bs_data.find_all('patient'):
        patient_id = patient.find('ID').text

        if not re.match(r'^[a-zA-Z].*$', patient_id):
            continue

        sex = patient.find('sex').text
        datasets = patient.find_all('dataset')
        linked_objects = patient.find_all('linkedObject')

        # convert datasets and linked_objects to dicts with <grouping> tag as key
        datasets = {dataset.find('grouping').text: dataset for dataset in datasets}
        linked_objects = {l_object.find('grouping').text: l_object for l_object in linked_objects}

        # check if there is 3 or more photos (otherwise data is useless)
        if len(datasets) >= 3:
            photos_dict = {}
            for grouping, dataset in datasets.items():
                if not linked_objects[grouping]:
                    continue
                else:
                    linked_object = linked_objects[grouping]

                    age = int(dataset.find('date').text[:4]) - 2000
                    path = linked_object.find('link').text[24:]
                    photos_dict[age] = path

            if len(photos_dict) >= 3 \
                    and any(age in photos_dict.keys() for age in [7, 8, 9, 10]) \
                    and any(age in photos_dict.keys() for age in [11, 12, 13]) \
                    and max(photos_dict.keys()) > 13:
                not_enough_data = False

                patient_database = Patients(
                    id=patient_id,
                    sex=sex
                )

                ages = []
                for age in photos_dict.keys():
                    ages.append(age)
                ages.sort()

                ort_data = []
                for year in [ages[0], ages[1], max(photos_dict.keys())]:
                    if (patient_id, year) in ed_dict.keys():
                        ort_data.append(OrtData(
                            patient_id=patient_id,
                            photo_number=1 if year == ages[0] else 2 if year == ages[1] else 3,
                            age=year,
                            sn_mp=ed_dict[(patient_id, year)]['sn_mp'],
                            facial_axis=ed_dict[(patient_id, year)]['facial_axis'],
                            y_axis=ed_dict[(patient_id, year)]['y_axis'],
                            point_a_to_nasion_perp=ed_dict[(patient_id, year)]['point_a_to_nasion_perp'],
                            pog_to_nasion_perp=ed_dict[(patient_id, year)]['pog_to_nasion_perp'],
                            antegonial_notch_depth=ed_dict[(patient_id, year)]['antegonial_notch_depth'],
                            mn_base_angle=ed_dict[(patient_id, year)]['mn_base_angle'],
                            mn_ramus_angle=ed_dict[(patient_id, year)]['mn_ramus_angle'],
                            sn_pog=ed_dict[(patient_id, year)]['sn_pog'],
                            snb=ed_dict[(patient_id, year)]['snb'],
                            sna=ed_dict[(patient_id, year)]['sna'],
                            sn_pp=ed_dict[(patient_id, year)]['sn_pp'],
                            anb=ed_dict[(patient_id, year)]['anb'],
                            afh_pfh=ed_dict[(patient_id, year)]['afh_pfh'],
                            point_a_to_pog_along_fh=ed_dict[(patient_id, year)]['point_a_to_pog_along_fh'],
                            path=photos_dict[year]
                        ))
                    else:
                        not_enough_data = True

                if not not_enough_data:
                    # save data to the database
                    db.session.add(patient_database)
                    db.session.commit()

                    for data in ort_data:
                        db.session.add(data)
                    db.session.commit()
