
export default {
    setup: {
        allow_submit: false,
        allow_cancel: false,
        allow_delete: true,
        new_form_id: 'new-income-tax-band',
        info_form_id: 'income-tax-band-info',
        title: "Tax Band",
        layout_columns: 3,
        model: "Income_Tax_Band"
    },
    fields: [
        {
            id: "name",
            fieldlabel: "Tax Band Name",
            fieldname: "name",
            columns: 1,
            required: true,
            hidden: false,
            placeholder: " ",
        },
        {
            id: "company",
            fieldlabel: "Company",
            fieldname: "company",
            fieldtype: "link",
            model: "Company",
            columns: 1,
            required: true,
            hidden: true,
            placeholder: " ",
            default:lite.user?.company?.name
        },
        {
            id: "effective-from",
            fieldlabel: "Effective From",
            fieldname: "effective_from",
            fieldtype: "date",
            columns: 1,
            required: true,
            hidden: false,
            placeholder: " ",
            default:lite.utils.today()
        },
        {
            id: "deduct-on",
            fieldlabel: "Deduct On",
            fieldname: "deduct_on",
            fieldtype: "select",
            columns: 1,
            required: true,
            hidden: false,
            placeholder: " ",
            options: ["Gross", "Net", "Basic"]
        },
        {
            id: "tax-free-amount",
            fieldlabel: "Tax Free Amount (@0% Tax)",
            fieldname: "tax_free_amount",
            fieldtype: "float",
            columns: 1,
            required: false,
            hidden: false,
            placeholder: " ",
        },
        {
            id: "is-current",
            fieldlabel: "Is Current",
            fieldname: "is_current",
            fieldtype: "check",
            columns: 1,
            required: false,
            hidden: false,
            placeholder: " ",
            default:1
        },
        {
            id: "salary-bands",
            fieldlabel: "Salary Bands",
            fieldname: "salary_bands",
            fieldtype: "table",
            model: "Taxable_Salary_Band",
            description: "Add salary ranges on which tax band shall be calculated",
            columns: 3,
            required: true,
            hidden: false,
            fields: [
                {
                    id: "amount-from",
                    fieldlabel: "Amount From",
                    fieldname: "amount_from",
                    fieldtype: "text",
                    columns: 7,
                    required: true,
                    hidden: false,
                    placeholder: " ",
                    is_figure:true
                },
                {
                    id: "amount-to",
                    fieldlabel: "Amount To",
                    fieldname: "amount_to",
                    fieldtype: "text",
                    columns: 7,
                    required: true,
                    hidden: false,
                    placeholder: " ",
                    is_figure:true
                },
                {
                    id: "deduction-percentage",
                    fieldlabel: "Deduction Percentage",
                    fieldname: "deduction_percentage",
                    fieldtype: "percentage",
                    columns: 7,
                    required: true,
                    hidden: false,
                    placeholder: " ",
                },
            ]
        },
    ],
}