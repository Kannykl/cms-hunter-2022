from config.celery import app
from .models import Scanning, Report, Status
from .services import run_what_web, check_site_for_vulnerabilities


@app.task(name='scanner_website')
def scanner_task(scan_id: int, proxy: str) -> None:
    """Starts whatweb scanning task.

    Args:
        scan_id: Task id.
        proxy: Whatweb proxy.

    Returns:
        None
    """
    scan = Scanning.objects.get(id=scan_id)

    try:
        result = run_what_web(scan.hostname, proxy)
        scan.ip = result[0]
        scan.cms = result[1]
        scan.webserver = result[2]
        scan.country = result[3]
        scan.status = Status.STATUS_SUCCESS

    except Exception as e:
        scan.status = Status.STATUS_ERROR
        scan.message = str(e)[:110]

    scan.save()


@app.task(name='vulnerability_scan', bind=True)
def vulnerability_task(self, report_id: int, hostname: str, cms: str) -> None:
    report = Report.objects.get(id=report_id)
    try:
        path_to_file = check_site_for_vulnerabilities(hostname, cms)
        report.file = path_to_file
        report.status = Status.STATUS_SUCCESS

    except Exception as e:
        report.status = Status.STATUS_ERROR
        report.message = str(e)[:110]

    report.save()

