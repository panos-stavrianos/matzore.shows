from datatables import ColumnDT, DataTables
from flask import render_template, session, request, jsonify
from werkzeug.utils import redirect

from app import app, db
from app.forms import CategoryForm
from app.models import Category
from app.tools import cdn, default_cover


@app.route('/categories')
def categories():
    if 'authenticated' not in session:
        return redirect('/login')

    return render_template('categories.html', page='categories', title='Κατηγορίες', cdn=cdn)


@app.route('/get_categories')
def get_categories():
    columns = [
        ColumnDT(Category.id, mData='id'),
        ColumnDT(Category.name, mData='name'),
    ]
    query = db.session.query().select_from(Category)
    params = request.args.to_dict()
    rowTable = DataTables(params, query, columns)
    return jsonify(rowTable.output_result())


@app.route('/category/<category_id>')
def category(category_id):
    if 'authenticated' not in session:
        return redirect('/login')
    category = Category.query.get(int(category_id))

    return render_template('category.html', page='category', title='Κατηγορίες', cdn=cdn, category=category,
                           default_cover=default_cover)


@app.route('/category_add', strict_slashes=False)
@app.route('/category_edit/<category_id>', strict_slashes=False)
@app.route('/category_submit', strict_slashes=False, methods=['GET', 'POST'])
def category_add_edit(category_id=None):
    if 'authenticated' not in session:
        return redirect('/login')
    form = CategoryForm()

    if form.validate_on_submit():  # it's submit!
        form.save_to_db()
        return redirect('/categories')
    else:  # either edit or add
        if category_id:  # populate first for edit
            form.load_from_db(category_id)

    return render_template('category_edit_or_add.html', page='category_edit_or_add', title='Άρθρα', cdn=cdn, form=form)


@app.route('/category_delete/<category_id>')
def category_delete(category_id):
    if 'authenticated' not in session:
        return redirect('/login')
    category = Category.query.get(int(category_id))
    category.authors.clear()
    db.session.commit()

    db.session.delete(category)
    db.session.commit()
    return redirect('/categories')
