from controllers.utils import Utils
from controllers.core_functions.hr import Core_Hr

utils = Utils ()
pp = utils.pretty_print
throw = utils.throw

class Skills_Distribution:
    def __init__(self,dbms, object):
        self.core_hr = Core_Hr (dbms)
        self.designation = self.core_hr.get_list ("Designation", fetch_linked_tables=True)
        self.skills = self.core_hr.get_list ("Skills")

    @classmethod
    def dashboard(cls, dbms, object):
        cls = cls(dbms,object)
        return utils.respond(utils.ok, {
            "skills_vs_job_requirements": cls.skills_vs_job_requirements (),
            "employee_turn_over": cls.employee_turn_over (),
            "skill_category": cls.skill_category (),
            "skill_proficient": cls.skill_proficient (),
            "skill_performance": cls.skill_performance (),
            "skill_department": cls.skill_department (),
        })

    def skills_vs_job_requirements (self):
        return_data = []

        return return_data

    def employee_turn_over (self):
        return_data = []
        return return_data

    def skill_category (self):
        return_data = []
        return return_data

    def skill_proficient (self):
        return_data = []
        return return_data

    def skill_performance (self):
        return_data = []
        return return_data

    def skill_department (self):
        return_data = []
        return return_data
