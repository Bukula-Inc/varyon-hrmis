export default {
    setup: {
        model: 'Main_Working_Hours',
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
            model: 'Main_Working_Hours',
            columns: 1,
            placeholder: "State Name",
        },
      
    ],
    actions: {
        main: [],
        row: []
    },
    columns: [
        {
            column_title: "Opening Time",
            column_name: "opening_time",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Closing Time",
            column_name: "closing_time",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Status",
            column_name: "status",
            column_type: "text",
            columns: 1,
        },
    ]
}