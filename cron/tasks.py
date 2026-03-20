# PERIODIC JOBSD DEFINED HERE. DO NOT PUT YOUR CUSTOM CODE.
from celery import shared_task
from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.tenant import Tenant_Controller
from cron import *
import time
utils = Utils()
dates = Dates()
pp = utils.pretty_print
reusable_dbs = {}
from django.db import close_old_connections

def execute_task(task, dbms, tc,freq, service, all_tenants=[]):
    # close_old_connections()
    if task.get("method") and task.get("service") and callable(task.get("method")) and isinstance(task.get("service"), str):
        try:
            if all_tenants:
                return task.get("method")(dbms, tc=tc, all_tenants=all_tenants)
            return task.get("method")(dbms, tc=tc)
        except Exception as e:
            return utils.respond(utils.internal_server_error, f"Fatal error occurred:{str(e)}")
    return utils.respond(utils.unprocessable_entity, f"Failed to fetch background service: {service.error_message}")

def evaluate_tenant(tc, task, tenant):
    if task.get("execute_only_for_main_instance") == True and tc.admin_db_name != tenant.db_name:
        return False
    return True


def initialize_tasks(tasks, every="Minute"):
    try:
        if tasks and len(tasks) > 0:
            utils.pretty_print(f"{every} TASKS EXECUTING")
            tc = Tenant_Controller()
            job_content = tc.get_background_jobs(filters={"name__in":utils.get_list_of_dicts_column_field(tasks,"service")})
            if job_content.status != utils.ok:
                pp(f"Failed to fetch background jobs:{job_content.error_message}")
                return job_content
            jobs = job_content.data
            tenants = tc.get_tenants()
            if tenants.status != utils.ok:
                pp(f"Failed to fetch tenants:{tenants.error_message}")
                return tenants
            for task in tasks:
                # update task status
                service_data = jobs.get(task.get("service").lower())
                if service_data.status in ["Idle"]:
                    update = tc.update_background_job_status(service_data.name, "Running")
                    res = utils.from_dict_to_object({ 
                        "task_name": task.get("method").__name__, 
                        "module": service_data.module,
                        "service_name": service_data.name,
                        "status" : "Completed", 
                        "error_message": "",  "result": "",
                        "execution_frequency": every
                    })
                    start_time = time.time()
                    if update:
                        for tnt in tenants.data:
                            if tnt.status.lower() not in ["initialized", "suspended", "expired", "deleted"]:
                                if evaluate_tenant(tc, task, tnt):
                                    try:
                                        dbms = reusable_dbs.get(tnt.db_name)
                                        if not dbms:
                                            try:
                                                dbms = tc.connect_tenant(tnt.db_name)
                                            except Exception as e:
                                                pp(f"ERROR OCCURRED WHILE SETTING UP DBMS:{str(e)}")
                                                dbms = None
                                        if dbms:
                                            reusable_dbs[f"{tnt.db_name}"] = dbms
                                            try:
                                                pass
                                                result = execute_task(task, dbms, tc, "Every Minute",task.get("service"), tenants if task.get("pass_all_tenants") else [])
                                                if result:
                                                    res.result = f"{result}"
                                            except Exception as e:
                                                res.status = "Failed"
                                                res.error_message = f"{str(e)}"
                                        else:
                                            pp(f"Tenant evaluation failed to configure dbms for {tnt.db_name}")
                                        end_time = time.time()
                                        exec_time = end_time - start_time
                                        res.execution_time = dates.convert_seconds_to_time(exec_time)
                                        res.name = f"{res.task_name}-{dates.timestamp()}"
                                        res.for_tenant = tnt.name
                                        # pp(res)
                                        result = tc.dbms.create("Background_Job_Results", res, privilege=True)
                                    except Exception as e:
                                        pp(f"::::{str(e)}")
                        update = tc.update_background_job_status(service_data.name, "Idle")
                    else:
                        pp("Service Status not known")
                else:
                    pp(f"Skipping task:{service_data.name}")
    except Exception as e:
        pp(f"An error occurred while processing background Job: {str(e)}")

# all tasks, defined here
@shared_task
def one_minute_tasks():
    return initialize_tasks(one_minute, "One Minute")


@shared_task
def five_minute_tasks():
    return initialize_tasks(five_minutes, "Five Minutes")

@shared_task
def ten_minute_tasks():
    return initialize_tasks(ten_minutes, "Ten Minutes")

@shared_task
def thirty_minute_tasks():
    return initialize_tasks(thirty_minutes, "Thirty Minutes")


@shared_task
def one_hour_tasks():
    return initialize_tasks(one_hour, "One Hour")


@shared_task
def one_day_tasks():
    return initialize_tasks(one_day, "One Day")


@shared_task
def one_month_tasks():
    return initialize_tasks(one_month, "One Month")


@shared_task
def one_year_tasks():
    return initialize_tasks(one_year, "One Year")