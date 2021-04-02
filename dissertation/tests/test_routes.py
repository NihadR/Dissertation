# import flask 
# import dissertation
# import dissertation.users.utils as util
# import dissertation.users.routes as uroutes
# import unittest

# from dissertation import create_app, db
# import pytest
# app = dissertation.create_app()



# class FlaskTestCase(unittest.TestCase):
#     '''
#     Test routes in application, routes which require login to access
#     check for 302 status codes
#     '''

#     # def test_home(self):
#     #     tester = app.test_client(self)
#     #     response = tester.get('/', content_type = 'html/text')
#     #     self.assertEqual(response.status_code, 200)
    
#     def test_about(self):
#         tester = app.test_client(self)
#         response = tester.get('/about', content_type = 'html/text')
#         self.assertEqual(response.status_code, 200)

#     def test_reset_request(self):
#         tester = app.test_client(self)
#         response = tester.get('/reset_password', content_type = 'html/text')
#         self.assertEqual(response.status_code, 200)

#     def test_info(self):
#         tester = app.test_client(self)
#         response = tester.get('/info', content_type = 'html/text')
#         self.assertEqual(response.status_code, 200)

#     def test_compiler(self):
#         tester = app.test_client(self)
#         response = tester.get('/compiler', content_type = 'html/text')
#         self.assertEqual(response.status_code, 200)


#     def test_dashboard(self):
#         tester = app.test_client(self)
#         response = tester.get('/dashboard', content_type = 'html/text')
#         self.assertEqual(response.status_code, 302)

#     def test_learning_style(self):
#         tester = app.test_client(self)
#         response = tester.get('/learning_style', content_type = 'html/text')
#         self.assertEqual(response.status_code, 302)

#     def test_pretest(self):
#         tester = app.test_client(self)
#         response = tester.get('/pretest', content_type = 'html/text')
#         self.assertEqual(response.status_code, 302)

#     def test_account(self):
#         tester = app.test_client(self)
#         response = tester.get('/account', content_type = 'html/text')
#         self.assertEqual(response.status_code, 302)
    
#     def test_create_task(self):
#         tester = app.test_client(self)
#         response = tester.get('/create_task', content_type = 'html/text')
#         self.assertEqual(response.status_code, 302)

#     def test_view_topic(self):
#         tester = app.test_client(self)
#         response = tester.get('/view_topics', content_type = 'html/text')
#         self.assertEqual(response.status_code, 302)

#     def test_login(self):
#         tester = app.test_client(self)
#         response = tester.get('/login', content_type = 'html/text')
#         self.assertEqual(response.status_code, 200)