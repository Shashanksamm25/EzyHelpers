
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import JobAssignment
from .serializers import JobSerializer


class AssignedJobsView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = JobSerializer

    def get_queryset(self):
        return (
            JobAssignment.objects
            .filter(helper=self.request.user)
            .select_related("job", "helper")
            .order_by("-created_at")
        )


class JobDetailView(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = JobSerializer

    def get_queryset(self):
        return (
            JobAssignment.objects
            .filter(helper=self.request.user)
            .select_related("job", "helper")
        )


class UpdateJobStatusView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        assignment = get_object_or_404(
            JobAssignment.objects.select_related("job", "helper"),
            pk=pk,
            helper=request.user,
        )

        new_status = request.data.get("status")

        allowed_transitions = {
            JobAssignment.Status.ASSIGNED: JobAssignment.Status.IN_PROGRESS,
            JobAssignment.Status.IN_PROGRESS: JobAssignment.Status.COMPLETED,
        }

        expected_status = allowed_transitions.get(assignment.status)

        if expected_status is None:
            raise ValidationError({
                "status": "This assignment cannot be changed further."
            })

        if new_status != expected_status:
            raise ValidationError({
                "status": (
                    f"Invalid transition. The next status must be "
                    f"{expected_status}."
                )
            })

        assignment.status = new_status
        assignment.save(update_fields=["status", "updated_at"])

        return Response(
            JobSerializer(assignment).data,
            status=status.HTTP_200_OK,
        )
