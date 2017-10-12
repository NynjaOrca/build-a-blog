from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:nynjaorca@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/add-post', methods=['POST', 'GET'])
def add_post():
    head="Add Post!"
    tError = ''
    bError = ''

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        if not title:
            tError = "You did not enter a title for your post."
        if not body:
            bError = "You did not enter a body for your post."
        
        if tError and bError:
            return render_template('add-post.html', head=head, tError=tError, bError=bError)
        elif tError:
            return render_template('add-post.html', head=head, tError=tError)
        elif bError:
            return render_template('add-post.html', head=head, bError=bError)
        else:
            post = Blog(title, body)
            db.session.add(post)
            db.session.commit()
            return redirect('/?id={}'.format(post.id))


    return render_template("add-post.html", head=head)


@app.route('/post-page', methods=['POST', 'GET'])
def post_page():
    return render_template('post-page.html')

@app.route('/', methods=['POST', 'GET'])
def index():
    head = "Build - A - Blog"
    blog_id = request.args.get('id')
    if blog_id:
        post = Blog.query.get(blog_id)
        return render_template('post-page.html', post=post)
    
    else:
        posts = Blog.query.all()
        return render_template('homepage.html', head=head, posts=posts)

    




if __name__ == "__main__":
    app.run()