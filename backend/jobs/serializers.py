
from rest_framework import serializers

from .models import Job


class JobSerializer(serializers.ModelSerializer):
    assigned_to = serializers.CharField(
        source="assigned_to.username",
        read_only=True,
    )

    class Meta:
        model = Job
        fields = [
            "id",
            "title",
            "description",
            "assigned_to",
            "status",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "assigned_to",
            "status",
            "created_at",
            "updated_at",
        ]
