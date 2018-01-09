from flask import Flask, render_template, url_for, request, redirect, g
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/jason/Projects/flask-sqlalchemy/Flask_Blog/blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Blog(db.Model):
	id = db.Column(db.Integer(), primary_key=True)
	title = db.Column(db.String(50))
	subtitle = db.Column(db.String(50))
	author = db.Column(db.String(20))
	#date_posted = db.Column(db.String(20))
	date_posted = db.Column(db.DateTime())
	content = db.Column(db.Text())

@app.route('/')
@app.route('/<int:page_num>')
def index(page_num=None):
	#posts = Blog.query.order_by(Blog.date_posted.desc()).all()
	if page_num:
		posts = Blog.query.order_by(Blog.date_posted.desc()).paginate(per_page=5, page=page_num, error_out=True)	
		return render_template('index.html', posts=posts)
	else:
		posts = Blog.query.order_by(Blog.date_posted.desc()).paginate(per_page=5, page=1, error_out=True)	
		return render_template('index.html', posts=posts)

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/contact')
def contact():
	return render_template('contact.html')

@app.route('/post/<int:post_id>')
def post(post_id):
	post = Blog.query.filter_by(id=post_id).one()
	return render_template('post.html', post=post)

@app.route('/addpost', methods=['GET','POST'])
def addpost():
	if request.method == 'POST':
		title = request.form['title']
		subtitle = request.form['subtitle']
		author = request.form['author']
		content = request.form['content']
		#date_posted = datetime.now().strftime('%d %B, %Y')
		blog_post = Blog(title=title, subtitle= subtitle, author=author, date_posted=datetime.now(), content=content)
		db.session.add(blog_post)
		db.session.commit()
		return redirect(url_for('index', page_num=1))
	return render_template('add.html')

if __name__ == '__main__':
	app.run(debug=True)