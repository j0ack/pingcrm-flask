import unittest

from flask_inertia.unittest import InertiaTestResponse

from app import create_app, db


class PingCrmTestCase(unittest.TestCase):
    """Ping CRM meta class for unit tests."""

    def setUp(self):
        self.app = create_app("test")
        self.app.response_class = InertiaTestResponse
        self.client = self.app.test_client()
        with self.app.test_request_context():
            db.create_all()
