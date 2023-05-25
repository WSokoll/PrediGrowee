from flask_admin.contrib.sqla import ModelView


class ResultsModelView(ModelView):
    can_view_details = False
    can_create = False
    can_edit = False
    can_delete = True

    column_list = ['id', 'user_id', 'user.email']
    column_sortable_list = ['id', 'user_id', 'user.email']

    column_labels = {
        'id': 'ID',
        'user_id': 'User ID',
        'user.email': 'User email'
    }
