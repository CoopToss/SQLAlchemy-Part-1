import unittest
from app import app, db, User

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.assertEqual(app.debug, False)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/testdb'
        app.config['TESTING'] = True

        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_add_user(self):
        response = self.app.post('/users/new', data=dict(
            first_name='John',
            last_name='Doe',
            image_url='john.jpg'
        ), follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'John Doe', response.data)

    def test_user_detail(self):
        user = User(first_name='Jane', last_name='Doe', image_url='jane.jpg')
        with app.app_context():
            db.session.add(user)
            db.session.commit()

        response = self.app.get(f'/users/{user.id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Jane Doe', response.data)

    def test_edit_user(self):
        user = User(first_name='Jane', last_name='Doe', image_url='jane.jpg')
        with app.app_context():
            db.session.add(user)
            db.session.commit()

        response = self.app.post(f'/users/{user.id}/edit', data=dict(
            first_name='Jane Edited',
            last_name='Doe Edited',
            image_url='jane_edited.jpg'
        ), follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Jane Edited Doe Edited', response.data)

    def test_delete_user(self):
        user = User(first_name='Jane', last_name='Doe', image_url='jane.jpg')
        with app.app_context():
            db.session.add(user)
            db.session.commit()

        response = self.app.post(f'/users/{user.id}/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Jane Doe', response.data)

if __name__ == '__main__':
    unittest.main()
