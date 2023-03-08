from app.app import db
from flask_security.models import fsqla_v2


class Role(db.Model, fsqla_v2.FsRoleMixin):
    __tablename__ = 'role'
    __table_args__ = {'extend_existing': True}

    def __repr__(self):
        return self.name


class User(db.Model, fsqla_v2.FsUserMixin):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}

    def __repr__(self):
        return self.email

    def __iter__(self):
        values = vars(self)
        for attr in self.__mapper__.columns.keys():
            if attr in values:
                yield attr, values[attr]


class OrtData(db.Model):
    __tablename__ = 'ort_data'
    __table_args__ = {'extend_existing': True}

    sn_mp = db.Column(db.Numeric(asdecimal=False))
    facial_axis = db.Column(db.Numeric(asdecimal=False))
    y_axis = db.Column(db.Numeric(asdecimal=False))
    point_a_to_nasion_perp = db.Column(db.Numeric(asdecimal=False))
    pog_to_nasion_perp = db.Column(db.Numeric(asdecimal=False))
    antegonial_notch_depth = db.Column(db.Numeric(asdecimal=False))
    mn_base_angle = db.Column(db.Numeric(asdecimal=False))
    mn_ramus_angle = db.Column(db.Numeric(asdecimal=False))
    sn_pog = db.Column(db.Numeric(asdecimal=False))
    snb = db.Column(db.Numeric(asdecimal=False))
    sna = db.Column(db.Numeric(asdecimal=False))
    sn_pp = db.Column(db.Numeric(asdecimal=False))
    anb = db.Column(db.Numeric(asdecimal=False))
    afh_pfh = db.Column(db.Numeric(asdecimal=False))


class OrtParameters(db.Model):
    __tablename__ = 'ort_parameters'
    __table_args__ = {'extend_existing': True}


class Patients(db.Model):
    __tablename__ = 'patients'
    __table_args__ = {'extend_existing': True}


class CaseGrouping(db.Model):
    __tablename__ = 'case_grouping'
    __table_args__ = {'extend_existing': True}


class Config(db.Model):
    __tablename__ = 'config'
    __table_args__ = {'extend_existing': True}


class Survey(db.Model):
    __tablename__ = 'survey'
    __table_args__ = {'extend_existing': True}


class UserResults(db.Model):
    __tablename__ = 'user_results'
    __table_args__ = {'extend_existing': True}

