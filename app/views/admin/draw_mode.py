from flask import abort, flash, redirect, url_for
from flask_admin import expose
from flask_admin.contrib.sqla import ModelView

from app.app import db
from app.models import Config


class DrawModeModelView(ModelView):
    list_template = 'admin/views/draw_mode_list.html'

    can_view_details = False
    can_create = True
    can_edit = True
    can_delete = True

    column_list = ['patient_id', 'group_nr']
    column_sortable_list = ['patient_id', 'group_nr']
    form_columns = ['patient_id', 'group_nr']

    column_labels = {
        'patient_id': 'Patient ID',
        'group_nr': 'Group Number'
    }

    @expose('/')
    def index_view(self):
        config = Config.query.filter_by(name='grouping_mode_on').one_or_none()

        if not config:
            flash('grouping_mode_on key was not found in the database')
            self._template_args['grouping_mode_on'] = None
        else:
            self._template_args['grouping_mode_on'] = config.value

        return super(DrawModeModelView, self).index_view()

    # status variable:
    #   - on  (cases will be drawn from defined groups)
    #   - off (cases will be drawn randomly)
    @expose('/grouping/mode/<string:status>', methods=['GET'])
    def change_draw_config(self, status: str):
        if status not in ['on', 'off']:
            abort(404)

        config = Config.query.filter_by(name='grouping_mode_on').one_or_none()
        if not config:
            flash('grouping_mode_on key was not found in the database')
            return redirect(url_for('casegrouping.index_view'))

        if status == 'on':
            config.value = True
        else:
            config.value = False

        db.session.commit()
        return redirect(url_for('casegrouping.index_view'))
