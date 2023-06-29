from flask import Flask, render_template

app = Flask(__name__)

data = [
    {'id': 1, 'author': 'John Doe', 'title': 'First Post', 'content': 'This is my first post.'},
    {'id': 2, 'author': 'Jane Doe', 'title': 'Second Post', 'content': 'This is another post.'},
    # More blog posts can go here...
]


@app.route('/')
def index():
    return render_template('index.html', posts=data)


if __name__ == '__main__':
    app.run()
