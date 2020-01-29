from datatables import ColumnDT, DataTables
from flask import render_template, send_from_directory, redirect, session, request, jsonify
from flask_wtf import FlaskForm
from google.cloud import storage
from wtforms import PasswordField, SubmitField, StringField, FileField, SelectMultipleField, HiddenField, TextAreaField
from wtforms.validators import DataRequired

from app import app, db
from app.models import Member, Show
from app.tools import cdn


class LoginForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class ShowForm(FlaskForm):
    id = HiddenField("id")
    name = StringField('Όνομα εκπομπής', validators=[DataRequired()])
    description = TextAreaField('Περιγραφή', validators=[DataRequired()])
    members = SelectMultipleField('Μέλη')
    show_logo = FileField()
    email = StringField('Email')
    facebook = StringField('Facebook')
    instagram = StringField('Instagram')
    twitter = StringField('Twitter')

    submit = SubmitField('Προσθήκη')


class MemberForm(FlaskForm):
    id = HiddenField("id")
    name = StringField('Όνομα', validators=[DataRequired()])
    email = StringField('Email')
    facebook = StringField('Facebook')
    phone = StringField('Τηλέφωνο')

    submit = SubmitField('Προσθήκη')


@app.route('/<path:path>')
def send_js(path):
    return send_from_directory('static', path)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():

        if app.config['SECRET_KEY'] == form.password.data:
            session['authenticated'] = form.password.data
            return redirect('/')
    return render_template('login.html', page='login', title='Home', cdn=cdn, form=form)


@app.route('/members', methods=['GET', 'POST'])
def members():
    if 'authenticated' not in session:
        return redirect('/login')

    return render_template('members.html', page='members', title='Μέλη', cdn=cdn, members=Member.query.all())


@app.route('/member/<member_id>')
def member(member_id):
    if 'authenticated' not in session:
        return redirect('/login')
    member = Member.query.get(int(member_id))
    return render_template('member.html', page='member', title='Μέλος', cdn=cdn, member=member)


@app.route('/member_add', strict_slashes=False)
@app.route('/member_edit/<member_id>', strict_slashes=False)
@app.route('/member_submit', strict_slashes=False, methods=['GET', 'POST'])
def member_add_edit(member_id=None):
    if 'authenticated' not in session:
        return redirect('/login')
    form = MemberForm()

    if form.validate_on_submit():  # it's submit!
        print("validate_on_submit")
        if form.id.data:
            member = Member.query.get(int(form.id.data))
            member.name = form.name.data
            member.email = form.email.data
            member.facebook = form.facebook.data
            member.phone = form.phone.data
        else:
            member = Member(name=form.name.data,
                            email=form.email.data,
                            facebook=form.facebook.data,
                            phone=form.phone.data)
        db.session.add(member)
        db.session.commit()
        return redirect('/members')
    else:  # either edit or add
        if member_id:  # populate first for edit
            member = Member.query.get(int(member_id))
            form.id.data = member.id
            form.name.data = member.name
            form.email.data = member.email
            form.phone.data = member.phone
            form.facebook.data = member.facebook

    return render_template('member_edit_or_add.html', page='member_edit_or_add', title='Mέλος', cdn=cdn, form=form)


@app.route('/')
@app.route('/shows')
def shows():
    if 'authenticated' not in session:
        return redirect('/login')

    return render_template('shows.html', page='shows', title='Εκπομπές', cdn=cdn)


@app.route('/show/<show_id>')
def show(show_id):
    if 'authenticated' not in session:
        return redirect('/login')
    show = Show.query.get(int(show_id))
    return render_template('show.html', page='show', title='Εκπομπές', cdn=cdn, show=show)


