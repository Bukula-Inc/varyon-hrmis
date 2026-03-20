from controllers.utils import Utils
utils = Utils()
pp = utils.pretty_print
def short_list(dbms, object):
    filters =object.filters
    fetch_short_listed = dbms.get_list("Applicant_Short_List", filters=filters)
    short_list_report = []
    if fetch_short_listed.status == utils.ok:
        df = utils.to_data_frame(fetch_short_listed.data.rows)
        df = df[["applicant", "applicant_email", "contact_no", "job_position", "application_date", "job_advertisement"]]
        df = df.rename(columns={
            # "job_advertisement": 'Job Advertisement' or "",
            "applicant": "Applicant Name",
            "applicant_email": "Email",
            "contact_no": "Contact Number",
            "job_position": "Job Position",
            "application_date": "Application Date",
            "job_advertisement": "Job Advertisement",
        })

        for index, row in df.iterrows():
            report_entry = {
                # "job_advertisement": row['Job Advertisement'] or "",
                "date_of_application": row['Application Date'],
                "applicant": row['Applicant Name'],
                "applicant_email": row['Email'],
                "applicant_mobile_no": row['Contact Number'],
                "job_position": row['Job Position'],
                "job_advertisement": row['Job Advertisement'],
            }
            short_list_report.append(report_entry)

        pp(short_list_report)
    return utils.respond(utils.ok, {"rows": short_list_report})