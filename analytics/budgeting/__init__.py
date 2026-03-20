import pandas as pd
from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.utils.dict_to_object import Dict_To_Object

utils = Utils ()
dates = Dates ()
pp = utils.pretty_print
throw = utils.throw

class Budgeting_Analytics:
    def __init__(self,dbms,object=None):
        self.dbms = dbms
        self.object = object

    def calculate_budget_setup_metrics(self, data):
        df = utils.to_data_frame(data)
        total_count = len(df)
        draft_count = len(df[df['status'] == 'Draft'])
        submitted_count = len(df[df['status'] == 'Submitted'])
        approved_count = len(df[df['status'] == 'Approved'])
        rejected_count = len(df[df['status'] == 'Rejected'])
        pending_count = len(df[df['status'] == 'Pending Approval'])

        metrics = Dict_To_Object({
            "total": total_count,
            "draft": draft_count,
            "submitted": submitted_count,
            "approved": approved_count,
            "rejected": rejected_count,
            "pending": pending_count,
        })

        return utils.respond(utils.ok, metrics)
    
    def calculate_committee_setup_metrics(self, data):
        df = utils.to_data_frame(data)
        total_count = len(df)
        draft_count = len(df[df['status'] == 'Draft'])
        submitted_count = len(df[df['status'] == 'Submitted'])
        approved_count = len(df[df['status'] == 'Approved'])
        rejected_count = len(df[df['status'] == 'Rejected'])

        metrics = Dict_To_Object({
            "total": total_count,
            "draft": draft_count,
            "submitted": submitted_count,
            "approved": approved_count,
            "rejected": rejected_count,
        })

        return utils.respond(utils.ok, metrics)

    def calculate_consolidated_budget_metrics(self, data):
        df = utils.to_data_frame(data)
        total_count = len(df)
        approved_count = len(df[df['status'] == 'Approved'])
        rejected_count = len(df[df['status'] == 'Rejected'])
        pending_count = len(df[df['status'] == 'Pending Approval'])

        total_income = 0
        total_expenses = 0

        for _, row in df.iterrows():
            if 'budget_data' in row:
                budget_data = row['budget_data']
                if isinstance(budget_data, list) and len(budget_data) == 1 and budget_data[0] is not None:
                    total_income += float(budget_data[0]['totals']['income'].get('Total', 0))
                    total_expenses += float(budget_data[0]['totals']['expense'].get('Total', 0))

        metrics = Dict_To_Object({
            "total": total_count,
            "approved": approved_count,
            "rejected": rejected_count,
            "pending": pending_count,
            "total_incomes": total_income,
            "total_expenses": total_expenses,
            "net_balance": total_income - total_expenses,
        })

        return utils.respond(utils.ok, metrics)
    
    def calculate_departmental_budget_metrics(self, data):
        df = utils.to_data_frame(data)
        total_count = len(df)
        draft_count = len(df[df['status'] == 'Draft'])
        submitted_count = len(df[df['status'] == 'Submitted'])
        active_count = len(df[df['status'] == 'Active'])
        approved_count = len(df[df['status'] == 'Approved'])
        rejected_count = len(df[df['status'] == 'Rejected'])
        pending_count = len(df[df['status'] == 'Pending Approval'])

        total_income = 0
        total_expenses = 0

        for _, row in df.iterrows():
            budget_data = row['budget_data']
            if isinstance(budget_data, list) and len(budget_data) == 1 and budget_data[0] is not None:
                total_income += float(budget_data[0]['totals']['income'].get('Total', 0))
                total_expenses += float(budget_data[0]['totals']['expense'].get('Total', 0))

        metrics = Dict_To_Object({
            "total": total_count,
            "draft": draft_count,
            "submitted": submitted_count,
            "active": active_count,
            "approved": approved_count,
            "rejected": rejected_count,
            "pending": pending_count,
            "total_incomes": total_income,
            "total_expenses": total_expenses,
            "net_balance": total_income - total_expenses,
        })

        return utils.respond(utils.ok, metrics)