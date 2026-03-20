from controllers.mailing.templates.hr_email_template import Default_Templates
from controllers.utils.dates import Dates
from controllers.utils import Utils
from controllers.core_functions.hr import Core_Hr

# Initialize utility classes
utils = Utils()
dates = Dates()
throw = utils.throw

# Function to execute before saving an appraisal form
def before_appraisal_setup_save(dbms, object):
    pass

# Function to execute before updating an appraisal form
def before_appraisal_setup_update(dbms, object):
    pass

# Function to execute before submitting an appraisal setup
def before_appraisal_setup_submit(dbms, object):
    core = Core_Hr(dbms=dbms,user=object.user, obj=object)
    setup = object.body
    # Handling for 360 degree Appraisal
    if setup.appraisal_type == "360 degree Appraisal":
        if len(setup.appraisers) > 0:
            generated_forms = core.generate_appraisal_360_form()
    object.doc_status = "Submitted"
        # Handling for self Appraisal
    if setup.appraisal_type == "Self-Rating":
        if len(setup.appraisees) > 0:
            generated_forms = core.generate_self_appraisal_form()
    object.doc_status = "Submitted"


            