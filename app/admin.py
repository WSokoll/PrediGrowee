from flask import url_for
from flask_admin.menu import MenuLink

from app import models
from app.views.admin.draw_mode import DrawModeModelView


def admin_panel_init(admin, db):
    class LogoutLink(MenuLink):
        def get_url(self):
            return url_for("security.logout")

    admin.add_link(LogoutLink(name="Log out"))
    admin.add_view(DrawModeModelView(models.CaseGrouping, db.session, name='Draw Mode'))
