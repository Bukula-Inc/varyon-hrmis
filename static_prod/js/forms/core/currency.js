export default {
    setup: {
        new_form_id: 'new-currency-forex',
        info_form_id: 'currency-forex-info',
        title: "Currency",
        layout_columns: 2,
        model: "Currency"
    },
    fields: [
        {
            id: "name",
            fieldlabel: "Currency Name",
            fieldname: "name",
            fieldtype: "text",
            columns: 1,
            placeholder: "Enter Currency Name",
            required: true,
            hidden: false,
            description: "Currency Name",
            value: ""
        },
        {
            id: "country",
            fieldlabel: "Currency Country",
            fieldname: "country",
            fieldtype: "link",
            model: 'Country',
            linkfield: "name",
            columns: 1,
            placeholder: "Select Currency Country",
            required: false,
            hidden: false,
            default: "Zambia"
        },
        {
            id: "symbol",
            fieldlabel: "Symbol",
            fieldname: "symbol",
            fieldtype: "text",
            columns: 1,
            placeholder: "Enter Symbol",
            required: true,
            hidden: false,
            description: "Symbol"
        },
        {
            id: "fraction",
            fieldlabel: "Fraction",
            fieldname: "fraction",
            fieldtype: "text",
            columns: 1,
            placeholder: "Enter Fraction",
            required: false,
            hidden: false,
            description: "Fraction"
        },
        
        {
            id: "include-in-forex-table",
            fieldlabel: "Include In Forex Table",
            fieldname: "include_in_forex_table",
            fieldtype: "check",
            columns: 1,
            placeholder: "Include In Forex Table",
            required: false,
            hidden: false,
            default:"0"
        },
        {
            id: "include-in-quick-rates",
            fieldlabel: "Include In Quick Rates",
            fieldname: "include_in_quick_rates",
            fieldtype: "check",
            columns: 1,
            placeholder: "Include In Quick Rates",
            required: false,
            hidden: false,
            default:"0"
        },
    ],
}