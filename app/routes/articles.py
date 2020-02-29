from datatables import ColumnDT, DataTables
from flask import render_template, session, request, jsonify
from werkzeug.utils import redirect

from app import app, db
from app.forms import ArticleForm
from app.models import Article
from app.tools import cdn, default_cover


@app.route('/articles')
def articles():
    if 'authenticated' not in session:
        return redirect('/login')

    return render_template('articles.html', page='articles', title='Άρθρα', cdn=cdn)


@app.route('/get_articles')
def get_articles():
    columns = [
        ColumnDT(Article.id, mData='id'),
        ColumnDT(Article.title, mData='title'),
        ColumnDT(Article.short_description, mData='short_description'),
        ColumnDT(Article.published, mData='published'),
        ColumnDT(Article.created_at, mData='created_at')
    ]
    query = db.session.query().select_from(Article)
    params = request.args.to_dict()
    rowTable = DataTables(params, query, columns)
    return jsonify(rowTable.output_result())


@app.route('/article/<article_id>')
def article(article_id):
    if 'authenticated' not in session:
        return redirect('/login')
    article = Article.query.get(int(article_id))

    return render_template('article.html', page='article', title='Άρθρα', cdn=cdn, article=article,
                           default_cover=default_cover)


@app.route('/article_add', strict_slashes=False)
@app.route('/article_edit/<article_id>', strict_slashes=False)
@app.route('/article_submit', strict_slashes=False, methods=['GET', 'POST'])
def article_add_edit(article_id=None):
    if 'authenticated' not in session:
        return redirect('/login')
    form = ArticleForm()
    form.init()
    print(form.authors.choices)
    if form.validate_on_submit():  # it's submit!
        form.save_to_db()
        return redirect('/articles')
    else:  # either edit or add
        if article_id:  # populate first for edit
            form.load_from_db(article_id)

    return render_template('article_edit_or_add.html', page='article_edit_or_add', title='Άρθρα', cdn=cdn, form=form)


@app.route('/article_delete/<article_id>')
def article_delete(article_id):
    if 'authenticated' not in session:
        return redirect('/login')
    article = Article.query.get(int(article_id))
    article.authors.clear()
    db.session.commit()

    db.session.delete(article)
    db.session.commit()
    return redirect('/articles')
