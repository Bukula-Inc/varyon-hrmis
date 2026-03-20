export default {
    setup: {
        model: 'Country',
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
            id: "country",
            fieldname: "country",
            fieldtype: "link",
            model: 'Country',
            columns: 1,
            placeholder: "Select Country",
        },
      
    ],
    actions: {
        
    },
    columns: [
        {
            column_title: "Country Code",
            column_name: "code",
            column_type: "text",
            columns: 1,
        },
        
        {
            column_title: "Date Format",
            column_name: "date_format",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Time Format",
            column_name: "time_format",
            column_type: "text",
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