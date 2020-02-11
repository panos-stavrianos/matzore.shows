from sqlalchemy import DateTime, func

from app import db

show_have_members = db.Table('show_have_members',
                             db.Column('show_id', db.Integer, db.ForeignKey('show.id'), primary_key=True),
                             db.Column('member_id', db.Integer, db.ForeignKey('member.id'), primary_key=True))


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    email = db.Column(db.String(120), unique=True)
    facebook = db.Column(db.String(500), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    shows = db.relationship('Show', secondary=show_have_members, lazy='subquery',
                            backref=db.backref('shows', lazy=True))

    def __repr__(self):
        return '<Member {}>'.format(self.name)


class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    description = db.Column(db.Text)
    email = db.Column(db.String(120), nullable=True)
    facebook = db.Column(db.String(500), nullable=True)
    instagram = db.Column(db.String(500), nullable=True)
    twitter = db.Column(db.String(500), nullable=True)
    logo = db.Column(db.String(500), nullable=True)
    members = db.relationship('Member', secondary=show_have_members, lazy='subquery',
                              backref=db.backref('members', lazy=True))

    def __repr__(self):
        return '<Show {}>'.format(self.name)


class Traffic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    radio_name = db.Column(db.String(200))
    listeners = db.Column(db.Integer)
    date_time = db.Column(DateTime(), default=func.now())

    def __repr__(self):
        return '<Traffic {}>'.format(self.name)


db.create_all()
