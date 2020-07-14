from unittest import TestCase

from app import app
from models import db, User, Post

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class BloglyTests(TestCase):
    def setUp(self):
        """Add sample user."""
        Post.query.delete()
        User.query.delete()


        user = User(first_name="FirstName", last_name="LastName", image_url="")
        db.session.add(user)
        db.session.commit()
        post = Post(title="title", content="content", user_id=user.id)
        db.session.add(post)
        db.session.commit()
        self.user_id = user.id
        self.post_id = post.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()



    def test_users(self):
        with app.test_client() as client:
            print(self.user_id)
            resp = client.get("/users")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Add User', html)

    def test_add_user(self):
        with app.test_client() as client:
            resp = client.get("/users/new")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('First Name', html)

    def test_user_detail(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Edit', html)


    def test_user_edit(self):
        with app.test_client() as client:

            resp = client.get(f"/users/{self.user_id}/edit")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('First Name', html)

    def test_delete(self):
        with app.test_client() as client:

            resp = client.post(f"/users/{self.user_id}/delete")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 302)


    def test_new_post(self):
        with app.test_client() as client:
    # post = Post.query.get_or_404(post_id)
    # user = User.query.get_or_404(post.user_id)
            resp = client.get(f"/users/{self.user_id}/posts/new")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)

    def test_read_post(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)

    def test_edit_post(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}/edit")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)

    def test_delete_post(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.user_id}/delete")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 302)


