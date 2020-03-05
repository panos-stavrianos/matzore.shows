# -*- coding: utf-8 -*-
from flask import render_template, session
from werkzeug.utils import redirect

from app import db, app
from app.forms import ScheduleForm
from app.models import Schedule, days
from app.tools import cdn


@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
    if 'authenticated' not in session:
        return redirect('/login')
    schedule = Schedule.query.all()
    data = {}
    for day in days:
        data[day] = []
    for record in schedule:
        data[record.day].append(record)
    for day in data:
        data[day] = sorted(data[day], key=lambda record: record.from_time)
    return render_template('schedule.html', page='schedule', title='Πρόγραμμα εκπομπών', cdn=cdn, days=days,
                           schedule=data)


@app.route('/schedule_add', strict_slashes=False)
@app.route('/schedule_edit/<schedule_id>', strict_slashes=False)
@app.route('/schedule_submit', strict_slashes=False, methods=['GET', 'POST'])
def schedule_add_edit(schedule_id=None):
    if 'authenticated' not in session:
        return redirect('/login')
    form = ScheduleForm()
    form.init()
    if form.validate_on_submit():  # it's submit!
        form.save_to_db()
        return redirect('/schedule')
    else:  # either edit or add
        if schedule_id:  # populate first for edit
            form.load_from_db(schedule_id)

    return render_template('schedule_edit_or_add.html', page='schedule_edit_or_add', title='Πρόγραμμα εκπομπών',
                           cdn=cdn, form=form)


@app.route('/schedule_delete/<schedule_id>')
def schedule_delete(schedule_id):
    if 'authenticated' not in session:
        return redirect('/login')
    schedule = Schedule.query.get(int(schedule_id))
    db.session.delete(schedule)
    db.session.commit()
    return redirect('/schedule')
