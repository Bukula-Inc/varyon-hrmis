export default {
    setup: {
        model: 'Data_Importation',
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
            model: 'Data_Importation',
            linkfield: "name",
            columns: 1,
            placeholder: "Select Data Importation Name",
        },
      
    ],
    actions: {
        // main: [
        //     {
        //         fun: null,
        //         title: 'Wipe All Transactions',
        //         icon: 'recycling',
        //         icon_color: 'teal',
        //         show_on_list_check: false
        //     },
        //     {
        //         fun: null,
        //         title: 'Delete this row',
        //         icon: 'recycling',
        //         icon_color: 'red',
        //         show_on_list_check: false,
        //         is_custom_button: true
        //     },
        // ],
        // row: [
        //     {
        //         fun: null,
        //         title: 'Get JSON',
        //         icon: 'code',
        //         icon_color: 'teal',
        //     },
        // ]
    },
    columns: [
        {
            column_title: "Importing For",
            column_name: "model",
            column_type: "link",
            columns: 1,
        },
        {
            column_title: "Status",
            column_name: "status",
            column_type: "status",
            columns: 1,
        },
    ]
}