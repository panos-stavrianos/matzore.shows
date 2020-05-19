# -*- coding: utf-8 -*-
from datatables import ColumnDT, DataTables
from flask import render_template, session, request, jsonify
from werkzeug.utils import redirect

from app import db, app
from app.forms import ShowForm
from app.models import Show
from app.tools import cdn, default_logo


@app.route('/')
@app.route('/shows')
def shows():
    if 'authenticated' not in session:
        return redirect('/login')

    return render_template('shows.html', page='shows', title='Εκπομπές', cdn=cdn)


@app.route('/get_shows')
def get_shows():
    columns = [
        ColumnDT(Show.id, mData='id'),
        ColumnDT(Show.name, mData='name'),
        ColumnDT(Show.short_description, mData='short_description'),
        ColumnDT(Show.email, mData='email'),
        ColumnDT(Show.facebook, mData='facebook'),
        ColumnDT(Show.instagram, mData='instagram'),
        ColumnDT(Show.twitter, mData='twitter')
    ]
    query = db.session.query().select_from(Show)
    params = request.args.to_dict()
    rowTable = DataTables(params, query, columns)
    return jsonify(rowTable.output_result())


@app.route('/show/<show_id>')
def show(show_id):
    if 'authenticated' not in session:
        return redirect('/login')
    show = Show.query.get(int(show_id))

    return render_template('show.html', page='show', title='Εκπομπές', cdn=cdn, show=show, default_logo=default_logo)


@app.route('/show_add', strict_slashes=False)
@app.route('/show_edit/<show_id>', strict_slashes=False)
@app.route('/show_submit', strict_slashes=False, methods=['GET', 'POST'])
def show_add_edit(show_id=None):
    if 'authenticated' not in session:
        return redirect('/login')
    form = ShowForm()
    form.init()
    if form.validate_on_submit():  # it's submit!
        form.save_to_db()
        return redirect('/shows')
    else:  # either edit or add
        if show_id:  # populate first for edit
            form.load_from_db(show_id)

    return render_template('show_edit_or_add.html', page='show_edit_or_add', title='Mέλος', cdn=cdn, form=form)


@app.route('/show_delete/<show_id>')
def show_delete(show_id):
    if 'authenticated' not in session:
        return redirect('/login')
    show = Show.query.get(int(show_id))
    show.members.clear()
    db.session.commit()

    db.session.delete(show)
    db.session.commit()
    return redirect('/shows')
