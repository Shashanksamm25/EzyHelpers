
from django.conf import settings
from django.db import models


class Job(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class JobAssignment(models.Model):
    class Status(models.TextChoices):
        ASSIGNED = "ASSIGNED", "Assigned"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        COMPLETED = "COMPLETED", "Completed"

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="assignments",
    )
    helper = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="job_assignments",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ASSIGNED,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["job", "helper"],
                name="unique_helper_per_job",
            )
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.job.title} - {self.helper.username} - {self.status}"
