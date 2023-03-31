from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from zadar.blueprints.auth import login_required
from zadar.db import get_db

from math import ceil

bp = Blueprint('posts', __name__)


@bp.route('/', methods=('GET', 'POST'))
@login_required
def index():
    category = request.args.get('category', 'ALL', type=str)
    page = request.args.get('page', 1, type=int)

    db = get_db()

    total_posts = 0
    posts_per_page = 5
    current_offset = posts_per_page * (page - 1)

    if category == 'ALL':
        total_posts = db.execute(
            'SELECT COUNT(*) '
            'FROM post'
        ).fetchone()[0]
    else:
        total_posts = db.execute(
            'SELECT COUNT(*) '
            'FROM post '
            'WHERE category = ?',
            (category, )
        ).fetchone()[0]

    if request.method == 'POST':
        category = request.form['category']
        if category == "ALL":
            posts = db.execute(
                'SELECT p.id, title, body, category, created, author_id, username '
                'FROM post p JOIN user u ON p.author_id = u.id '
                'ORDER BY created DESC '
                'LIMIT ? OFFSET ?',
                (posts_per_page, current_offset)
            ).fetchall()
        else:
            posts = db.execute(
                'SELECT p.id, title, body, category, created, author_id, username '
                'FROM post p JOIN user u ON p.author_id = u.id '
                'WHERE p.category = ? '
                'ORDER BY created DESC '
                'LIMIT ? OFFSET ?',
                (category, posts_per_page, current_offset)
            ).fetchall()

        if category == 'ALL':
            total_posts = db.execute(
                'SELECT COUNT(*) '
                'FROM post'
            ).fetchone()[0]
        else:
            total_posts = db.execute(
                'SELECT COUNT(*) '
                'FROM post '
                'WHERE category = ?',
                (category, )
            ).fetchone()[0]
        
    else:
        if category == "ALL":
            posts = db.execute(
                'SELECT p.id, title, body, category, created, author_id, username '
                'FROM post p JOIN user u ON p.author_id = u.id '
                'ORDER BY created DESC '
                'LIMIT ? OFFSET ?',
                (posts_per_page, current_offset)
            ).fetchall()
        else:
            posts = db.execute(
                'SELECT p.id, title, body, category, created, author_id, username '
                'FROM post p JOIN user u ON p.author_id = u.id '
                'WHERE p.category = ? '
                'ORDER BY created DESC '
                'LIMIT ? OFFSET ?',
                (category, posts_per_page, current_offset)
            ).fetchall()

    total_pages = ceil(total_posts / posts_per_page)

    return render_template(
        'posts/index.html', 
        posts=posts, 
        total_pages=total_pages,
        category=category,
        current_page=page,
        categories=get_categories())

@bp.route('/profile', methods=('GET', 'POST'))
@login_required
def get_profile():
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', 'ALL', type=str)

    db = get_db()

    total_posts = 0
    posts_per_page  = 5
    current_offset = posts_per_page * (page - 1)

    if category == 'ALL':
        total_posts = db.execute(
            'SELECT COUNT(*) '
            'FROM post p '
            'JOIN user u ON p.author_id = u.id '
            'WHERE p.author_id = ?',
            (g.user['id'],)
        ).fetchone()[0]
    else:
        total_posts = db.execute(
            'SELECT COUNT(*) '
            'FROM post p '
            'JOIN user u ON p.author_id = u.id '
            'WHERE p.author_id = ? AND p.category = ?',
            (g.user['id'], category)
        ).fetchone()[0]

    if request.method == 'POST':
        category = request.form['category']
        if category == "ALL":
            posts = db.execute(
                'SELECT p.id, title, body, category, created, author_id, username '
                'FROM post p JOIN user u ON p.author_id = u.id '
                'WHERE p.author_id = ? '
                'ORDER BY created DESC '
                'LIMIT ? OFFSET ?',
                (g.user['id'], posts_per_page , current_offset)
            ).fetchall()
        else:
            posts = db.execute(
                'SELECT p.id, title, body, category, created, author_id, username '
                'FROM post p JOIN user u ON p.author_id = u.id '
                'WHERE p.author_id = ? AND p.category = ? '
                'ORDER BY created DESC '
                'LIMIT ? OFFSET ?',
                (g.user['id'], category, posts_per_page , current_offset)
            ).fetchall()

        if category == 'ALL':
            total_posts = db.execute(
                'SELECT COUNT(*) '
                'FROM post p '
                'JOIN user u ON p.author_id = u.id '
                'WHERE p.author_id = ?',
                (g.user['id'],)
            ).fetchone()[0]
        else:
            total_posts = db.execute(
                'SELECT COUNT(*) '
                'FROM post p '
                'JOIN user u ON p.author_id = u.id '
                'WHERE p.author_id = ? AND p.category = ?',
                (g.user['id'], category)
            ).fetchone()[0]
    else:
        if category == "ALL":
            posts = db.execute(
                'SELECT p.id, title, body, category, created, author_id, username '
                'FROM post p JOIN user u ON p.author_id = u.id '
                'WHERE p.author_id = ? '
                'ORDER BY created DESC '
                'LIMIT ? OFFSET ?',
                (g.user['id'], posts_per_page , current_offset)
            ).fetchall()
        else:
            posts = db.execute(
                'SELECT p.id, title, body, category, created, author_id, username '
                'FROM post p JOIN user u ON p.author_id = u.id '
                'WHERE p.author_id = ? AND p.category = ? '
                'ORDER BY created DESC '
                'LIMIT ? OFFSET ?',
                (g.user['id'], category, posts_per_page , current_offset)
            ).fetchall()
    
    total_pages = ceil(total_posts / posts_per_page)

    likes = db.execute(
        'SELECT likes.type, COUNT(*) as count '
        'FROM likes '
        'WHERE user_id = ? '
        'GROUP BY likes.type',
        (g.user['id'],)
    ).fetchall()

    likes_count = 0
    dislikes_count = 0

    for row in likes:
        if row['type'] == 'like':
            likes_count = row['count']
        elif row['type'] == 'dislike':
            dislikes_count = row['count']

    prev_page = page - 1 if page > 1 else None
    next_page = page + 1 if page < total_pages else None

    user_timestamp = db.execute(
        'SELECT user_timestamp '
        'FROM user '
        'WHERE id = ? ',
        (g.user['id'],)
    ).fetchone()[0]

    formatted_date = format_date(user_timestamp)

    return render_template(
        'posts/profile.html',
        posts_count=total_posts,
        likes=likes_count,
        dislikes=dislikes_count,
        posts=posts,
        date=formatted_date,
        category=category,
        prev_page=prev_page,
        next_page=next_page,
        page=page,
        total_pages=total_pages,
        categories=get_categories()
    )

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        category = request.form['category']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, category, author_id)'
                ' VALUES (?, ?, ?, ?)',
                (title, body, category, g.user['id'])
            )
            db.commit()
            return redirect(url_for('posts.index'))

    return render_template('posts/create.html', categories=get_categories())


