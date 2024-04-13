"""Blogly application."""

from flask import Flask, render_template
from models import db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = '1234567890'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)
db.init_app(app)

connect_db(app)
db.create_all()

@app.route('/')
def index():
    return redirect(url_for('list_users'))

@app.route('/users')
def list_users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/new', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        image_url = request.form.get('image_url', 'default.jpg')
        
        new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('list_users'))
    
    return render_template('add_user.html')

@app.route('/users/<int:user_id>')
def user_detail(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user_detail.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        user.first_name = request.form.get('first_name')
        user.last_name = request.form.get('last_name')
        user.image_url = request.form.get('image_url', 'default.jpg')
        
        db.session.commit()
        return redirect(url_for('user_detail', user_id=user.id))
    
    return render_template('edit_user.html', user=user)

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('list_users'))

if __name__ == '__main__':
    app.run(debug=True)