
from rest_framework import serializers

from .models import JobAssignment


class JobSerializer(serializers.ModelSerializer):
    job_id = serializers.IntegerField(source="job.id", read_only=True)
    title = serializers.CharField(source="job.title", read_only=True)
    description = serializers.CharField(
        source="job.description",
        read_only=True,
    )
    assigned_to = serializers.CharField(
        source="helper.username",
        read_only=True,
    )

    class Meta:
        model = JobAssignment
        fields = [
            "id",
            "job_id",
            "title",
            "description",
            "assigned_to",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "job_id",
            "title",
            "description",
            "assigned_to",
            "status",
            "created_at",
            "updated_at",
        ]
