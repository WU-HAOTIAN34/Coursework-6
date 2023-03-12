import unittest
from app import db, models
from app import app


# tests login
class TestLogin(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.app_context().push()
        user = models.User.query.filter_by(username='test').first()
        if user:
            db.session.delete(user)
            db.session.commit()
        else:
            user = models.User(username='test', password='123456789', job=0, phone='13315457898', name='Wang')
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        user = models.User.query.filter_by(username='test').first()
        if user:
            db.session.delete(user)
            db.session.commit()

    # test login
    def test_login(self):
        response = self.client.get('/', follow_redirects=True)
        self.assertEqual(200, response.status_code)

    # tests login if required items are empty
    def test_login_empty_required(self):
        response = self.client.post('/', data=dict(username='', password=''))
        received = response.get_data(as_text=True)
        self.assertTrue("Please enter all the required items!" not in received)

    # tests login if username is empty
    def test_login_empty_username(self):
        response = self.client.post('/', data=dict(username='', password='123456789'))
        received = response.get_data(as_text=True)
        self.assertTrue("Please enter all the required items!" not in received)

    # tests login if wrong username
    def test_login_error_username(self):
        response = self.client.post('/', data=dict(username='test123456789', password='123456789'))
        received = response.get_data(as_text=True)
        self.assertTrue("Username or password error!"not in received)

    # tests login if wrong password
    def test_login_error_password(self):
        response = self.client.post('/', data=dict(username='test', password='test123456789'))
        received = response.get_data(as_text=True)
        a = response.get_json()
        print(a)
        self.assertTrue("<div class=\"login layui-anim layui-anim-up\">" in received)

    def test_login_successfully(self):
        response = self.client.post('/', data=dict(username='test', password='123456789'))
        received = response.get_data(as_text=True)
        self.assertTrue("<hr class=\"hr20\" >" in received)


# tests register
class TestRegister(unittest.TestCase):
    # sets up the test client
    def setUp(self):
        self.client = app.test_client()
        app.app_context().push()
        user = models.User.query.filter_by(username='test').first()
        if user:
            db.session.delete(user)
            db.session.commit()
        else:
            user = models.User(username='test', password='123456789')
            db.session.add(user)
            db.session.commit()

    # tears down the test client
    def tearDown(self):
        user = models.User.query.filter_by(username='test').first()
        if user:
            db.session.delete(user)
            db.session.commit()

    def test_register(self):
        response = self.client.get('/register', follow_redirects=True)
        self.assertEqual(200, response.status_code)

    # tests register if required items are empty
    def test_register_empty_required(self):
        response = self.client.post('/register', data=dict(username='', password='', confirm='', name='', phome=''))
        received = response.get_data(as_text=True)
        self.assertTrue("Please enter all the required items!" not in received)

    # tests register if password shorter than required
    def test_register_shorter_than_required(self):
        response = self.client.post('/register', data=dict(username='123456', password='123456', confirm_password='123456'))
        received = response.get_data(as_text=True)
        self.assertTrue("The password should be longer than 6 characters!" not in received)

    # tests register if confirm is different from password
    def test_register_password_different(self):
        response = self.client.post('/register', data=dict(username='123456', password='12345678', confirm='123456789'))
        received = response.get_data(as_text=True)
        self.assertTrue("The passwords entered twice are different!" not in received)

    # tests register if the username exists
    def test_register_username_existing(self):
        response = self.client.post('/register', data=dict(username='test', password='123456789', confirm='123456789'))
        received = response.get_data(as_text=True)

        self.assertTrue("The username already exists!" not in received)


# used to test search function
class TestSearching(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.app_context().push()
        item = models.Item.query.filter_by(item_name='Apple').first()
        if item:
            db.session.delete(item)
            db.session.commit()
        else:
            item = models.Item(item_name='Apple', price=15)
            db.session.add(item)
            db.session.commit()
        user = models.User.query.filter_by(username='test').first()
        if user:
            db.session.delete(user)
            db.session.commit()
        else:
            user = models.User(username='test', password='123456789')
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        item = models.Item.query.filter_by(item_name='Apple').first()
        if item:
            db.session.delete(item)
            db.session.commit()
        user = models.User.query.filter_by(username='test').first()
        if user:
            db.session.delete(user)
            db.session.commit()

    def test_search_result(self):
        response = self.client.post('/', data=dict(username='test', password='123456789'))
        response = self.client.post('/', data=dict(search='Oran'))
        received = response.get_data(as_text=True)
        self.assertTrue("Orange" not in received)


if __name__ == '__main__':
    unittest.main()