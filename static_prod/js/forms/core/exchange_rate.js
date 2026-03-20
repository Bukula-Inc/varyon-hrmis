export default {
    setup: {
        new_form_id: 'new-currency-forex',
        info_form_id: 'currency-forex-info',
        title: "Exchange Rate",
        layout_columns: 2,
        model: "Exchange_Rate"
    },
    fields: [
        
        {
            id: "from-currency",
            fieldlabel: "From Currency",
            fieldname: "from_currency",
            fieldtype: "link",
            model: 'Currency',
            columns: 1,
            placeholder: "Select From Currency",
            required: true,
            hidden: false,
        },
        {
            id: "to-currency",
            fieldlabel: "To Currency",
            fieldname: "to_currency",
            fieldtype: "link",
            model: 'Currency',
            columns: 1,
            placeholder: "Select To Currency",
            required: true,
            hidden: false,
        },
        {
            id: "rate",
            fieldlabel: "Exchange Rate",
            fieldname: "rate",
            fieldtype: "float",
            columns: 1,
            placeholder: "Enter Rate",
            required: true,
            hidden: false,
            default: "0.00"
        },
        {
            id: "inverse",
            fieldlabel: "Inverse",
            fieldname: "inverse",
            fieldtype: "read-only",
            columns: 1,
            placeholder: "",
            required: true,
            hidden: false,
            is_figure:true,
            default: "0.00"
        }, 
    ],
}