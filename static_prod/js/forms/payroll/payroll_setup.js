;
export default {
    setup: {
        new_form_id: 'new-payroll-setup',
        info_form_id: 'payroll-setup-info',
        title: "Payroll Setup",
        layout_columns: 6,
        model: "Payroll_Setup"
    },
    fields:[
        {
            id: "name",
            fieldlabel: "Council",
            fieldname: "name",
            fieldtype: "link",
            model: "Company",
            columns: 2,
            required: true,
            hidden: false,
            placeholder: " ",
            default: lite.user.company.name,
        },
        {
            id: "salary_account",
            fieldlabel: "Salary Account",
            fieldname: "salary_account",
            fieldtype: "link",
            model: "Account",
            columns: 2,
            required: true,
            hidden: false,
            placeholder: " ",
        },
        {
            id: "payroll_payable_account",
            fieldlabel: "Payroll Payable Account",
            fieldname: "payroll_payable_account",
            fieldtype: "link",
            model: "Account",
            columns: 2,
            required: true,
            hidden: false,
            placeholder: " ",
        },
        {
            id: "payment_bank_or_cash_account",
            fieldlabel: "Payment Bank/Cash Account",
            fieldname: "payment_bank_or_cash_account",
            fieldtype: "link",
            model: "Bank_Account",
            columns: 2,
            required: true,
            hidden: false,
            placeholder: " ",
        },
        
    ]
}