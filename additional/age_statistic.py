# beautifulsoup4, lxml - required libs

import re
from bs4 import BeautifulSoup


# this function was created to show age statistics from XML file
def age_statistic(xml_path):

    # reading xml file
    with open(xml_path, 'r') as f:
        xml_data = f.read()

    bs_data = BeautifulSoup(xml_data, 'xml')

    age_comparison = {}
    for patient in bs_data.find_all('patient'):
        patient_id = patient.find('ID').text

        if not re.match(r'^[a-zA-Z].*$', patient_id):
            continue

        datasets = patient.find_all('dataset')
        linked_objects = patient.find_all('linkedObject')

        # convert datasets and linked_objects to dicts with <grouping> tag as key
        datasets = {dataset.find('grouping').text: dataset for dataset in datasets}
        linked_objects = {l_object.find('grouping').text: l_object for l_object in linked_objects}

        # check if there is 3 or more photos (otherwise data is useless)
        if len(datasets) >= 3:
            age_list = []
            for grouping, dataset in datasets.items():
                if not linked_objects[grouping]:
                    continue
                else:
                    age_list.append(int(dataset.find('date').text[:4]) - 2000)

            age_list.sort()
            age_list = str(age_list)

            if age_list not in age_comparison.keys():
                age_comparison[age_list] = 1
            else:
                age_comparison[age_list] += 1

    age_comparison = sorted(age_comparison.items(), key=lambda x: x[1], reverse=True)
    for age, number in age_comparison:
        print(str(number) + ': ' + age)
