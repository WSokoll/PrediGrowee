from flask import url_for
from flask_admin.menu import MenuLink

from app import models
from app.views.admin.about_content import AboutContentModelView
from app.views.admin.config import ConfigModelView
from app.views.admin.draw_mode import DrawModeModelView
from app.views.admin.errors import ErrorsBaseView
from app.views.admin.ort_parameters import OrtParametersModelView
from app.views.admin.results import ResultsModelView
from app.views.admin.stats import StatsBaseView
from app.views.admin.surveys import SurveysModelView
from app.views.admin.users import UserModelView


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
    admin.add_view(AboutContentModelView(models.AboutContent, db.session, name='About'))
    admin.add_view(StatsBaseView(session=db.session, models=models, name='Stats', endpoint='stats'))
    admin.add_view(UserModelView(models.User, db.session, name='Users', endpoint='users'))
    admin.add_view(ResultsModelView(models.UserResults, db.session, name='Results', endpoint='res'))
    admin.add_view(SurveysModelView(models.Survey, db.session, name='Surveys', endpoint='surveys'))
    admin.add_view(ConfigModelView(models.Config, db.session, name='Config'))
    admin.add_view(ErrorsBaseView(config_model=models.Config, name='Errors', endpoint='errors'))
