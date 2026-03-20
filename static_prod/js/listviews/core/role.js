export default {
    setup: {
        model: 'Role',
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
            model: 'Role',
            linkfield: "name",
            columns: 1,
            placeholder: "Role Name",
        },
      
    ],
    actions: {
        main: [],
        row: []
    },
    columns: [
        {
            column_title:"Module",
            column_type:"link",
            column_name:"module"
        },
        {
            column_title:"Department",
            column_type:"link",
            column_name:"department"
        },
        {
            column_title:"Default Dashboard",
            column_type:"link",
            column_name:"default_dashboard"
        },
        {
            column_title:"Status",
            column_type:"status",
            column_name:"status"
        }
    ]
}