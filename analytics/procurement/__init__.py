import pandas as pd
from controllers.utils import Utils
from controllers.utils.dates import Dates
from datetime import datetime

utils = Utils ()
dates = Dates ()
pp = utils.pretty_print
throw = utils.throw

class Procurement_Analytics:
    def __init__(self,dbms,object=None):
        self.dbms = dbms
        self.object = object

    def req_side_view(self, data):
        df = utils.to_data_frame(data)
        total_count = len(df)
        draft_count = len(df[df['status'] == 'Draft'])
        pending_count = len(df[df['status'] == 'Pending'])
        ordered_count = len(df[df['status'] == 'Ordered'])
        rfq_raised_count = len(df[df['status'] == 'Raised RFQ'])
        delivered_count = len(df[df['status'] == 'Delivered'])

        qtys = utils.from_dict_to_object({
            "draft": draft_count,
            "pending": pending_count,
            "rfq_raised": rfq_raised_count,
            "ordered": ordered_count,
            "delivered": delivered_count,
            # "total": total_count,
            # "draft": draft_count,
            # "submitted": submitted_count,
            # "approved": approved_count,
            # "rejected": rejected_count,
            # "pending": pending_count,
        })

        return utils.respond(utils.ok, qtys)
    def supplier_performanace_info(self, data):
        df = utils.to_data_frame(data)
        # total_count = len(df)
        # draft_count = len(df[df['status'] == 'Draft'])
        # pending_count = len(df[df['status'] == 'Pending'])
        # ordered_count = len(df[df['status'] == 'Ordered'])
        # rfq_raised_count = len(df[df['status'] == 'Raised RFQ'])
        # delivered_count = len(df[df['status'] == 'Delivered'])

        for supplier, value in df:   
            qtys = utils.from_dict_to_object({
                "supplier": supplier,
                # "sup_transactions": len(),
                # "completed_transactions": 0,
                # "score": 0,
                # "percentage": 0,
            })

        return utils.respond(utils.ok, qtys)

    def spend_analysis(self, data):
        df = utils.to_data_frame(data)
        items ={}
        items = df['line_items']

        return utils.respond(utils.ok, items)
    
    def suppliers(self, data):
        df = utils.to_data_frame(data)
        # total_count = len(df)
        # draft_count = len(df[df['status'] == 'Draft'])
        # supplier_names = df['name']
        supplier_names =df["name"]

        return utils.respond(utils.ok, supplier_names)

    def split_invoices_by_date (self, data=[] or {}):
        df = utils.to_data_frame (data)
        df['issue_date'] = pd.to_datetime(df['issue_date'])

        current_date = datetime.now()
        current_year = current_date.year
        current_month = current_date.month
        last_year = current_year - 1
        last_year_invoices = df[df['issue_date'].dt.year == last_year].to_dict(orient='records')
        # current_year_invoices = df[(df['issue_date'].dt.year == current_year) & (df['issue_date'].dt.month != current_month)].to_dict(orient='records')
        current_year_invoices = df[(df['issue_date'].dt.year == current_year) ].to_dict(orient='records')
        current_month_invoices = df[(df['issue_date'].dt.year == current_year) & (df['issue_date'].dt.month == current_month)].to_dict(orient='records')
        return {
            'last_year_invoices': last_year_invoices,
            'current_year_invoices': current_year_invoices,
            'current_month_invoices': current_month_invoices
        }