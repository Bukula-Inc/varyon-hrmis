
export default {
    setup: {
        new_form_id: 'new-graduity-setup',
        info_form_id: 'gratuity-setup-info',
        title: "Gratuity Configuration",
        layout_columns: 6,
        model: "Gratuity_Configuration"
    },
    fields:[
        {
            id: "name",
            fieldlabel: "Name",
            fieldname: "name",
            fieldtype: "read-only",
            columns: 2,
            required: true,
            hidden: true,
            placeholder: " ",
            default: lite.user.company.name,
        },
        {
            id: "gratuity_rate",
            fieldlabel: "Gratuity Rate",
            fieldname: "gratuity_rate",
            fieldtype: "percentage",
            columns: 2,
            required: false,
            hidden: false,
            placeholder: " ",
            default:"0.00"
        },
        {
            id: "debit_account",
            fieldlabel: "Debit Account",
            fieldname: "debit_account",
            fieldtype: "link",
            model: "Account",
            columns: 2,
            required: false,
            hidden: false,
            placeholder: " ",
            filters: {
                is_group: 0,
                is_root: 0,
                root_type: "Expense",
                account_type: "Expenses",
            }
        },
        {
            id: "credit_account",
            fieldlabel: "Credit Account",
            fieldname: "credit_account",
            fieldtype: "link",
            model: "Account",
            columns: 2,
            required: false,
            hidden: false,
            placeholder: " ",
            filters: {
                is_group: 0,
                is_root: 0,
                root_type: "Liability",
                account_type: "Payable",
            }
        },
        {
            id: "minimum_rate",
            fieldlabel: "Minimum Gratuity Rate",
            fieldname: "minimum_rate",
            fieldtype: "read-only",
            columns: 6,
            required: true,
            hidden: true,
            placeholder: " ",
            default:"25"
        },
        {
            id: "transaction_currency",
            fieldlabel: "Transaction Currency",
            fieldname: "transaction_currency",
            fieldtype: "link",
            model: "Currency",
            columns: 1,
            required: true,
            hidden: false,
            placeholder: " ",
            default: lite?.user?.company?.reporting_currency
        },
    ]
}