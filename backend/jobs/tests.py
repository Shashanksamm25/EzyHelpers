
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Job


User = get_user_model()


class JobAPITests(APITestCase):
    def setUp(self):
        self.helper1 = User.objects.create_user(
            username="helper1",
            password="Demo@123",
        )

        self.helper2 = User.objects.create_user(
            username="helper2",
            password="Demo@456",
        )

        self.job1 = Job.objects.create(
            title="Home Cleaning",
            description="Clean the living room and kitchen",
            assigned_to=self.helper1,
            status=Job.Status.ASSIGNED,
        )

        self.job2 = Job.objects.create(
            title="Office Maintenance",
            description="Inspect office equipment",
            assigned_to=self.helper2,
            status=Job.Status.ASSIGNED,
        )

    def test_helper_can_only_see_own_jobs(self):
        self.client.force_authenticate(user=self.helper1)

        response = self.client.get("/api/jobs/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        returned_ids = {job["id"] for job in response.data}
        self.assertEqual(returned_ids, {self.job1.id})

    def test_helper_cannot_access_another_helpers_job(self):
        self.client.force_authenticate(user=self.helper1)

        response = self.client.get(
            f"/api/jobs/{self.job2.id}/"
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_valid_status_transition(self):
        self.client.force_authenticate(user=self.helper1)

        response = self.client.patch(
            f"/api/jobs/{self.job1.id}/status/",
            {"status": "IN_PROGRESS"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.job1.refresh_from_db()
        self.assertEqual(
            self.job1.status,
            Job.Status.IN_PROGRESS,
        )

    def test_invalid_status_transition_is_rejected(self):
        self.client.force_authenticate(user=self.helper1)

        response = self.client.patch(
            f"/api/jobs/{self.job1.id}/status/",
            {"status": "COMPLETED"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.job1.refresh_from_db()
        self.assertEqual(
            self.job1.status,
            Job.Status.ASSIGNED,
        )
