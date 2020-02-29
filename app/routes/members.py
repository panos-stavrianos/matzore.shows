from datatables import ColumnDT, DataTables
from flask import render_template, session, jsonify, request
from werkzeug.utils import redirect

from app import db, app
from app.forms import MemberForm
from app.models import Member
from app.tools import default_avatar, cdn


@app.route('/members', methods=['GET', 'POST'])
def members():
    if 'authenticated' not in session:
        return redirect('/login')

    return render_template('members.html', page='members', title='Μέλη', cdn=cdn, members=Member.query.all())


@app.route('/get_members')
def get_members():
    columns = [
        ColumnDT(Member.id, mData='id'),
        ColumnDT(Member.name, mData='name'),
        ColumnDT(Member.email, mData='email'),
        ColumnDT(Member.phone, mData='phone'),
        ColumnDT(Member.facebook, mData='facebook')
    ]
    query = db.session.query().select_from(Member)
    params = request.args.to_dict()
    rowTable = DataTables(params, query, columns)
    return jsonify(rowTable.output_result())


@app.route('/member/<member_id>')
def member(member_id):
    if 'authenticated' not in session:
        return redirect('/login')
    member = Member.query.get(int(member_id))
    return render_template('member.html', page='member', title='Μέλος', cdn=cdn, member=member,
                           default_avatar=default_avatar)


@app.route('/member_add', strict_slashes=False)
@app.route('/member_edit/<member_id>', strict_slashes=False)
@app.route('/member_submit', strict_slashes=False, methods=['GET', 'POST'])
def member_add_edit(member_id=None):
    if 'authenticated' not in session:
        return redirect('/login')
    form = MemberForm()
    if form.validate_on_submit():  # it's submit!
        form.save_to_db()
        return redirect('/members')
    else:  # either it's edit or add
        if member_id:  # populate for edit
            form.load_from_db(member_id)
    return render_template('member_edit_or_add.html', page='member_edit_or_add', title='Mέλος', cdn=cdn, form=form)


@app.route('/member_delete/<member_id>')
def member_delete(member_id):
    if 'authenticated' not in session:
        return redirect('/login')
    member = Member.query.get(int(member_id))
    member.shows.clear()
    db.session.commit()

    db.session.delete(member)
    db.session.commit()
    return redirect('/members')
