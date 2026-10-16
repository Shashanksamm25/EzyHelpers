
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404

from .models import Job
from .serializers import JobSerializer


class AssignedJobsView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = JobSerializer

    def get_queryset(self):
        return Job.objects.filter(
            assigned_to=self.request.user
        ).order_by("-created_at")


class JobDetailView(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = JobSerializer

    def get_queryset(self):
        return Job.objects.filter(
            assigned_to=self.request.user
        )


class UpdateJobStatusView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        job = get_object_or_404(
            Job,
            pk=pk,
            assigned_to=request.user,
        )

        new_status = request.data.get("status")

        allowed_transitions = {
            Job.Status.ASSIGNED: Job.Status.IN_PROGRESS,
            Job.Status.IN_PROGRESS: Job.Status.COMPLETED,
        }

        expected_status = allowed_transitions.get(job.status)

        if expected_status is None:
            raise ValidationError({
                "status": "This job cannot be changed further."
            })

        if new_status != expected_status:
            raise ValidationError({
                "status": f"Invalid transition. The next status must be {expected_status}."
            })

        job.status = new_status
        job.save(update_fields=["status", "updated_at"])

        return Response(
            JobSerializer(job).data,
            status=status.HTTP_200_OK,
        )
