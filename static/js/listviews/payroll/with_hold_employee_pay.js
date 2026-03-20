export default {
    setup: {
        model: 'With_Hold_Employee_Pay',
        list_height: 50,
        allow_submit: true,
        allow_cancel: true,
        allow_delete: true,
        allow_export_csv: true,
        allow_export_excel: true,
        allow_print: true
    },
    filters: [
        {
            id: "name",
            fieldname: "name",
            fieldtype: "link",
            model: 'With_Hold_Employee_Pay',
            columns: 1,
            placeholder: "Select Name",
        },
      
    ],
    actions: {
        
    },
    columns: [
        {
            column_title: "Posting Date",
            column_name: "posting_date",
            column_type: "date",
            columns: 1,
        },
        {
            column_title: "Status",
            column_name: "status",
            column_type: "status",
            columns: 1,
        }
        
    ]
}