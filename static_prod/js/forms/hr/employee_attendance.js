export default {
    setup: {
        new_form_id: 'new-attendance',
        info_form_id: 'employee-attendant-info',
        title: "Employee Attendance",
        layout_columns: 3,
        allow_submit: false,
        allow_cancel: false,
        allow_delete: false,
        allow_print: false,
        allow_sending_mail: false,
        model: "Employee_Attendance"
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
            fieldlabel: "Employee Full Name",
            fieldname: "employee_name",
            fieldtype: "read-only",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            fetchfrom:"employee",
            fetchfield: "full_name"
        },
       
        {
            id: "attendance-date",
            fieldlabel: "Attendance Date",
            fieldname: "attendance_date",
            fieldtype: "read-only",
            columns: 1,
            placeholder: " ",
            required: true,
            hidden: true,
            default: lite.utils.today()
        },
        {
            id: "company",
            fieldlabel: "Council",
            fieldname: "company",
            fieldtype: "link",
            model: "Company",
            columns: 1,
            placeholder: " ",
            required: true,
            hidden: true,
            fetchfrom:"employee",
            fetchfield: "company",
            default: lite.user.company.name
        },
        {
            id: "department",
            fieldlabel: "Department /  Unit",
            fieldname: "department",
            fieldtype: "read-only",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: true,
            fetchfrom:"employee",
            fetchfield: "department"
        },
        {
            id: "designation",
            fieldlabel: "Job Title",
            fieldname: "designation",
            fieldtype: "read-only",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: true,
            fetchfrom:"employee",
            fetchfield: "designation"
        },
        {
            id: "manager",
            fieldlabel: "Supervisor",
            fieldname: "manager",
            fieldtype: "read-only",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: true,
            fetchfrom:"employee",
            fetchfield: "report_to"
        },
        {
            id: "total_hours_worked",
            fieldlabel: "Working Hours",
            fieldname: "total_hours_worked",
            fieldtype: "read-only",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: true,
            fetchfrom:"employee",
            fetchfield: "working_hours"
        },
        {
            id: "shift",
            fieldlabel: "Shift",
            fieldname: "shift",
            fieldtype: "select",
            options: [
                "Morning",
                "Afternoon",
                "Evening",
                "Night",
                "Day",
            ],
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            default: "Morning"
        },
    ]
}