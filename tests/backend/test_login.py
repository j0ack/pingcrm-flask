from app import db
from app.models.account import Account
from app.models.user import User
from tests.backend import PingCrmTestCase


class TestLogin(PingCrmTestCase):
    def setUp(self):
        super().setUp()
        self.app.config["LOGIN_DISABLED"] = False
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
            db.session.add(self.account)
            db.session.add(self.user)
            db.session.commit()

    def tearDown(self):
        with self.app.test_request_context():
            db.session.delete(self.account)
            db.session.delete(self.user)
            db.session.commit()

    def test_login_redirect(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.location)

    def test_login_get(self):
        with self.app.test_request_context():
            response = self.client.get("/login/")
            data = response.inertia("app")
            self.assertEqual(data.component, "Login")
            self.assertTrue(data.url.endswith("/login/"))

    def test_login_successful(self):
        with self.app.test_request_context():
            response = self.client.post(
                "/login/",
                json={
                    "email": "john@doe.com",
                    "password": "test",
                },
                follow_redirects=True,
            )
            data = response.inertia("app")
            self.assertEqual(data.component, "Dashboard")
            self.assertNotEqual({}, data.props.auth)

    def test_login_invalid_password(self):
        with self.app.test_request_context():
            response = self.client.post(
                "/login/",
                json={
                    "email": "john@doe.com",
                    "password": "invalid",
                },
                follow_redirects=True,
            )
            data = response.inertia("app")
            self.assertIn("Invalid email or password", data.props.flash.error)
            self.assertEqual(data.component, "Login")

    def test_login_invalid_email(self):
        with self.app.test_request_context():
            response = self.client.post(
                "/login/",
                json={
                    "email": "doe@john.com",
                    "password": "test",
                },
                follow_redirects=True,
                headers={"X-Inertia": True},
            )
            data = response.inertia("app")
            self.assertIn("Invalid email or password", data.props.flash.error)
            self.assertEqual(data.component, "Login")

    def test_logout(self):
        with self.app.test_request_context():
            response = self.client.post(
                "/login/",
                json={
                    "email": "john@doe.com",
                    "password": "test",
                },
                follow_redirects=True,
            )
            data = response.inertia("app")
            self.assertTrue(hasattr(data.props.auth, "user"))
            response = self.client.post("/logout/", follow_redirects=True)
            data = response.inertia("app")
            self.assertFalse(hasattr(data.props.auth, "user"))
