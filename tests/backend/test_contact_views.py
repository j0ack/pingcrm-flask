from datetime import datetime

from app import db
from app.factories import ContactFactory, OrganizationFactory
from app.models.contact import Contact
from app.models.organization import Organization
from tests.backend import PingCrmTestCase


class TestContactViews(PingCrmTestCase):
    """Test contacts related views."""

    def setUp(self):
        super().setUp()
        with self.app.test_request_context():
            organization = OrganizationFactory()
            first_contact = ContactFactory(
                first_name="john",
                organization=organization,
            )
            deleted_contact = ContactFactory(
                first_name="jane",
                organization=organization,
            )
            deleted_contact.deleted_at = datetime.now()

            db.session.add(organization)
            db.session.add(first_contact)
            db.session.add(deleted_contact)
            db.session.commit()

            self.organization_id = organization.id
            self.contact_id = first_contact.id
            self.deleted_id = deleted_contact.id

    def tearDown(self):
        with self.app.test_request_context():
            Contact.query.delete()
            Organization.query.delete()
            db.session.commit()

    def test_search(self):
        with self.app.test_request_context():
            response = self.client.get("/contacts/")
            data = response.inertia("app")
            self.assertEqual(len(data.props.contacts.data), 1)
            self.assertEqual(data.props.contacts.data[0].first_name, "john")
            self.assertEqual(data.component, "contacts/Search")

            args = {"trashed": "only"}
            response = self.client.get("/contacts/", query_string=args)
            data = response.inertia("app")
            self.assertEqual(len(data.props.contacts.data), 1)
            self.assertEqual(data.props.contacts.data[0].first_name, "jane")
            self.assertEqual(data.component, "contacts/Search")

    def test_create_contact(self):
        with self.app.test_request_context():
            response = self.client.post(
                "/contacts/create/",
                json={
                    "first_name": "Test",
                    "last_name": "Doe",
                    "organization_id": self.organization_id,
                },
            )
            data = response.inertia("app")
            self.assertEqual(Contact.query.count(), 3)

            contact = Contact.query.get(data.props.contact.id)
            organization = Organization.query.get(self.organization_id)
            self.assertEqual(contact.organization, organization)
            self.assertTrue(hasattr(data.props, "organizations"))

    def test_create_missing_fields(self):
        with self.app.test_request_context():
            response = self.client.post(
                "/contacts/create/",
                json={
                    "last_name": "Doe",
                    "organization_id": self.organization_id,
                },
            )
            data = response.inertia("app")
            self.assertTrue(hasattr(data.props, "organizations"))
            self.assertTrue(hasattr(data.props.errors, "first_name"))
            self.assertEqual(Contact.query.count(), 2)

    def test_edit_contact(self):
        with self.app.test_request_context():
            response = self.client.put(
                f"/contacts/{self.contact_id}/edit/",
                json={
                    "first_name": "Test 1",
                    "last_name": "Test 2",
                    "organization_id": self.organization_id,
                },
            )
            data = response.inertia("app")
            self.assertTrue(hasattr(data.props, "organizations"))
            self.assertEqual(data.props.contact.first_name, "Test 1")
            self.assertEqual(data.props.contact.last_name, "Test 2")

            contact = Contact.query.get(self.contact_id)
            self.assertEqual(contact.first_name, "Test 1")
            self.assertEqual(contact.last_name, "Test 2")

    def test_edit_missing_fields(self):
        with self.app.test_request_context():
            response = self.client.put(
                f"/contacts/{self.contact_id}/edit/",
                json={
                    "first_name": "",
                },
            )
            data = response.inertia("app")
            self.assertTrue(hasattr(data.props.errors, "first_name"))

    def test_delete_contact(self):
        with self.app.test_request_context():
            response = self.client.delete(
                f"/contacts/{self.contact_id}/delete/", follow_redirects=True
            )
            contact = Contact.query.get(self.contact_id)
            data = response.inertia("app")
            self.assertIsNotNone(contact.deleted_at)
            self.assertIsNotNone(data.props.contact.deleted_at)

    def test_delete_contact_not_found(self):
        with self.app.test_request_context():
            response = self.client.delete(
                "/contacts/99999/delete/", follow_redirects=True
            )
            self.assertEqual(response.status_code, 404)

    def test_restore_contact(self):
        with self.app.test_request_context():
            response = self.client.put(
                f"/contacts/{self.deleted_id}/restore/", follow_redirects=True
            )
            contact = Contact.query.get(self.deleted_id)
            data = response.inertia("app")
            self.assertIsNone(contact.deleted_at)
            self.assertIsNone(data.props.contact.deleted_at)
            self.assertEqual(data.component, "contacts/Edit")

    def test_restore_contact_not_found(self):
        with self.app.test_request_context():
            response = self.client.put(
                "/contacts/99999/restore/", follow_redirects=True
            )
            self.assertEqual(response.status_code, 404)
