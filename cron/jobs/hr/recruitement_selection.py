from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.tenant import Tenant_Controller
from controllers.mailing import Mailing


utils = Utils()
date = Dates()
tc = Tenant_Controller()


utils = Utils ()
pp = utils.pretty_print
dates = Dates ()

class Recruitment_Selection_Controller:
    def __init__(self) -> None:
        self.dbms = tc.get_admin_dbms()
    
    @classmethod
    def init_interview_reminders (cls):
        cls.__init__ (cls)
        bj = tc.get_background_job_content("Recruitment And Selection")
        if bj.get("status") == utils.ok:
            data = bj.get("data")
            if data.status.lower() == "idle":
                # update = tc.update_background_job_status("Recruitment And Selection", "Running")
                # print(update)
                # if update.get("status"):
                    tenants = tc.get_tenants ()
                    if tenants.get("status") == utils.ok:
                        for tenant in tenants.get("data"):
                            con = tc.connect_tenant (tenant_url=tenant.tenant_url)
                            get_all_schedules = con.get_list ("Interview_Schedule", filters={"schedule__range": [dates.today (), dates.add_days (dates.today (), 4)]}, privilege=True, skip_user_evaluation=True)
                            if utils.checker (get_all_schedules, is_list=True):
                                mailing = Mailing (dbms=con)
                                for schedule in get_all_schedules:
                                    get_application = con.get_doc ("Job_Application", schedule.application, privilege=True, skip_user_evaluation=True)
                                    job_opening = get_application.linked_fields.job_opening
                                    designation = get_application.linked_fields.designation
                                    if get_application:
                                        dti = date.calculate_days (dates.today (), schedule.schedule)
                                        if dti > 0:
                                            days = f"{dti}days"
                                        else:
                                            days = "today"

                                        msg = f"""
                                                <h3>Hello {get_application.applicant_name},</h3>
                                                <p>
                                                    We are Please to remind You that your Scheduled Interview for {schedule.schedule} date 
                                                    time from {schedule.from_time} to {schedule.to_time} is almost here. Job Title 
                                                    <u><b>{designation.name}</b></u> at {job_opening.company}.
                                                </p>
                                                <p>
                                                    Hope this reminder found you i high spirit and read for you interview which is in {days}
                                                </p>
                                            """
                                        sent = mailing.send_mail (recipient=get_application.email, subject="Interview Schedule", body=msg)
                                        # pp (sent)
