export default {
    setup: {
        model: 'Training_Feedback',
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
            id: "event",
            fieldname: "training_event",
            fieldtype: "link",
            model: 'Training_Event',
            linkfield: "name",
            columns: 1,
            placeholder: "Training Event",
        },
        {
            id: "employee-no",
            fieldname: "employee",
            fieldtype: "link",
            model: 'Employee',
            columns: 1,
            placeholder: "Employee ",
        },
        {
            id: "employee-name",
            fieldname: "employee_name",
            fieldtype: "link",
            model: 'Employee',
            linkfield: "full_name",
            columns: 1,
            placeholder: "Employee Name",
        },
      
    ],
    actions: {
    },
    columns: []
}