from controllers.utils.dates import Dates
from controllers.utils import Utils
from controllers.utils.object_generator import Generate_Object, Extract_Object


utils = Utils()
dates = Dates()
pp = utils.pretty_print
throw = utils.throw

# before submitting an appraisal form
# def before_appraisal_360_Degree_update(dbms, object):
#     ext = Extract_Object(object.body).extracted
#     # utils.throw("hihi")


# before submitting an appraisal setup
def before_self_appraisal_setup_submit(dbms, object):
   pass