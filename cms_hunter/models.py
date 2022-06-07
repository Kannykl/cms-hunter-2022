from django.contrib.auth.models import UserManager
from django.db import models
from django.contrib.auth.models import User


class Status:
    STATUS_PENDING = 'PENDING'
    STATUS_ERROR = 'ERROR'
    STATUS_SUCCESS = 'SUCCESS'
    STATUSES = (
        (STATUS_PENDING, 'Pending'),
        (STATUS_ERROR, 'Error'),
        (STATUS_SUCCESS, 'Success'),
    )


class CMS(models.Model):
    vulnerability = models.CharField(max_length=100, default="")
    github_repository = models.CharField(max_length=100, default="")

    objects = UserManager()

    def get_absolute_url(self):
        return "/"


class Scanning(models.Model):
    """Information about scanning website"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scan_users', default="")

    hostname = models.CharField(max_length=100, default="")
    cms = models.CharField(max_length=50, default="")
    webserver = models.CharField(max_length=50, default="")
    country = models.CharField(max_length=50, default="")
    ip = models.CharField(max_length=50, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=8, choices=Status.STATUSES)
    message = models.CharField(max_length=110, blank=True)

    def __str__(self):
        return self.hostname


class Report(models.Model):
    """Report about found vulnerabilities."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='report_users', default="")

    hostname = models.CharField(max_length=100, default="")
    file = models.FileField(db_index=True)
    upload_time = models.DateTimeField(auto_now_add=True)

    message = models.CharField(max_length=110, blank=True)
    status = models.CharField(max_length=8, choices=Status.STATUSES)

    def __str__(self):
        return self.hostname


