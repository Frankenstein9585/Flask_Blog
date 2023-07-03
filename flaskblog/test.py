import json

from flaskblog import db, app
from flaskblog.models import Post

with app.app_context():
    with open('posts.json', 'r') as file:
        data = json.load(file)

    for post_dict in data:
        post = Post()
        for key, value in post_dict.items():
            setattr(post, key, value)
        db.session.add(post)
        db.session.commit()
