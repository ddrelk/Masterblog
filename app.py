from flask import Flask, render_template, request, redirect, url_for
import json

post_file = 'storage/data_post.json'

app = Flask(__name__)


def create_file():
    try:
        empty_data = []
        with open('', 'x') as handle:
            json.dump(empty_data, handle)
    except FileExistsError:
        pass


def load_data():
    try:
        with open(post_file, 'r') as handle:
            blog_data = json.load(handle)
    except FileNotFoundError:
        blog_data = []
    return blog_data


def save_data(new_content):
    with open(post_file, 'w') as handle:
        json.dump(new_content, handle, indent=None)


def fetch_post_by_id(post_id):
    for post in blog_post:
        if post['id'] == post_id:
            return post
    return None


blog_post = load_data()


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', posts=blog_post)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Get data from form
        author = request.form['author']
        title = request.form['title']
        content = request.form['content']
        # Check for max ID in the post
        max_id = max([post['id'] for post in blog_post]) if blog_post else 0
        # Create new dictionary
        new_post = {
            "id": max_id + 1,
            "author": author,
            "title": title,
            "content": content
        }
        # Append new dict to existing file
        blog_post.append(new_post)
        # Save file
        save_data(blog_post)
        # Redirect to homepage
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    # Find the blog post with the given id and remove it from the list
    post_index = -1
    for i, post in enumerate(blog_post):
        if post['id'] == post_id:
            post_index = i
            break
    if post_index != -1:
        # Delete post from list
        del blog_post[post_index]
    save_data(blog_post)
    # Redirect back to the home page
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    # Fetch the blog posts from the JSON file
    post = fetch_post_by_id(post_id)
    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
        # Get data from form
        author = request.form['author']
        title = request.form['title']
        content = request.form['content']

        # Update the post in the JSON file
        post['author'] = author
        post['title'] = title
        post['content'] = content
        save_data(blog_post)
        # Redirect back to index
        return redirect('/')
    # Else, it's a GET request
    # So display the update.html page
    return render_template('update.html', post=post)


@app.route('/like/<int:post_id>', methods=['POST'])
def like(post_id):
    for post in blog_post:
        if post['id'] == post_id:
            if 'likes' in post:
                post['likes'] += 1
            else:
                post['likes'] = 1
            break
    return redirect('/')


if __name__ == '__main__':
    app.run()
