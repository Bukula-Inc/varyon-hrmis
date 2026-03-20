from controllers.utils import Utils
from controllers.utils.dates import Dates

utils = Utils()
dates = Dates()
pp = utils.pretty_print
throw = utils.throw


class Accounting_Background_Jobs:
    def __init__(self, dbms=None, tc=None) -> None:
        self.dbms = dbms
        self.tc = tc

    def validate_tax_invoices(self):
        try:
            invoices = self.dbms.get_list("Tax_Invoice",filters ={"status__in":["Unreceipted", "Partially Receipted", "Partially Returned"], "due_date__lt":dates.today()}, fetch_linked_tables=True, privilege=True)
            if invoices.status == utils.ok and len(invoices.data.rows) > 0:
                for inv in invoices.data.rows:
                    if inv.status == "Unreceipted":
                        inv.status = "Overdue"
                    if inv.status == "Partially Receipted":
                        inv.status = "Overdue | Partially Receipted"
                    if inv.status == "Partially Returned":
                        inv.status = "Overdue | Partially Returned"
                    update = self.dbms.update("Tax_Invoice", inv, skip_hooks=True, privilege=True,skip_audit_trail=True)
        except Exception as e:
            pp(str(e))


    def validate_purchase_invoices(self,):
        try:
            invoices = self.dbms.get_list("Purchase_Invoice",filters ={"status__in":["Outstanding", "Outstanding | Pending GRN", "Partially Returned","Partially Paid", "Pending GRN"], "due_date__lt":dates.today()}, fetch_linked_tables=True, privilege=True)
            if invoices.status == utils.ok and len(invoices.data.rows) > 0:
                for inv in invoices.data.rows:
                    if inv.status == "Outstanding":
                        inv.status = "Overdue"
                    if inv.status == "Partially Returned":
                        inv.status = "Overdue | Partially Returned"
                    if inv.status == "Outstanding | Pending GRN":
                        inv.status = "Overdue | Outstanding | Pending GRN"
                    if inv.status == "Pending GRN":
                        inv.status = "Overdue | Pending GRN"
                    if inv.status == "Partially Paid":
                        inv.status = "Overdue | Partially Paid"
                    update = self.dbms.update("Purchase_Invoice", inv, skip_hooks=True, privilege=True,skip_audit_trail=True)
        except Exception as e:
            pp(str(e))

    @classmethod
    def transaction_overdue_management(cls, dbms, tc=None):
        cls.__init__(cls, dbms, tc)
        tax_invoices = cls.validate_tax_invoices(cls)
        tax_invoices = cls.validate_purchase_invoices(cls)

