from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DeleteView
from .models import Scanning, Report, Status
from .forms import VulnerabilityScanForm, ScanForm
from . import services
from .tasks import scanner_task, vulnerability_task


class ScanListView(LoginRequiredMixin, ListView):
    """Page displays crawled hosts."""

    model = Scanning
    template_name = "cms_hunter/scans.html"
    context_object_name = "scan_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['scan_list'] = Scanning.objects.filter(user=self.request.user)
        return context


class WebSiteScanView(LoginRequiredMixin, View):
    """The page displays a form to crawl the site on CMS."""

    def get(self, request, *args, **kwargs):
        form = ScanForm(request.POST or None)
        context = {"form": form}

        return render(request, "cms_hunter/scanner.html", context)

    def post(self, request, *args, **kwargs):
        form = ScanForm(request.POST or None)
        proxy: tuple = ()

        if form.is_valid():
            if 'proxy_server' in request.POST:
                proxy = services.create_proxy_for_whatweb(request.POST)

            scan = Scanning.objects.create(
                user=request.user,
                hostname=request.POST['hostname'],
                status=Status.STATUS_PENDING,
            )
            scanner_task.delay(scan.id, proxy)

        return HttpResponseRedirect(reverse("list_hosts"))


class VulnerabilityScanView(LoginRequiredMixin, View):
    """The page displays a form to select settings for scanning site for vulnerabilities."""
    def get(self, request, pk, *args, **kwargs):
        scan = Scanning.objects.get(id=pk)
        form = VulnerabilityScanForm(request.POST or None)

        context = {
            "form": form,
            "scan": scan
        }

        return render(request, "cms_hunter/github.html", context)

    def post(self, request, pk, *args, **kwargs):
        form = VulnerabilityScanForm(request.POST or None)
        scan = Scanning.objects.get(id=pk)

        if form.is_valid():
            report = Report.objects.create(
                hostname=scan.hostname,
                status=Status.STATUS_PENDING,
            )

            vulnerability_task.delay(report.id, scan.hostname, request.POST['cms'])

        return HttpResponseRedirect(reverse("list_vulnerabilities"))


class VulnerabilitiesListView(LoginRequiredMixin, ListView):
    """Page displays hacked hosts."""

    model = Report
    template_name = "cms_hunter/vulnerabilities.html"
    context_object_name = "report_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['report_list'] = Report.objects.filter(user=self.request.user)
        return context


# class DeleteScanView(LoginRequiredMixin, DeleteView):
#     model = Scanning
#     success_url = ""