def get_categories():
    return ['GENERAL', 'TEMTEMUP', 'OPINION']

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, category, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

def get_comments(id):
    db = get_db()
    comments = db.execute('SELECT c.id, c.post_id, c.user_id, u.username, c.created, c.body '
                          'FROM comments c JOIN user u ON c.user_id = u.id '
                          'WHERE c.post_id = ? '
                          'ORDER BY c.created DESC', (id,)).fetchall()
    
    return comments

@bp.route('/post/<int:id>', methods=['GET', 'POST'])
@login_required
def post(id):
    db = get_db()
    post = get_post(id, False)
    likes = get_likes(id)
    comments = get_comments(id)

    if request.method == 'POST':
        comment_body = request.form['body']
        user_id = g.user['id']
        db.execute('INSERT INTO comments (post_id, user_id, body) VALUES (?, ?, ?)',
                   (id, user_id, comment_body))
        db.commit()

        return redirect(url_for('posts.post', id=id))

    return render_template(
        'posts/post.html', 
        post=post, 
        comments=comments,
        likes=likes, 
        categories=get_categories()
    )

@bp.route('/post/like/<int:id>', methods=['POST'])
@login_required
def like_post(id):
    db = get_db()

    existing_vote = db.execute(
        'SELECT type FROM likes WHERE post_id = ? AND user_id = ?',
        (id, g.user['id'])
    ).fetchone()

    if existing_vote:
        flash('You have already voted on this post.')
    else:
        if 'like' in request.form:
            db.execute(
                'INSERT INTO likes (post_id, user_id, type) VALUES (?, ?, "like")',
                (id, g.user['id'])
            )
        elif 'dislike' in request.form:
            db.execute(
                'INSERT INTO likes (post_id, user_id, type) VALUES (?, ?, "dislike")',
                (id, g.user['id'])
            )

        db.commit()
        
        flash('Vote submitted')
    return redirect(url_for('posts.post', id=id))

def get_likes(id):
    db = get_db()

    likes = db.execute(
        'SELECT '
        'COUNT(CASE WHEN type = "like" THEN 1 ELSE NULL END) as likes, '
        'COUNT(CASE WHEN type = "dislike" THEN 1 ELSE NULL END) as dislikes '
        'FROM likes '
        'WHERE post_id = ?',
        (id,)
    ).fetchone()

    return likes

@bp.route('/update/<int:id>', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        category = request.form['category']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)

        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?, category = ?'
                ' WHERE id = ?',
                (title, body, category, id)
            )
            db.commit()
            return redirect(url_for('posts.index'))

    return render_template('posts/update.html', post=post, categories=get_categories())


@bp.route('/delete/<int:id>', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('posts.index'))

def format_date(date):
    formatted_date = date.strftime('%d %B %Y').replace(' 0', ' ')

    return formatted_date.replace('{S}', 'th').replace('{st}', 'st').replace('{nd}', 'nd').replace('{rd}', 'rd').replace('{th}', 'th')