export default {
    setup: {
        allow_submit: false,
        new_form_id: 'new-banking',
        info_form_id: 'banking-info',
        title: "Bank Account",
        layout_columns: 8,
        model: "Bank_Account"
    },
    form_actions: [
    ],
    fields:[
        {
            id: "name",
            fieldlabel: "Account Name",
            fieldname: "name",
            fieldtype: "text",
            columns: 2,
            required: true,
            hidden: false,
            placeholder: " ",
        },
        
        {
            id: "account_code",
            fieldlabel: "Account Code",
            fieldname: "account_code",
            fieldtype: "text",
            columns: 2,
            required: true,
            hidden: false,
            placeholder: " ",
        },
        {
            id: "is_debit",
            fieldlabel: "Is A Debit Account",
            fieldname: "is_debit",
            fieldtype: "check",
            columns: 2,
            required: false,
            hidden: false,
            placeholder: " ",
        },
        {
            id: "is_credit",
            fieldlabel: "Is A Credit Account",
            fieldname: "is_credit",
            fieldtype: "check",
            columns: 2,
            required: false,
            hidden: false,
            placeholder: " ",
        },
        
        {
            id: "sedd-brect",
            fieldlabel: " ",
            fieldname: "sedd-brect",
            fieldtype: "section-break",
            columns: 2,
            required: true,
            hidden: false,
            placeholder: " ",
            addborder: true
        },
                
        {
            id: "descriptions",
            fieldlabel: "descriptions",
            fieldname: "descriptions",
            fieldtype: "longtext",
            classnames: "h-[250px]",
            columns: 8,
            required: false,
            hidden: false,
            placeholder: " ",

        },
    ]
}