from flask import url_for
from flask_admin.menu import MenuLink

from app import models
from app.views.admin.draw_mode import DrawModeModelView
from app.views.admin.ort_parameters import OrtParametersModelView
from app.views.admin.stats import StatsBaseView


def admin_panel_init(admin, db):

    class LogoutLink(MenuLink):
        def get_url(self):
            return url_for("security.logout")

    class HomePageLink(MenuLink):
        def get_url(self):
            return url_for("welcome.get")

    admin.add_link(HomePageLink(name="Home"))
    admin.add_link(LogoutLink(name="Log out"))

    admin.add_view(DrawModeModelView(models.CaseGrouping, db.session, name='Draw Mode'))
    admin.add_view(OrtParametersModelView(models.OrtParameters, db.session, name='Ort Parameters'))
    admin.add_view(StatsBaseView(session=db.session, models=models, name='Stats', endpoint='stats'))
