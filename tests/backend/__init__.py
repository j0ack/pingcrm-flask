import json
import unittest
from typing import Any, Dict

from bs4 import BeautifulSoup

from app import create_app, db


class PingCrmTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("test")
        self.client = self.app.test_client()
        with self.app.test_request_context():
            db.create_all()

    def get_response_data(self, html: str) -> Dict[str, Any]:
        soup = BeautifulSoup(html, features="html.parser")
        root = soup.find(id="app")
        return json.loads(root.get("data-page"))
