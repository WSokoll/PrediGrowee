from flask_admin.contrib.sqla import ModelView


class OrtParametersModelView(ModelView):
    can_view_details = True
    can_create = False
    can_edit = True
    can_delete = False

    column_list = ['id', 'name']
    column_sortable_list = ['id', 'name']
    form_columns = ['name', 'description']
    column_details_list = ['id', 'variable_name', 'name', 'description']

    column_labels = {
        'id': 'ID',
        'name': 'Parameter name',
        'variable_name': 'Name of the dict key/column in the ort_data table',
        'description': 'Description'
    }
