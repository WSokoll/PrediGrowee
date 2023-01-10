from flask import abort, redirect, url_for, request
from flask_admin import AdminIndexView
from flask_login import current_user


class CustomAdminIndexView(AdminIndexView):
    def is_visible(self):
        return False

    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated and
                current_user.has_role('Admin'))

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            if current_user.is_authenticated:
                abort(403)
            else:
                return redirect(url_for('security.login', next=request.url))
