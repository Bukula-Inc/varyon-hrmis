export default {
    setup: {
        model: 'Workflow_Approver_Group',
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
            model: 'Workflow_Approver_Group',
            linkfield: "name",
            columns: 1,
            placeholder: "Workflow Action Name",
        },
        
      
    ],
    actions: {
        main: [],
        row: []
    },
    columns: [
        {
            id: "minimum-total-approvers",
            column_name: "minimum_total_approvers",
            columns: 1,
            column_title: "Minimum Total Approvers",
        },
        {
            id: "status",
            column_name: "status",
            columns: 1,
            column_type:"status",
            column_title: "Status",
        },
    ]
}