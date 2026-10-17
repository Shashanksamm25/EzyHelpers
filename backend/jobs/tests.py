
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Job, JobAssignment


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
        )
        self.job2 = Job.objects.create(
            title="Office Maintenance",
            description="Inspect office equipment",
        )

        self.assignment1 = JobAssignment.objects.create(
            job=self.job1,
            helper=self.helper1,
            status=JobAssignment.Status.ASSIGNED,
        )
        self.assignment2 = JobAssignment.objects.create(
            job=self.job2,
            helper=self.helper2,
            status=JobAssignment.Status.ASSIGNED,
        )

    def test_helper_can_only_see_own_jobs(self):
        self.client.force_authenticate(user=self.helper1)

        response = self.client.get("/api/jobs/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        returned_ids = {item["id"] for item in response.data}
        self.assertEqual(returned_ids, {self.assignment1.id})

    def test_helper_cannot_access_another_helpers_job(self):
        self.client.force_authenticate(user=self.helper1)

        response = self.client.get(
            f"/api/jobs/{self.assignment2.id}/"
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_valid_status_transition(self):
        self.client.force_authenticate(user=self.helper1)

        response = self.client.patch(
            f"/api/jobs/{self.assignment1.id}/status/",
            {"status": "IN_PROGRESS"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assignment1.refresh_from_db()
        self.assertEqual(
            self.assignment1.status,
            JobAssignment.Status.IN_PROGRESS,
        )

    def test_invalid_status_transition_is_rejected(self):
        self.client.force_authenticate(user=self.helper1)

        response = self.client.patch(
            f"/api/jobs/{self.assignment1.id}/status/",
            {"status": "COMPLETED"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assignment1.refresh_from_db()
        self.assertEqual(
            self.assignment1.status,
            JobAssignment.Status.ASSIGNED,
        )

    def test_helpers_have_independent_statuses_for_same_job(self):
        second_assignment = JobAssignment.objects.create(
            job=self.job1,
            helper=self.helper2,
            status=JobAssignment.Status.ASSIGNED,
        )

        self.client.force_authenticate(user=self.helper1)
        response = self.client.patch(
            f"/api/jobs/{self.assignment1.id}/status/",
            {"status": "IN_PROGRESS"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assignment1.refresh_from_db()
        second_assignment.refresh_from_db()

        self.assertEqual(
            self.assignment1.status,
            JobAssignment.Status.IN_PROGRESS,
        )
        self.assertEqual(
            second_assignment.status,
            JobAssignment.Status.ASSIGNED,
        )
