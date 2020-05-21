# -*- coding: utf-8 -*-
from datatables import ColumnDT, DataTables
from flask import render_template, session, request, jsonify
from werkzeug.utils import redirect

from app import app, db
from app.forms import EventForm
from app.models import Event, Tag
from app.tools import cdn, default_cover


@app.route('/events')
def events():
    if 'authenticated' not in session:
        return redirect('/login')

    return render_template('events.html', page='events', title='Εκδηλώσεις', cdn=cdn)


@app.route('/get_events')
def get_events():
    columns = [
        ColumnDT(Event.id, mData='id'),
        ColumnDT(Event.title, mData='title'),
        ColumnDT(Event.short_description, mData='short_description'),
        ColumnDT(Event.published, mData='published'),
        ColumnDT(Event.event_date, mData='event_date')
    ]
    query = db.session.query().select_from(Event)
    params = request.args.to_dict()
    rowTable = DataTables(params, query, columns)
    return jsonify(rowTable.output_result())


@app.route('/event/<event_id>')
def event(event_id):
    if 'authenticated' not in session:
        return redirect('/login')
    event = Event.query.get(int(event_id))
    try:
        lat, lng = event.coordinates.split(',')
    except:
        lat, lng = 0, 0
    return render_template('event.html', page='event', title='Εκδηλώσεις', cdn=cdn, event=event,
                           default_cover=default_cover, lat=lat, lng=lng, )


@app.route('/tag/<tag_id>')
def tag(tag_id):
    if 'authenticated' not in session:
        return redirect('/login')
    tag = Tag.query.get(int(tag_id))

    return render_template('tag.html', page='tag', title='Tag', cdn=cdn, tag=tag,
                           default_cover=default_cover)


@app.route('/event_add', strict_slashes=False)
@app.route('/event_edit/<event_id>', strict_slashes=False)
@app.route('/event_submit', strict_slashes=False, methods=['GET', 'POST'])
def event_add_edit(event_id=None):
    if 'authenticated' not in session:
        return redirect('/login')
    form = EventForm()
    form.init()
    print('event_add_edit')

    for fieldName, errorMessages in form.errors.items():
        print(fieldName, errorMessages)
        for err in errorMessages:
            # do something with your errorMessages for fieldName
            print(err)

    if form.validate_on_submit():  # it's submit!
        form.save_to_db()
        return redirect('/events')
    else:  # either edit or add
        if event_id:  # populate first for edit
            form.load_from_db(event_id)

    return render_template('event_edit_or_add.html', page='event_edit_or_add', title='Εκδηλώσεις', cdn=cdn, form=form)


@app.route('/event_delete/<event_id>')
def event_delete(event_id):
    if 'authenticated' not in session:
        return redirect('/login')
    event = Event.query.get(int(event_id))
    event.tags.clear()
    db.session.commit()

    db.session.delete(event)
    db.session.commit()
    return redirect('/events')
