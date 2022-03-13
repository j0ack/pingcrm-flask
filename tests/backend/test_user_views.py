from datetime import datetime
from io import BytesIO

from app import db
from app.models.account import Account
from app.models.user import User
from tests.backend import PingCrmTestCase


class TestUserViews(PingCrmTestCase):
    def setUp(self):
        super().setUp()
        with self.app.test_request_context():
            self.user = User(
                first_name="john",
                last_name="doe",
                owner=True,
                email="john@doe.com",
            )
            self.user.set_password("test")
            self.account = Account(name="account")
            self.user.account = self.account

            self.second_user = User(
                first_name="jane",
                last_name="doe",
                owner=False,
                email="jane@doe.com",
                deleted_at=datetime.now(),
            )
            self.second_user.set_password("test")
            self.second_account = Account(name="unknown")
            self.second_user.account = self.second_account

            db.session.add(self.account)
            db.session.add(self.second_account)
            db.session.add(self.user)
            db.session.add(self.second_user)
            db.session.commit()

    def tearDown(self):
        with self.app.test_request_context():
            db.session.delete(self.account)
            db.session.delete(self.second_account)
            db.session.delete(self.user)
            db.session.delete(self.second_user)
            db.session.commit()

    def test_search(self):
        with self.app.test_request_context():
            response = self.client.get("/users/")
            data = self.get_response_data(response.data)
            self.assertEqual(len(data["props"]["users"]["data"]), 1)
            self.assertEqual(data["props"]["users"]["data"][0]["first_name"], "john")
            self.assertEqual(data["component"], "users/Search")

            args = {"trashed": "only"}
            response = self.client.get("/users/", query_string=args)
            data = self.get_response_data(response.data)
            self.assertEqual(len(data["props"]["users"]["data"]), 1)
            self.assertEqual(data["props"]["users"]["data"][0]["first_name"], "jane")
            self.assertEqual(data["component"], "users/Search")

            args = {"role": "owner"}
            response = self.client.get("/users/", query_string=args)
            data = self.get_response_data(response.data)
            self.assertEqual(len(data["props"]["users"]["data"]), 1)
            self.assertEqual(data["props"]["users"]["data"][0]["first_name"], "john")
            self.assertEqual(data["component"], "users/Search")

    def test_create_user(self):
        with self.app.test_request_context():
            response = self.client.post(
                "/users/create/",
                content_type="multipart/form-data",
                data={
                    "first_name": "Test",
                    "last_name": "Doe",
                    "email": "test@doe.com",
                    "password": "test",
                },
            )
            data = self.get_response_data(response.data)
            self.assertEqual(data["props"]["errors"], {})
            self.assertEqual(User.query.count(), 3)

            user = User.query.filter_by(first_name="Test").first()
            self.assertTrue(user.check_password("test"))
            self.assertIsNone(user.photo_path)
            db.session.delete(user)
            db.session.commit()

    def test_create_user_with_photo(self):
        with self.app.test_request_context():
            response = self.client.post(
                "/users/create/",
                content_type="multipart/form-data",
                data={
                    "first_name": "Test",
                    "last_name": "Doe",
                    "email": "test@doe.com",
                    "password": "test",
                    "photo": (BytesIO(b"abcdef"), "test.jpg"),
                },
            )
            data = self.get_response_data(response.data)
            self.assertEqual(data["props"]["errors"], {})
            self.assertEqual(User.query.count(), 3)

            user = User.query.filter_by(first_name="Test").first()
            self.assertTrue(user.check_password("test"))
            self.assertIsNotNone(user.photo_path)
            db.session.delete(user)
            db.session.commit()

    def test_create_missing_fields(self):
        with self.app.test_request_context():
            response = self.client.post(
                "/users/create/",
                content_type="multipart/form-data",
                data={
                    "last_name": "Doe",
                    "email": "test@doe.com",
                    "password": "test",
                },
            )
            data = self.get_response_data(response.data)
            self.assertIn("first_name", data["props"]["errors"])
            self.assertEqual(User.query.count(), 2)

            response = self.client.post(
                "/users/create/",
                content_type="multipart/form-data",
                data={
                    "first_name": "Test",
                    "email": "test@doe.com",
                    "password": "test",
                },
            )
            data = self.get_response_data(response.data)
            self.assertIn("last_name", data["props"]["errors"])
            self.assertEqual(User.query.count(), 2)

            response = self.client.post(
                "/users/create/",
                content_type="multipart/form-data",
                data={
                    "first_name": "Test",
                    "last_name": "Doe",
                    "password": "test",
                },
            )
            data = self.get_response_data(response.data)
            self.assertIn("email", data["props"]["errors"])
            self.assertEqual(User.query.count(), 2)

            response = self.client.post(
                "/users/create/",
                content_type="multipart/form-data",
                data={
                    "first_name": "Test",
                    "last_name": "Doe",
                    "email": "test@doe.com",
                },
            )
            data = self.get_response_data(response.data)
            self.assertIn("password", data["props"]["errors"])
            self.assertEqual(User.query.count(), 2)
