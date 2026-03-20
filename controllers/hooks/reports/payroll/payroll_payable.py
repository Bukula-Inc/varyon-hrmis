from controllers.utils import Utils
from controllers.utils.data_conversions import DataConversion
from controllers.core_functions.payroll import Core_Payroll
from controllers.utils.dates import Dates

dates = Dates ()
utils = Utils()
pp = utils.pretty_print

def apply_on (apply, val, obj):
    match apply:
        case "Basic":
            basic = DataConversion.convert_to_float (DataConversion.safe_get (obj, "basic"))
            return (val/100) * basic
        case "Gross":
            gross = DataConversion.convert_to_float (DataConversion.safe_get (obj, "gross"))
            return (val/100) * gross
        case "Net":
            net = DataConversion.convert_to_float (DataConversion.safe_get (obj, "net"))
            return (val/100) * net
        case _:
            return 0.00

def payroll_journal_listing(dbms, obj):
    core_payroll = Core_Payroll(dbms)
    dict_ = {}
    totals = utils.from_dict_to_object ()

    return_data = []
    debit_rows = []
    credit_rows = []
    unknown_rows = []

    salary_components = core_payroll.get_list ("Salary_Component")
    accounts = core_payroll.get_list ("Bank_Account")
    acc_refs = utils.array_to_dict (accounts, 'name')
    sc_dict = utils.array_to_dict (salary_components, "name")

    total_debit = 0
    total_credits = 0

    date_range = [
        dates.get_first_date_of_current_month(),
        dates.get_last_date_of_current_month()
    ]

    payslips = core_payroll.get_list(
        "Payslip",
        filters={"to_date__range": date_range}
    )

    pp (payslips)

    if payslips:
        earnings_rows = []
        deductions_rows = []

        payslip_df = utils.to_data_frame (payslips)
        payslip_df[["basic_pay", "gross", "net"]]
        totals = payslip_df[["basic_pay", "gross", "net"]].sum()

        for slip in payslips:
            earnings_rows.extend(slip.get("earnings", []))
            deductions_rows.extend(slip.get("deductions", []))

        earnings_df = utils.to_data_frame(earnings_rows)
        deductions_df = utils.to_data_frame(deductions_rows)

        if not earnings_df.empty:
            earnings_summary = (
                earnings_df
                .groupby("earning", as_index=False)["amount"]
                .sum()
                .to_dict(orient="records")
            )
            pp (earnings_summary)

        if not deductions_df.empty:
            deductions_summary = (
                deductions_df
                .groupby("deduction", as_index=False)["amount"]
                .sum()
                .to_dict(orient="records")
            )
            pp (deductions_summary)
            for sc in deductions_summary:
                amount = DataConversion.convert_to_float (DataConversion.safe_get (sc, "amount", 0))
                sc_name = DataConversion.safe_get (sc, "deduction")
                acc_name = ''
                sc_ref = DataConversion.safe_get (sc_dict, sc_name)
                pp (sc_ref)
                total_credits += amount
                if DataConversion.safe_e (sc_name, "paye", str, True):
                    acc_name = DataConversion.safe_get (DataConversion.safe_get (acc_refs, "PAYE"), "account_code")
                if DataConversion.safe_e (DataConversion.safe_get (sc_ref, "shared_deduction_custom", 0), 1, int):
                    pp (sc_ref)
                
                DataConversion.safe_list_append (credit_rows, {
                    "acc_ref": acc_name,
                    "income_debits": 0,
                    "deduction_credits": amount,
                    "money_name": sc_name
                })

            DataConversion.safe_list_append (credit_rows, {
                "acc_ref": DataConversion.safe_get (DataConversion.safe_get (acc_refs, "Net"), "account_code"),
                "income_debits": 0,
                "deduction_credits": totals.net,
                "money_name": "Net Pay"
            })
            total_credits += DataConversion.convert_to_float (totals.net)

    return_data.extend (debit_rows)
    return_data.extend (credit_rows)

    DataConversion.safe_list_append (return_data, {
        "acc_ref": "TOTAL",
        "income_debits": total_debit,
        "deduction_credits": total_credits,
        "is_opening_or_closing": True,
    })

    return utils.respond(utils.ok, {"rows": return_data})
