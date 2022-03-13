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
                id=1,
                first_name="john",
                last_name="doe",
                owner=True,
                email="john@doe.com",
            )
            self.user.set_password("test")
            self.account = Account(name="account")
            self.user.account = self.account

            self.second_user = User(
                id=2,
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

    def test_edit(self):
        with self.app.test_request_context():
            response = self.client.put(
                "/users/1/edit/",
                content_type="multipart/form-data",
                data={
                    "first_name": "Test 1",
                    "last_name": "Test 2",
                    "email": "test@test.com",
                },
            )
            data = self.get_response_data(response.data)
            self.assertEqual(data["props"]["user"]["first_name"], "Test 1")
            self.assertEqual(data["props"]["user"]["last_name"], "Test 2")
            self.assertEqual(data["props"]["user"]["email"], "test@test.com")
            self.assertNotIn("password", data["props"]["user"])

    def test_edit_password(self):
        with self.app.test_request_context():
            response = self.client.put(
                "/users/1/edit/",
                content_type="multipart/form-data",
                data={
                    "password": "foobar",
                },
            )
            data = self.get_response_data(response.data)
            user = User.query.get(data["props"]["user"]["id"])
            self.assertTrue(user.check_password("foobar"))

    def test_edit_add_photo(self):
        with self.app.test_request_context():
            response = self.client.put(
                "/users/1/edit/",
                content_type="multipart/form-data",
                data={
                    "photo": (BytesIO(b"abcdef"), "test.jpg"),
                },
            )
            data = self.get_response_data(response.data)
            user = User.query.get(data["props"]["user"]["id"])
            self.assertIsNotNone(user.photo_path)
            self.assertTrue(user.check_password("test"))

    def test_edit_missing_fields(self):
        with self.app.test_request_context():
            response = self.client.put(
                "/users/1/edit/",
                content_type="multipart/form-data",
                data={
                    "first_name": "",
                },
            )
            data = self.get_response_data(response.data)
            self.assertIn("first_name", data["props"]["errors"])

            response = self.client.put(
                "/users/1/edit/",
                content_type="multipart/form-data",
                data={
                    "last_name": "",
                },
            )
            data = self.get_response_data(response.data)
            self.assertIn("last_name", data["props"]["errors"])

    def test_edit_not_found_user(self):
        with self.app.test_request_context():
            response = self.client.put(
                "/users/9999/edit/",
                content_type="multipart/form-data",
                data={
                    "first_name": "John",
                },
            )
            self.assertEqual(response.status_code, 404)

    def test_restore_user(self):
        with self.app.test_request_context():
            response = self.client.put("/users/2/restore/", follow_redirects=True)
            user = User.query.get(2)
            data = self.get_response_data(response.data)
            self.assertIsNone(user.deleted_at)
            self.assertIsNone(data["props"]["user"]["deleted_at"])
            self.assertEqual(data["component"], "users/Edit")

    def test_restore_user_not_found(self):
        with self.app.test_request_context():
            response = self.client.put("/users/9999/restore/", follow_redirects=True)
            self.assertEqual(response.status_code, 404)

    def test_delete(self):
        with self.app.test_request_context():
            response = self.client.delete("/users/1/delete/", follow_redirects=True)
            user = User.query.get(2)
            data = self.get_response_data(response.data)
            self.assertIsNotNone(user.deleted_at)
            self.assertIsNotNone(data["props"]["user"]["deleted_at"])

    def test_delete_user_not_found(self):
        with self.app.test_request_context():
            response = self.client.delete(
                "/users/9999/delete/", follow_redirects=True
            )
            self.assertEqual(response.status_code, 404)
