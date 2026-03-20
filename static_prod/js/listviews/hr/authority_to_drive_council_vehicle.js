// import { wipe_all_transactions } from "../core/functions.js"

export default {
    setup: {
        model: 'Request_For_Council_Car',
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
            id: "name-filter",
            fieldname: "name",
            fieldtype: "link",
            model: 'Request_For_Council_Car',
            columns: 1,
            placeholder: "ID",
        },
        {
            id: "employee-filter",
            fieldname: "employee",
            fieldtype: "link",
            model: 'Request_For_Council_Car',
            linkfield: "employee",
            columns: 1,
            placeholder: "Officer;s Name",
        },
     
       
    ],
    actions: {
        // main: [
            
        // ],
        // row: [
        //     {
        //         fun: wipe_all_transactions,
        //         title: 'Get JSON',
        //         icon: 'code',
        //         icon_color: 'teal',
        //     },
        // ]
    },
    columns: [
        {
            column_title: "Employee",
            column_name: "drivers_name",
            column_type: "text",
            columns: 4,
        },
        {
            column_title: "Driver's License Number",
            column_name: "drivers_license_number",
            column_type: "text",
            columns: 4,
        },
        {
            column_title: "Expected Return Date",
            column_name: "travel_date",
            column_type: "date",
            columns: 4,
        }        
    ]
}