@app.route('/show_add', strict_slashes=False)
@app.route('/show_edit/<show_id>', strict_slashes=False)
@app.route('/show_submit', strict_slashes=False, methods=['GET', 'POST'])
def show_add_edit(show_id=None):
    if 'authenticated' not in session:
        return redirect('/login')
    form = ShowForm()
    form.members.choices = list(map(lambda member: (str(member.id), member.name), Member.query.all()))

    logo = 'https://images.unsplash.com/photo-1507808973436-a4ed7b5e87c9?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=800&q=80'
    if form.validate_on_submit():  # it's submit!
        print("validate_on_submit")
        if form.id.data:  # edit
            show = Show.query.get(int(form.id.data))
            show.name = form.name.data
            show.description = form.description.data
            show.email = form.email.data
            show.facebook = form.facebook.data
            show.instagram = form.instagram.data
            show.twitter = form.twitter.data
            if form.show_logo.data:
                show.logo = upload(form.show_logo.data)
            show.members = list(map(lambda member_id: Member.query.get(int(member_id)), form.members.data))
        else:  # add
            show = Show(name=form.name.data,
                        description=form.description.data,
                        email=form.email.data,
                        facebook=form.facebook.data,
                        instagram=form.instagram.data,
                        twitter=form.twitter.data,
                        logo=upload(form.show_logo.data))
            show.members = list(map(lambda member_id: Member.query.get(int(member_id)), form.members.data))
        db.session.add(show)
        db.session.commit()

        return redirect('/shows')
    else:  # either edit or add
        if show_id:  # populate first for edit
            show = Show.query.get(int(show_id))
            form.id.data = show.id
            form.name.data = show.name
            form.description.data = show.description
            form.email.data = show.email
            form.facebook.data = show.facebook
            form.instagram.data = show.instagram
            form.twitter.data = show.twitter
            form.members.data = list(map(lambda member: str(member.id), show.members))
            if show.logo:
                logo = show.logo

    return render_template('show_edit_or_add.html', page='show_edit_or_add', title='Mέλος', cdn=cdn, form=form,
                           logo=logo)


def upload(uploaded_file):
    """Process the uploaded file and upload it to Google Cloud Storage."""

    if not uploaded_file:
        return None

    # Create a Cloud Storage client.
    gcs = storage.Client()

    # Get the bucket that the file will be uploaded to.
    bucket = gcs.get_bucket(app.config['CLOUD_STORAGE_BUCKET'])

    # Create a new blob and upload the file's content.
    blob = bucket.blob(uploaded_file.filename)

    blob.upload_from_string(
        uploaded_file.read(),
        content_type=uploaded_file.content_type
    )
    blob.make_public()

    # The public URL can be used to directly access the uploaded file via HTTP.
    return blob.public_url


@app.route('/logout')
def logout():
    session.pop('authenticated')
    return redirect('/login')


@app.route('/get_members')
def get_members():
    """Return server side data."""
    # defining columns
    columns = [
        ColumnDT(Member.id, mData='id'),
        ColumnDT(Member.name, mData='name'),
        ColumnDT(Member.email, mData='email'),
        ColumnDT(Member.phone, mData='phone'),
        ColumnDT(Member.facebook, mData='facebook')
    ]

    # defining the initial query depending on your purpose
    query = db.session.query().select_from(Member)

    # GET parameters
    params = request.args.to_dict()

    # instantiating a DataTable for the query and table needed
    rowTable = DataTables(params, query, columns)

    # returns what is needed by DataTable
    return jsonify(rowTable.output_result())


@app.route('/get_shows')
def get_shows():
    """Return server side data."""
    # defining columns
    columns = [
        ColumnDT(Show.id, mData='id'),
        ColumnDT(Show.name, mData='name'),
        ColumnDT(Show.description, mData='description'),
        ColumnDT(Show.email, mData='email'),
        ColumnDT(Show.facebook, mData='facebook'),
        ColumnDT(Show.instagram, mData='instagram'),
        ColumnDT(Show.twitter, mData='twitter')
    ]

    # defining the initial query depending on your purpose
    query = db.session.query().select_from(Show)

    # GET parameters
    params = request.args.to_dict()

    # instantiating a DataTable for the query and table needed
    rowTable = DataTables(params, query, columns)

    # returns what is needed by DataTable
    return jsonify(rowTable.output_result())