export default {
    setup: {
        model: 'Cost_Center',
        list_height: 50,
        allow_submit: false,
        allow_cancel: false,
        allow_delete: true,
        allow_export_csv: false,
        allow_export_excel: false,
        allow_print: false
    },
    filters: [
     
        {
            id: "name",
            fieldname: "name",
            fieldtype: "link",
            model: 'Cost_Center',
            linkfield: "name",
            columns: 1,
            placeholder: "Select Cost Center",
        },
      
    ],
    actions: {
        main: [
            {
                fun: null,
                title: 'Wipe All Transactions',
                icon: 'recycling',
                icon_color: 'teal',
                show_on_list_check: false
            },
            {
                fun: null,
                title: 'Delete this row',
                icon: 'recycling',
                icon_color: 'red',
                show_on_list_check: false,
                is_custom_button: true
            },
        ],
        row: [
            {
                fun: null,
                title: 'Get JSON',
                icon: 'code',
                icon_color: 'teal',
            },
        ]
    },
    columns: [
        {
            column_title: "Company",
            column_name: "name",
            column_type: "link",
            columns: 1,
        },
    ]
}