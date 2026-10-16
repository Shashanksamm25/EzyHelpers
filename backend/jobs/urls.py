from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import (
    AssignedJobsView,
    JobDetailView,
    UpdateJobStatusView,
)

urlpatterns = [
    path("auth/login/", obtain_auth_token, name="helper-login"),
    path("jobs/", AssignedJobsView.as_view(), name="assigned-jobs"),
    path("jobs/<int:pk>/", JobDetailView.as_view(), name="job-detail"),
    path(
        "jobs/<int:pk>/status/",
        UpdateJobStatusView.as_view(),
        name="update-job-status",
    ),
]