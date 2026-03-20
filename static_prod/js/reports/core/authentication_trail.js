
export default {
    setup: {
        model: 'Authentication_Trail',
        title: "Authentication Trail",
        report_type: "script",
        include_opening: true,
        include_closing: true,
        allow_print: false,
        is_grid_layout : true,
        allow_download_csv: true,
        allow_download_excel: true,
        allow_download_pdf: true
    },
    filters: [
        {
            id: "date",
            fieldname: "created_on",
            fieldtype: "date",
            placeholder: "Select Date",
            value:lite.utils.today()
        },
        {
            id: "user",
            fieldname: "email",
            fieldtype: "link",
            model: "Lite_User",
            placeholder: "Select User",
        },
        
    ],
    actions: [
    ],

    columns: [
        {
            column_title: "Activity Date",
            column_name: "date",
            column_type: "text",
            columns: 2,
            sortable: true
        },
        {
            column_title: "Activity Time",
            column_name: "activity_time",
            column_type: "text",
            columns: 2,
            sortable: true
        },
        {
            column_title: "Name",
            column_name: "name",
            column_type: "text",
            columns: 2,
            sortable: true
        },
        // {
        //     column_title: "activity_type",
        //     column_name: "activity_type",
        //     column_type: "Data",
        //     columns: 2,
        //     sortable: true
        // },
        {
            column_title: "Email",
            column_name: "email",
            column_type: "Date",
            columns: 2,
            sortable: true
        },
        {
            column_title: "Activity Type",
            column_name: "activity_type",
            column_type: "Data",
            columns: 2,
            sortable: true
        },
        {
            column_title: "Message",
            column_name: "message",
            column_type: "link",
            columns: 2,
            sortable: true
        },
        {
            column_title: "Status",
            column_name: "status",
            column_type: "link",
            columns: 2,
            sortable: false
        },
    ]
};