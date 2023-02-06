import random

from sqlalchemy import and_, not_

from app.models import CaseGrouping, Patients


def get_random_patient_id(excluded=None, group_nr=None):
    """
    :param excluded: list of excluded patient_id's (already done)
    :param group_nr: group number from case_grouping table if grouping mode on

    :return patient_id: random patient id or None if no cases left
    """

    if not excluded:
        excluded = []

    if group_nr is not None:
        patient_id_list = CaseGrouping.query.with_entities(CaseGrouping.patient_id).\
            filter(and_(CaseGrouping.group_nr == group_nr, not_(CaseGrouping.patient_id.in_(excluded)))).all()
    else:
        patient_id_list = Patients.query.with_entities(Patients.id).filter(not_(Patients.id.in_(excluded))).all()

    if patient_id_list:
        return (random.choice(patient_id_list))[0]
    else:
        return None
