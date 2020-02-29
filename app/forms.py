from datetime import datetime, timedelta

from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, TextAreaField, SelectMultipleField, FileField, SubmitField, SelectField, \
    TimeField, PasswordField, BooleanField
from wtforms.validators import DataRequired

from app import db
from app.models import Member, Show, PlayingNow, Article, Category, Event, Tag
from app.tools import upload, default_avatar, default_logo, default_cover, TagListField


def get_members_as_choices():
    return list(map(lambda member: (str(member.id), member.name), Member.query.all()))


def get_shows_as_choices():
    return list(map(lambda show: (str(show.id), show.name), Show.query.all()))


def get_categories_as_choices():
    return list(map(lambda category: (str(category.id), category.name), Category.query.all()))


def get_tags_as_choices():
    return list(map(lambda tag: tag.name, Tag.query.all()))


class LoginForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class ShowForm(FlaskForm):
    id = HiddenField("id")
    name = StringField('Όνομα εκπομπής', validators=[DataRequired()])
    short_description = StringField('Σύντομη περιγραφή', validators=[DataRequired()])
    description = TextAreaField('Περιγραφή', validators=[DataRequired()])
    members = SelectMultipleField('Μέλη')
    show_logo = FileField()
    logo = default_logo
    email = StringField('Email')
    facebook = StringField('Facebook')
    instagram = StringField('Instagram')
    twitter = StringField('Twitter')

    submit = SubmitField('Καταχώριση')

    def init(self):
        self.members.choices = get_members_as_choices()

    def save_to_db(self):
        if self.id.data:  # edit
            show = Show.query.get(int(self.id.data))
        else:
            show = Show()
        show.name = self.name.data
        show.short_description = self.short_description.data
        show.description = self.description.data
        show.email = self.email.data
        show.facebook = self.facebook.data
        show.instagram = self.instagram.data
        show.twitter = self.twitter.data
        show.members = list(map(lambda member_id: Member.query.get(int(member_id)), self.members.data))
        if self.show_logo.data:
            show.logo = upload(self.show_logo.data)
        db.session.add(show)
        db.session.commit()

    def load_from_db(self, show_id):
        show = Show.query.get(int(show_id))
        self.id.data = show.id
        self.name.data = show.name
        self.short_description.data = show.short_description
        self.description.data = show.description
        self.email.data = show.email
        self.facebook.data = show.facebook
        self.instagram.data = show.instagram
        self.twitter.data = show.twitter
        self.members.data = list(map(lambda member: str(member.id), show.members))
        if show.logo:
            self.logo = show.logo


class MemberForm(FlaskForm):
    id = HiddenField("id")
    name = StringField('Όνομα', validators=[DataRequired()])
    display_name = StringField('Ψευδώνυμο')
    bio = TextAreaField('Bio')
    email = StringField('Email')
    facebook = StringField('Facebook')
    phone = StringField('Τηλέφωνο')
    member_avatar = FileField()
    avatar = default_avatar

    submit = SubmitField('Καταχώριση')

    def save_to_db(self):
        if self.id.data:
            member = Member.query.get(int(self.id.data))
        else:
            member = Member()
        member.name = self.name.data
        member.display_name = self.display_name.data
        member.bio = self.bio.data
        member.email = self.email.data
        member.facebook = self.facebook.data
        member.phone = self.phone.data
        if self.member_avatar.data:
            member.avatar = upload(self.member_avatar.data)
        db.session.add(member)
        db.session.commit()

    def load_from_db(self, member_id):
        member = Member.query.get(int(member_id))
        self.id.data = member.id
        self.name.data = member.name
        self.display_name.data = member.display_name
        self.bio.data = member.bio
        self.member_avatar.data = member.avatar
        self.email.data = member.email
        self.phone.data = member.phone
        self.facebook.data = member.facebook
        if member.avatar:
            self.avatar = member.avatar


class PlayingNowForm(FlaskForm):
    id = HiddenField("id")
    message = StringField('Μήνυμα')
    show = SelectField('Εκπομπή', choices=get_shows_as_choices())
    until = TimeField('Μέχρι')
    submit = SubmitField('Καταχώριση')

    def init(self):
        self.show.choices = get_shows_as_choices()

    def save_to_db(self):
        playing_now = PlayingNow()
        now = datetime.now()
        print(self.until.data)
        until = datetime.combine(now, self.until.data)

        if now > until:
            until = until + timedelta(days=1)
        playing_now.message = self.message.data
        playing_now.show_id = self.show.data
        playing_now.until_time = until
        db.session.add(playing_now)
        db.session.commit()


