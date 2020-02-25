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

    def to_dict(self):
        return {'id': self.id,
                'name': self.name}

    def to_dict_full(self):
        member = self.to_dict()
        member['shows'] = list(map(lambda show: show.to_dict(), self.shows))
        return member

    def __repr__(self):
        return '<Member: {}>'.format(self.to_dict())


class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    short_description = db.Column(db.String(500))
    description = db.Column(db.Text)
    email = db.Column(db.String(120), nullable=True)
    facebook = db.Column(db.String(500), nullable=True)
    instagram = db.Column(db.String(500), nullable=True)
    twitter = db.Column(db.String(500), nullable=True)
    logo = db.Column(db.String(500), nullable=True)
    members = db.relationship('Member', secondary=show_have_members, lazy='subquery',
                              backref=db.backref('members', lazy=True))

    def to_dict(self):
        return {'id': self.id,
                'name': self.name,
                'description': self.description,
                'short_description': self.short_description,
                'email': self.email,
                'facebook': self.facebook,
                'instagram': self.instagram,
                'twitter': self.twitter,
                'logo': self.logo,
                }

    def to_dict_full(self):
        show = self.to_dict()
        show['members'] = list(map(lambda member: member.to_dict(), self.members))
        return show

    def __repr__(self):
        return '<Show: {}>'.format(self.to_dict())


class Traffic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    radio_name = db.Column(db.String(200))
    listeners = db.Column(db.Integer)
    date_time = db.Column(DateTime(), default=func.now())

    def __repr__(self):
        return '<Traffic {}>'.format(self.name)


class PlayingNow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(200))
    start_time = db.Column(DateTime(), default=func.now())
    until_time = db.Column(DateTime(), default=func.now())

    show_id = db.Column(db.Integer, db.ForeignKey(Show.id))
    show = db.relationship(Show, uselist=False)

    def __repr__(self):
        return '<PlayingNow {}>'.format(self.message)


db.create_all()
