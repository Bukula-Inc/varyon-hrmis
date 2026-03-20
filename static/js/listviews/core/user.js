export default {
    setup: {
        model: 'Lite_User',
        list_height: 50,
        allow_submit: false,
        allow_cancel: false,
        allow_delete: true,
        allow_export_csv: true,
        allow_export_excel: true,
        allow_print: false
    },
    filters: [
     
        {
            id: "lite-user",
            fieldname: "name",
            fieldtype: "link",
            model: 'Lite_User',
            linkfield: "name",
            columns: 1,
            placeholder: "Select User",
        },
    ],
    columns: [
        
        {
            column_title: "First Name",
            column_name: "first_name",
            column_type: "text",
            columns: 1,
            icon:"id_card",
            icon_color:"orange"
        },
        {
            column_title: "Last Name",
            column_name: "last_name",
            column_type: "text",
            columns: 1,
            icon:"id_card",
            icon_color:"blue"
        },
        {
            column_title: "Role",
            column_name: "main_role",
            column_type: "text",
            columns: 1,
            icon:"verified_user",
            icon_color:"yellow"
        },
        {
            column_title: "Display Image",
            column_name: "dp",
            column_type: "image",
            columns: 1,
            icon:"image",
            icon_color:"purple"
        },
        {
            column_title: "Status",
            column_name: "status",
            column_type: "status",
            columns: 1,
            icon:"image",
            icon_color:"purple"
        }
    ]
}