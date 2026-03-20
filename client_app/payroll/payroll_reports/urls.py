from django.urls import path, include

urlpatterns = [
    path("monthly_attendance/",include ("client_app.payroll.payroll_reports.monthly_attendance.urls"), name='monthly_attendance'),
    path("napsa_report/",include ("client_app.payroll.payroll_reports.napsa_report.urls"), name='napsa_report'),
    path("nhima_report/",include ("client_app.payroll.payroll_reports.nhima_report.urls"), name='nhima_report'),
    path("paye_report/",include ("client_app.payroll.payroll_reports.paye_report.urls"), name='paye_report'),
    path("private_insurance_report/",include ("client_app.payroll.payroll_reports.private_insurance_report.urls"), name='private_insurance_report'),
    path("skills_levy_report/",include ("client_app.payroll.payroll_reports.skills_levy_report.urls"), name='skills_levy_report'),
    path("statutory_report/",include ("client_app.payroll.payroll_reports.statutory_report.urls"), name='statutory_report'),
    path("overtime_report/",include("client_app.payroll.payroll_reports.overtime_report.urls"), name= 'overtime_report'),
    path("advance_report/",include("client_app.payroll.payroll_reports.advance_report.urls"), name= 'advance_report'),
    path("payroll_summary/",include("client_app.payroll.payroll_reports.payroll_summary.urls"), name= 'payroll_summary'),
    path("payroll_payable/",include("client_app.payroll.payroll_reports.payroll_payable.urls"), name= 'payroll_payable'),
    path("imprest_report/",include("client_app.payroll.payroll_reports.imprest_report.urls"), name= 'imprest_report'),
    path("loan_report/",include("client_app.payroll.payroll_reports.loan_report.urls"), name="loan_report"),   
    path("medical_report/",include("client_app.payroll.payroll_reports.medical_report.urls"), name="medical_report"),   
    path("transfer_file/",include("client_app.payroll.payroll_reports.transfer_file.urls"), name= 'transfer_file'),
    path("amendments_report/",include("client_app.payroll.payroll_reports.amendments_report.urls"), name= 'amendments_report'),
]

