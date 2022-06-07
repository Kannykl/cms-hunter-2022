from django.urls import path
from . import views


urlpatterns = [
    path('scan', views.WebSiteScanView.as_view(), name='scan'),
    path('', views.ScanListView.as_view(), name='list_hosts'),
    path('scan/<int:pk>', views.DeleteScanView.as_view(), name='delete_scan'),
    path('vulnerabilities', views.VulnerabilitiesListView.as_view(), name='list_vulnerabilities'),
    path('cms/<int:pk>/', views.VulnerabilityScanView.as_view(), name="vulnerability_scan"),
]
