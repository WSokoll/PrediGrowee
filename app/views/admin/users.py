from flask_admin.contrib.sqla import ModelView


class UserModelView(ModelView):
    can_view_details = False
    can_create = False
    can_edit = False
    can_delete = True

    column_list = ['id', 'email', 'active', 'confirmed_at']
    column_sortable_list = ['id', 'email', 'active', 'confirmed_at']

    column_labels = {
        'id': 'ID',
        'email': 'Email',
        'active': 'Active',
        'confirmed_at': 'Confirmed at'
    }
