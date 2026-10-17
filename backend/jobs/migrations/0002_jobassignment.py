
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def copy_existing_assignments(apps, schema_editor):
    Job = apps.get_model("jobs", "Job")
    JobAssignment = apps.get_model("jobs", "JobAssignment")
    database = schema_editor.connection.alias

    for job in Job.objects.using(database).all().iterator():
        JobAssignment.objects.using(database).get_or_create(
            job_id=job.pk,
            helper_id=job.assigned_to_id,
            defaults={"status": job.status},
        )


class Migration(migrations.Migration):

    dependencies = [
        ("jobs", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="JobAssignment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("ASSIGNED", "Assigned"),
                            ("IN_PROGRESS", "In Progress"),
                            ("COMPLETED", "Completed"),
                        ],
                        default="ASSIGNED",
                        max_length=20,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "helper",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="job_assignments",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "job",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="assignments",
                        to="jobs.job",
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
                "constraints": [
                    models.UniqueConstraint(
                        fields=("job", "helper"),
                        name="unique_helper_per_job",
                    )
                ],
            },
        ),
        migrations.RunPython(
            copy_existing_assignments,
            migrations.RunPython.noop,
        ),
        migrations.RemoveField(
            model_name="job",
            name="assigned_to",
        ),
        migrations.RemoveField(
            model_name="job",
            name="status",
        ),
    ]
