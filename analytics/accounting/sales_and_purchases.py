from controllers.utils import Utils
from controllers.utils.dates import Dates

utils = Utils()
dates = Dates() 

pp = utils.pretty_print
throw = utils.throw

class Sales_and_Purchase_Analysis:
    def __init__(self) -> None:
        pass

    def analyse_purchases(self,purchase_invoice=[], debit_notes=[]):
        data = utils.from_dict_to_object()
        pd = utils.get_pandas_object()

        if not purchase_invoice:
            return data
        
        pi = utils.to_data_frame(purchase_invoice)
        dn = utils.to_data_frame(debit_notes)

        if debit_notes:
            dn["total_outstanding_amount"] = 0
            dn["base_total_outstanding_amount"] = 0
            dn["description"] = dn["debit_note_reason_type"]
            columns_to_negate = [
                "base_sub_total_amount",
                "base_total_discount_amount",
                "base_tax_exclusive_total_amount",
                "base_total_taxes_amount",
                "base_inclusive_total_amount",
                "base_total_outstanding_amount",
                "sub_total_amount",
                "total_discount_amount",
                "tax_exclusive_total_amount",
                "total_taxes_amount",
                "inclusive_total_amount",
            ]
            dn[columns_to_negate] = dn[columns_to_negate] * -1

        combined_df = pd.concat([pi, dn], ignore_index=True)
        combined_df['issue_date'] = pd.to_datetime(combined_df['issue_date']).dt.date
        sorted_df = combined_df.sort_values(by=['issue_date', 'id'], ascending=[False, False])
        combined_df = sorted_df.fillna("")
        new_records = combined_df.copy()
        new_records = new_records[[
            "owner", "issue_date", "doctype", "name", "reporting_currency",
            "supplier", "supplier_tax_identification_no",
            "description", "status", "currency", "reporting_currency",
            "tax_exclusive_total_amount", "total_discount_amount",
            "total_taxes_amount", "inclusive_total_amount",
            "total_outstanding_amount", "convertion_rate",
            "base_inclusive_total_amount", "base_total_outstanding_amount"
        ]]
        # pp(utils.df_to_dict(new_records))
        new_records = new_records.rename(columns={
            "issue_date": "posting_date", "name": "reference",
            "supplier_tax_identification_no": "supplier_tax_id", 
            "currency":"invoice_currency", "doctype":"transaction_type",
            "tax_exclusive_total_amount": "exclusive_amount", 
            "total_discount_amount": "discount_amount",
            "total_taxes_amount": "total_tax_amount", "convertion_rate":"exchange_rate",
            "inclusive_total_amount": "inclusive_amount",
            "total_outstanding_amount": "outstanding",
            "base_inclusive_total_amount": "invoice_amount_in_rep_currency",
            "base_total_outstanding_amount": "outstanding_in_rep_currency"
        })
        new_records['transaction_type'] = new_records['transaction_type'].str.replace("_", " ")

        to_list = utils.df_to_dict(new_records)
        to_list.append({
            "owner": "",
            "posting_date":"CLOSING",
            "transaction_type": " ",
            "reference": " ",
            "supplier": " ",
            "supplier_tax_id": " ",
            "description": " ",
            "status": " ",
            "invoice_currency": " ",
            "reporting_currency": " ",
            "exclusive_amount": " ",
            "discount_amount": " ",
            "total_tax_amount": " ",
            "inclusive_amount": " ",
            "outstanding": " ",
            "exchange_rate": " ",
            "invoice_amount_in_rep_currency":new_records["invoice_amount_in_rep_currency"].sum(),
            "outstanding_in_rep_currency": new_records["outstanding_in_rep_currency"].sum(),
            "is_opening_or_closing":True,
            "total_fields":["invoice_amount_in_rep_currency", "outstanding_in_rep_currency"],
        })

        return to_list

