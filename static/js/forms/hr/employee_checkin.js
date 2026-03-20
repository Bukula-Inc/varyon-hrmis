export default {
    setup: {
        new_form_id: 'new-checkin',
        info_form_id: 'employee-checkin-info',
        title: "Employee Checkin",
        layout_columns: 2,
        model: "Employee_Checkin"
    },
    fields: [
        {
            id: "employee",
            fieldlabel: "Employee No",
            fieldname: "employee",
            fieldtype: "link",
            model: "Employee",
            columns: 1,
            placeholder: " ",
            required: true,
            hidden: false,
            filters: {
                status: "Active",
            }, 
        },
        {
            id: "employee-name",
            fieldlabel: "Employee Names",
            fieldname: "employee_name",
            fieldtype: "text",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            fetchfrom:"employee",
            fetchfield: "full_name"
        },
       
        {
            id: "checkin-time",
            fieldlabel: "Check-in Time",
            fieldname: "checkin_time",
            fieldtype: "date",
            columns: 1,
            placeholder: " ",
            required: true,
            hidden: false,
            mode: "time",
        },
        {
            id: "log-type",
            fieldlabel: "Log Type",
            fieldname: "log_type",
            fieldtype: "select",
            options: [
                "In",
                "Out"
            ],
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
        },
        {
            id: "device",
            fieldlabel: "Device",
            fieldname: "device",
            fieldtype: "text",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
        },
    ],
}