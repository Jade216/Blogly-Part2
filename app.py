"""Blogly application."""

from flask import Flask, redirect, request, render_template, flash
from models import db, connect_db, User, Post
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

debug = DebugToolbarExtension(app)

connect_db(app)
with app.app_context():
    db.create_all()


@app.route('/')
def root():
    '''show recent 5 posts, most recent frist'''
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template('posts/homepage.html', posts = posts)

@app.errorhandler(404)
def page_not_found(e):
    '''show 404 ERROR page'''
    return render_template('404.html'), 404

@app.route('/users')
def users_list():
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/index.html', users = users)

@app.route('/users/new')
def users_new_form():
    '''show a form to create a new user'''
    return render_template('users/new.html')

@app.route('/users/new', methods=['POST'])
def add_new():
    ''''handle submission for creating new user'''
    new_user = User(
        first_name = request.form['first_name'],
        last_name = request.form['last_name'],
        image_url = request.form['image_url'] or None)
    
    db.session.add(new_user)
    db.session.commit()
    flash(f'User {new_user.full_name} added.')

    return redirect('/users')

@app.route('/users/<int:user_id>')
def users_info(user_id):
    '''specific user's info page'''
    user = User.query.get_or_404(user_id)
    return render_template('users/info.html', user = user)

@app.route('/users/<int:user_id>/edit')
def users_edit(user_id):
    '''edit page for user'''
    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user = user)

@app.route('/users/<int:user_id>/edit', methods = ['POST'])
def users_update(user_id):
    '''update users after edit'''
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()
    flash(f'User {user.full_name} edited.')

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods = ['POST'])
def users_delete(user_id):
    '''delete an user'''
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f'User {user.full_name} deleted.')

    return redirect('/users')



@app.route('/users/<int:user_id>/posts/new')
def posts_new_form(user_id):
    '''show form to create post for specific user'''
    user = User.query.get_or_404(user_id)
    return render_template('posts/new.html', user = user)

@app.route('/users/<int:user_id>/posts/new', methods =['POST'])
def posts_new(user_id):
    '''handle form submission for new post'''
    user = User.query.get_or_404(user_id)
    new_post = Post(
        title = request.form['title'],
        content = request.form['content'],
        user = user)
    db.session.add(new_post)
    db.session.commit()
    flash(f'Post {new_post.title} added')

    return redirect(f'/user/{user_id}')

@app.route('/posts/<int:post_id>')
def posts_info(post_id):
    '''show the info the specific post'''
    post = Post.query.get_or_404(post_id)
    return render_template('posts/info.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def posts_edit(post_id):
    '''show the page for editing a post'''
    post = Post.query.get_or_404(post_id)
    return render_template('posts/edit.html', post = post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def posts_update(post_id):
    '''handle form submission for post edit'''
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()
    flash(f'Post {{post.title}} edited.')

    return redirect(f'/users/{post.user_id}')

@app.route('/posts/<int:post_id>/delete', methods = ['POST'])
def posts_delete(post_id):
    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    flash(f'Post {post.title} deleted.')

    return redirect(f'/users/{post.user_id}')
