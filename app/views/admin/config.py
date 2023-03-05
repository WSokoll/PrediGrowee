from flask_admin.contrib.sqla import ModelView


class ConfigModelView(ModelView):
    can_view_details = True
    can_create = False
    can_edit = True
    can_delete = False

    column_list = ['name', 'bool_value', 'int_value']
    column_sortable_list = ['name']
    form_columns = ['bool_value', 'int_value']
    column_details_list = ['id', 'name', 'description', 'bool_value', 'int_value']

    column_labels = {
        'id': 'ID',
        'name': 'Config variable name',
        'description': 'Description',
        'bool_value': 'Boolean value',
        'int_value': 'Integer value'
    }
