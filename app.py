"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

db.create_all()


@app.route('/')
def root():
    posts = Post.query.order_by(Post.created_on.desc()).limit(3).all()
    users = []
    for post in posts:
        user = User.query.get(post.user_id)
        users.append(user)
    return render_template('homepage.html', posts=posts, users=users)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/users')
def users():
    users = User.query.order_by(User.last_name).all()
    return render_template("users_table.html", users = users)

@app.route('/users/new', methods=('POST', 'GET'))
def add_user():
    if request.method == 'POST':
        first_name = request.form['first']
        last_name = request.form['last']
        image_url = request.form['pic']

        user = User(first_name=first_name, last_name=last_name, image_url=image_url)
        db.session.add(user)
        db.session.commit()
        return redirect('/users')
    else:
        return render_template('add_user.html')

@app.route('/users/<int:user_id>', methods=("POST","GET"))
def user_detail(user_id):
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id=user.id).all()
    return render_template("details.html", user=user, posts=posts)


@app.route('/users/<int:user_id>/edit', methods=('POST', 'GET'))
def user_edit(user_id):
    if request.method == 'POST':
        first_name = request.form['first']
        last_name = request.form['last']
        image_url = request.form['pic']

        user = User.query.get(user_id)
        user.first_name = first_name
        user.last_name = last_name
        user.image_url = image_url
        db.session.commit()
        return redirect(f'/users/{user_id}')
    else:
        user = User.query.get_or_404(user_id)
        return render_template("edit_details.html", user=user)

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>/posts/new', methods=('POST','GET'))
def new_post(user_id):
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        tag_keys = request.form.getlist('tag_keys')

        post = Post(title=title, content=content, user_id=user_id)
        for key in tag_keys:
            tag = Tag.query.get(key)
            post.tags.append(tag)
        db.session.add(post)
        db.session.commit()
        return redirect(f'/users/{user_id}')
    else:
        user = User.query.get_or_404(user_id)
        tags = Tag.query.all()
        return render_template("new_post.html", user=user, tags=tags)

@app.route('/posts/<int:post_id>')
def read_post(post_id):
    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_id)
    return render_template('detail_post.html', post=post, user=user)

@app.route('/posts/<int:post_id>/edit', methods=('POST','GET'))
def edit_post(post_id):
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        tag_keys = request.form.getlist('tag_keys')
        
        post = Post.query.get(post_id)
        post.title = title
        post.content = content
        deleteTags = PostTag.query.filter_by(post_id=post.id)
        for dltg in deleteTags:
            db.session.delete(dltg)
        for key in tag_keys:
            tag = Tag.query.get(key)
            post.tags.append(tag)
        db.session.commit()
        return redirect(f'/posts/{post.id}')
    else:
        post = Post.query.get_or_404(post_id)
        tags = Tag.query.all()
        return render_template("edit_post.html", post=post, tags=tags)


@app.route('/posts/<int:post_id>/delete', methods=['POST','GET'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    user_address = post.user_id
    db.session.delete(post)
    db.session.commit()
    return redirect(f'/users/{user_address}')

@app.route('/tags')
def tags():
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)


@app.route('/tags/<int:tag_id>')
def specific_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('specific_tag.html', tag=tag)

@app.route('/tags/new', methods=('POST','GET'))
def new_tag():
    if request.method == 'POST':
        tag_name = request.form['name']
        post_keys = request.form.getlist('post_keys')
        tag = Tag(name=tag_name)

        for key in post_keys:
            post = Post.query.get(key)
            tag.posts.append(post)
        db.session.add(tag)
        db.session.commit()
        return redirect('/tags')
    else:
        posts = Post.query.all()
        return render_template('new_tag.html', posts=posts)


@app.route('/tags/<int:tag_id>/edit', methods=('POST','GET'))
def edit_tag(tag_id):
    if request.method == 'POST':
        tag_name = request.form['editname']
        tag = Tag.query.get(tag_id)
        tag.name = tag_name
        post_keys = request.form.getlist('post_keys')
        deletePost = PostTag.query.filter_by(tag_id=tag.id)
        for dltpost in deletePost:
            db.session.delete(dltpost)
        for key in post_keys:
            post = Post.query.get(key)
            tag.posts.append(tag)

        db.session.commit()
        return redirect('/tags')
    else:
        tag = Tag.query.get(tag_id)
        posts = Post.query.all()
        return render_template('edit_tag.html', tag=tag, posts=posts)


@app.route('/tags/<int:tag_id>/delete', methods=('POST','GET'))
def delete_tag(tag_id):
    tag = Tag.query.get(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect('/tags')