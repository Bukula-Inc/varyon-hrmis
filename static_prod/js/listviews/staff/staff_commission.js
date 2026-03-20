export default {
    setup: {
        model: 'Commission_Entry',
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
            id: "filter-created_on-date",
            fieldname: "created_on",
            fieldtype: "date",
            mode:"single",
            columns: 1,
            placeholder: "Date",
        },
        {
            id: "name",
            fieldname: "name",
            fieldtype: "text",
            columns: 1,
            placeholder: "Select Setup Name",
            filters:{
                "sales_person": lite.employee_info?.name
            }
        },
      
    ],
    default_filters:{
        sales_person: lite.employee_info?.name
    },
    actions: {
        
    },
    columns: [
        {
            column_title: "Sales Person",
            column_name: "sales_person",
            column_type: "text",
            columns: 1,
        },
        
        {
            column_title: "Reference",
            column_name: "reference",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Service/Product",
            column_name: "service_or_product",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Inclusive Amount",
            column_name: "inclusive_amount",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Commission Type",
            column_name: "commission_type",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Commission Amount",
            column_name: "commission_amount",
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