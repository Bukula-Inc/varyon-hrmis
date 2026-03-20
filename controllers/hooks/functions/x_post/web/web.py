from controllers.utils import Utils
from controllers.mailing import Mailing
from controllers.mailing.templates.default_template import Default_Template
utils = Utils()
pp = utils.pretty_print
throw = utils.throw

def submit_enquiry_from_web(dbms, object):
    body = object.body.data
    mailing = Mailing(dbms, object)
    message = f"""
        <div style="min-height:100vh">
            <div class="font-bold">FROM: {body.name}</div>
            <div class="font-bold">Mail Type: Enquiry</div>
            <div style="width:100%;border-top:1px gray solid"></div>
            {body.message}
        </div>
    """
    body.organization_or_individual = body.name
    body.status = "Open"
    del body.name
    save = dbms.create("Enquiry",body, privilege=True)
    mailing = mailing.send_mail("info@startappsolutions.com", "Enquiry From Web", Default_Template.template(message, "Enquiry From Web"))
    return save



def validate_kyc(dbms, object):
    # core = Core_Accounting(dbms,object.user,object)
    # validate = core.validate_customer()
    # if validate.status == utils.found:
    #     throw(validate.error_message)
    # return utils.respond(utils.ok, "Validation passed")
    pass

def get_job_opening(dbms, object):
    name = object.body.data.name
    opportunity = dbms.get_doc("Job_Advertisement", name, privilege=True)
    get_hr_settings = dbms.get_doc("Hr_Setting", name=object.user_current_company, privilege=True)
    if opportunity.status == utils.ok and opportunity.data:
        jo = opportunity.data
        lower = f"{jo.lower_range} {jo.currency}" if jo.lower_range else ''
        upper = f"{jo.upper_range} {jo.currency}" if jo.upper_range else ''
        jo.upper_range = upper
        jo.lower_range = lower
        return utils.respond(utils.ok, jo)

    return utils.respond(utils.ok, opportunity.data)
