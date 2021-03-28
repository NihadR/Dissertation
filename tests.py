from dissertation import app
import unittest
import pytest


class FlaskTestCase(unittest.TestCase):

    def test_home(self):
        tester = app.test_client(self)
        response = tester.get('/home', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        tester = app.test_client(self)
        response = tester.get('/register', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_dashboard(self):
        tester = app.test_client(self)
        response = tester.get('/dashboard', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_create_task(self):
        tester = app.test_client(self)
        response = tester.get('/home', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_content(self):
        tester = app.test_client(self)
        response = tester.get('/content', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_pretest(self):
        tester = app.test_client(self)
        response = tester.get('/pretest', content_type='html/text')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
