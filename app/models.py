from sqlalchemy import DateTime, func

from app import db

show_have_members = db.Table('show_have_members',
                             db.Column('show_id', db.Integer, db.ForeignKey('show.id'), primary_key=True),
                             db.Column('member_id', db.Integer, db.ForeignKey('member.id'), primary_key=True))

article_have_members = db.Table('article_have_members',
                                db.Column('article_id', db.Integer, db.ForeignKey('article.id'), primary_key=True),
                                db.Column('member_id', db.Integer, db.ForeignKey('member.id'), primary_key=True))

event_have_tags = db.Table('event_have_tags',
                           db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True),
                           db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True))

article_have_tags = db.Table('article_have_tags',
                             db.Column('article_id', db.Integer, db.ForeignKey('article.id'), primary_key=True),
                             db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True))


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    display_name = db.Column(db.String(200), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    email = db.Column(db.String(120), unique=True)
    facebook = db.Column(db.String(500), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    avatar = db.Column(db.String(500), nullable=True)

    articles = db.relationship('Article', secondary=article_have_members, lazy='subquery',
                               backref=db.backref('articles', lazy=True))
    shows = db.relationship('Show', secondary=show_have_members, lazy='subquery',
                            backref=db.backref('shows', lazy=True))

    def to_dict(self):
        name = self.display_name if self.display_name else self.name
        return {'id': self.id,
                'name': name,
                'bio': self.bio,
                'avatar': self.avatar}

    def to_dict_full(self):
        member = self.to_dict()
        member['shows'] = list(map(lambda show: show.to_dict(), self.shows))
        member['articles'] = list(map(lambda article: article.to_dict(), self.articles))
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


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True)
    short_description = db.Column(db.String(500))
    body = db.Column(db.Text)
    cover = db.Column(db.String(500), nullable=True)
    published = db.Column(db.Boolean, default=False)
    created_at = db.Column(DateTime(), default=func.now())

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship("Category", back_populates="articles")

    authors = db.relationship('Member', secondary=article_have_members, lazy='subquery',
                              backref=db.backref('authors', lazy=True))

    tags = db.relationship('Tag', secondary=article_have_tags, lazy='subquery',
                           backref=db.backref('a_tags', lazy=True))

    def to_dict(self):
        return {'id': self.id,
                'title': self.title,
                'short_description': self.short_description,
                'body': self.body,
                'cover': self.cover,
                'published': self.published,
                'created_at': self.created_at,
                }

    def to_dict_full(self):
        article = self.to_dict()
        article['authors'] = list(map(lambda member: member.to_dict(), self.authors))
        article['category'] = self.category.to_dict()
        return article

    def __repr__(self):
        return '<Article: {}>'.format(self.to_dict())


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True)
    short_description = db.Column(db.String(500))
    location = db.Column(db.String(200), nullable=True)
    coordinates = db.Column(db.String(200), nullable=True)
    event_date = db.Column(DateTime(), default=func.now())
    body = db.Column(db.Text)
    cover = db.Column(db.String(500), nullable=True)
    published = db.Column(db.Boolean, default=False)
    created_at = db.Column(DateTime(), default=func.now())

    tags = db.relationship('Tag', secondary=event_have_tags, lazy='subquery',
                           backref=db.backref('tags', lazy=True))

    def to_dict(self):
        return {'id': self.id,
                'title': self.title,
                'short_description': self.short_description,
                'body': self.body,
                'cover': self.cover,
                'event_date': self.event_date,
                'created_at': self.created_at,
                'published': self.published}

    def to_dict_full(self):
        event = self.to_dict()
        event['tags'] = list(map(lambda tag: tag.to_dict(), self.tags))
        return event

    def __repr__(self):
        return '<Event: {}>'.format(self.to_dict())


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)

    articles = db.relationship("Article", back_populates="category")

    def to_dict(self):
        return {'id': self.id,
                'name': self.name}

    def to_dict_full(self):
        category = self.to_dict()
        category['articles'] = list(map(lambda article: article.to_dict(), self.articles))
        return category

    def __repr__(self):
        return '<Category: {}>'.format(self.to_dict())


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))

    events = db.relationship('Event', secondary=event_have_tags, lazy='subquery',
                             backref=db.backref('events', lazy=True))

    articles = db.relationship('Article', secondary=article_have_tags, lazy='subquery',
                               backref=db.backref('t_articles', lazy=True))

    def to_dict(self):
        return {'id': self.id,
                'name': self.name}

    def to_dict_full(self):
        tag = self.to_dict()
        tag['events'] = list(map(lambda event: event.to_dict(), self.events))
        return tag

    def __repr__(self):
        return '<Tag: {}>'.format(self.to_dict())


db.create_all()
