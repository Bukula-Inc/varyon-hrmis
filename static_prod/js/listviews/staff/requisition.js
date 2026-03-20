export default {
    setup: {
        model: 'Requisition',
        list_height: 50,
        allow_submit: true,
        allow_cancel: true,
        allow_delete: false,
        allow_export_csv: true,
        allow_export_excel: true,
        allow_print: true
    },
    filters: [
        {
            id: "name",
            fieldname: "name",
            fieldtype: "link",
            model: 'Requisition',
            columns: 1,
            placeholder: "Purchase Requisition",
            filters: {
                "initiator":  lite?.user?.name 
                },
        }
    ],
    default_filters:{
        initiator:  lite?.user?.name 
    },
    actions: {},
    columns: [
        {
            column_title: "Status",
            column_name: "status",
            column_type: "status",
            columns: 1,
        },
    ]
}