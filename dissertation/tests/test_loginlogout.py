import os 
import tempfile
import pytest
import dissertation
from dissertation import create_app, db
import pytest
app = dissertation.create_app()

app.config['USERNAME'] = 'nihad1999@hotmail.co.uk'
app.config['PASSWORD'] = 'testing'
# TEST_DB = 'test.db'


# class DB_Tests(unittest.TestCase):

#     def setUp(self):

#     def tearDown(self):
#         pass

@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])

# def test_empty_db(client):
#     """Start with a blank database."""

#     rv = client.get('/')
#     assert b'No entries here so far' in rv.data

def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)

def test_login_logout(client):
    """Make sure login and logout works."""

    rv = login(client, app.config['USERNAME'], app.config['PASSWORD'])
    assert 'Login Successful' in rv.data

    rv = logout(client)
    assert b'You were logged out' in rv.data

    rv = login(client, app.config['USERNAME'] + 'x', app.config['PASSWORD'])
    assert b'Invalid username' in rv.data

    rv = login(client, app.config['USERNAME'], app.config['PASSWORD'] + 'x')
    assert b'Invalid password' in rv.data