class ArticleForm(FlaskForm):
    id = HiddenField("id")
    title = StringField('Τίτλος', validators=[DataRequired()])
    short_description = StringField('Σύντομη περιγραφή', validators=[DataRequired()])
    authors = SelectMultipleField('Συγγραφείς')
    body = TextAreaField('Κείμενο', validators=[DataRequired()])
    published = BooleanField('Δημοσιευμένο')
    category = SelectField('Κατηγορία')
    article_cover = FileField()
    cover = default_cover
    tags = TagListField('Tags')

    submit = SubmitField('Καταχώριση')

    def init(self):
        self.category.choices = get_categories_as_choices()
        self.authors.choices = get_members_as_choices()
        self.tags.choices = get_tags_as_choices()

    def save_to_db(self):
        if self.id.data:  # edit
            article = Article.query.get(int(self.id.data))
        else:
            article = Article()
        article.title = self.title.data
        article.short_description = self.short_description.data
        article.body = self.body.data
        article.published = self.published.data
        article.category_id = self.category.data
        article.authors = list(map(lambda member_id: Member.query.get(int(member_id)), self.authors.data))
        article.tags = []
        for tag in self.tags.data:
            tag_record = Tag.query.filter_by(name=tag).first()
            if not tag_record:
                tag_record = Tag(name=tag)
                db.session.add(tag_record)
                db.session.commit()

            article.tags.append(tag_record)
        if self.article_cover.data:
            article.cover = upload(self.article_cover.data)
        print("article", article)

        db.session.add(article)
        db.session.commit()

    def load_from_db(self, show_id):
        article = Article.query.get(int(show_id))
        self.id.data = article.id
        self.title.data = article.title
        self.short_description.data = article.short_description
        self.body.data = article.body
        self.published.data = article.published
        self.category.data = article.category_id
        self.authors.data = list(map(lambda member: str(member.id), article.authors))
        self.tags.data = list(map(lambda tag: str(tag.name), article.tags))
        if article.cover:
            self.cover = article.cover


class EventForm(FlaskForm):
    id = HiddenField("id")
    title = StringField('Τίτλος', validators=[DataRequired()])
    short_description = StringField('Σύντομη περιγραφή', validators=[DataRequired()])
    event_date = StringField('Ημ/Ώρα')
    location = StringField('Τοποθεσία')
    lat = StringField('lat')
    lng = StringField('lng')
    body = TextAreaField('Κείμενο')
    event_cover = FileField()
    cover = default_cover
    published = BooleanField('Δημοσιευμένο')
    tags = TagListField('Tags')

    submit = SubmitField('Καταχώριση')

    def init(self):
        self.tags.choices = get_tags_as_choices()

    def save_to_db(self):
        if self.id.data:  # edit
            event = Event.query.get(int(self.id.data))
        else:
            event = Event()
        event.title = self.title.data
        event.short_description = self.short_description.data
        event.event_date = datetime.strptime(self.event_date.data, '%H:%M %d/%m/%Y')
        event.location = self.location.data
        if self.lat.data and self.lng.data:
            event.coordinates = self.lat.data + ',' + self.lng.data
        event.body = self.body.data
        event.published = self.published.data
        event.tags = []
        for tag in self.tags.data:
            tag_record = Tag.query.filter_by(name=tag).first()
            if not tag_record:
                tag_record = Tag(name=tag)
                db.session.add(tag_record)
                db.session.commit()

            event.tags.append(tag_record)

        if self.event_cover.data:
            event.cover = upload(self.event_cover.data)
        print("event", event)

        db.session.add(event)
        db.session.commit()

    def load_from_db(self, show_id):
        event = Event.query.get(int(show_id))
        self.id.data = event.id
        self.title.data = event.title
        self.short_description.data = event.short_description
        self.event_date.data = event.event_date.strftime('%H:%M %d/%m/%Y')
        self.location.data = event.location
        if event.coordinates:
            self.lat.data, self.lng.data = event.coordinates.split(',')

        self.body.data = event.body
        self.published.data = event.published
        self.tags.data = list(map(lambda tag: str(tag.name), event.tags))
        if event.cover:
            self.cover = event.cover


class CategoryForm(FlaskForm):
    id = HiddenField("id")
    name = StringField('Όνομα εκπομπής', validators=[DataRequired()])
    submit = SubmitField('Καταχώριση')

    def save_to_db(self):
        if self.id.data:  # edit
            category = Category.query.get(int(self.id.data))
        else:
            category = Category()
        category.name = self.name.data

        db.session.add(category)
        db.session.commit()

    def load_from_db(self, category_id):
        category = Category.query.get(int(category_id))
        self.id.data = category.id
        self.name.data = category.name
