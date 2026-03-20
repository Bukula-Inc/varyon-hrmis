from controllers.utils import Utils
utils = Utils()
pp = utils.pretty_print
throw = utils.throw

class Approver:
    def __init__(self, dbms, object):
        self.dbms = dbms
        self.object = object

    @classmethod
    def get_approvals(cls,dbms, object):
        instance = cls(dbms, object)

        current_user = instance.dbms.current_user.name



        approvals = instance.dbms.get_list("Workflow_Doc", privilege=True)
        return approvals