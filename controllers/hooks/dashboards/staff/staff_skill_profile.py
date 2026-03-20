from controllers.utils import Utils
utils = Utils ()
pp = utils.pretty_print
class Staff_Skill_Profile:
    def __init__(self, dbms, object) -> None:
        self.dbms = dbms
        self.object = object
        self.sales_person = []
        self.latest_closed_sales = []

    @classmethod
    def skils_docs(cls, dbms, object):
        cls.__init__ (cls, dbms=dbms, object=object)
        return utils.respond (utils.ok, {
            "employee_skill_set": cls.employee_skills(cls),        
        })
    def employee_skills(self):
        emp_skills = self.dbms.get_list("Employee_File", fetch_linked_tables=True, privilege=True)
        skills = {}
        for emp in emp_skills.data.rows:
            for file in emp['files']:
                file_name = file['file_name']
                if file_name not in skills:
                    skills[file_name] = []
                skills[file_name].append({
                    'employee_name': emp['employee_name'],
                    'designation': emp['designation']
                })
        return skills


    