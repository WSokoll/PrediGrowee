from flask_admin.contrib.sqla import ModelView


class AboutContentModelView(ModelView):
    can_view_details = True
    can_create = True
    can_edit = True
    can_delete = True

    column_list = ['id', 'title']
    column_sortable_list = ['id', 'title']
    form_columns = ['title', 'content']
    column_details_list = ['id', 'title', 'content']

    column_labels = {
        'id': 'ID',
        'title': 'Card Title',
        'content': 'Content'
    }
