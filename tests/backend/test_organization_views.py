from datetime import datetime

from app import db
from app.factories import OrganizationFactory
from app.models.organization import Organization
from tests.backend import PingCrmTestCase


class TestOrganizationViews(PingCrmTestCase):
    """Test organization related views."""

    def setUp(self):
        super().setUp()
        with self.app.test_request_context():
            organization = OrganizationFactory(name="Acme")

            db.session.add(organization)
            db.session.commit()

            self.organization_id = organization.id

    def tearDown(self):
        with self.app.test_request_context():
            Organization.query.delete()
            db.session.commit()

    def test_search(self):
        with self.app.test_request_context():
            response = self.client.get("/organizations/")
            data = response.inertia("app")
            self.assertEqual(len(data.props.organizations.data), 1)
            self.assertEqual(data.props.organizations.data[0].name, "Acme")
            self.assertEqual(data.component, "organizations/Search")

            args = {"trashed": "only"}
            response = self.client.get("/organizations/", query_string=args)
            data = response.inertia("app")
            self.assertEqual(len(data.props.organizations.data), 0)

    def test_create_organization(self):
        with self.app.test_request_context():
            response = self.client.post(
                "/organizations/create/",
                json={
                    "name": "Test",
                },
            )
            data = response.inertia("app")
            self.assertEqual(Organization.query.count(), 2)

            organization = Organization.query.get(data.props.organization.id)
            self.assertEqual(organization.name, "Test")
            self.assertEqual(data.props.organization.name, "Test")

    def test_create_missing_fields(self):
        with self.app.test_request_context():
            response = self.client.post(
                "/organizations/create/",
                json={
                    "name": "",
                },
            )
            data = response.inertia("app")
            self.assertTrue(hasattr(data.props.errors, "name"))
            self.assertEqual(Organization.query.count(), 1)

    def test_edit_organization(self):
        with self.app.test_request_context():
            response = self.client.put(
                f"/organizations/{self.organization_id}/edit/",
                json={
                    "name": "Test 2",
                    "email": "test@test.io",
                },
            )
            data = response.inertia("app")
            organization = Organization.query.get(data.props.organization.id)
            self.assertEqual(data.props.organization.id, self.organization_id)
            self.assertEqual(organization.name, "Test 2")
            self.assertEqual(data.props.organization.name, "Test 2")
            self.assertEqual(organization.email, "test@test.io")
            self.assertEqual(data.props.organization.email, "test@test.io")

    def test_edit_missing_fields(self):
        with self.app.test_request_context():
            response = self.client.put(
                f"/organizations/{self.organization_id}/edit/",
                json={
                    "email": "test@test.io",
                },
            )
            data = response.inertia("app")
            organization = Organization.query.get(self.organization_id)
            self.assertTrue(hasattr(data.props.errors, "name"))
            self.assertNotEqual(organization.email, "test@test.io")

    def test_delete_organization(self):
        with self.app.test_request_context():
            response = self.client.delete(
                f"/organizations/{self.organization_id}/delete/",
                follow_redirects=True,
            )
            organization = Organization.query.get(self.organization_id)
            data = response.inertia("app")
            self.assertIsNotNone(organization.deleted_at)
            self.assertIsNotNone(data.props.organization.deleted_at)

    def test_restore_organization(self):
        with self.app.test_request_context():
            organization = Organization.query.get(self.organization_id)
            organization.deleted_at = datetime.now()
            db.session.commit()

            self.assertIsNotNone(organization.deleted_at)
            response = self.client.put(
                f"/organizations/{self.organization_id}/restore/",
                follow_redirects=True,
            )
            db.session.refresh(organization)
            data = response.inertia("app")
            self.assertIsNone(organization.deleted_at)
            self.assertIsNone(data.props.organization.deleted_at)
