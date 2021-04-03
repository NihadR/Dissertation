import os 
import tempfile
import pytest
import dissertation
from dissertation import create_app, db
from dissertation import config
import pytest
app = dissertation.create_app()

class TestDB(unittest.TestCase):

    def setUp(self):
        self.app =create_app(config)

        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()