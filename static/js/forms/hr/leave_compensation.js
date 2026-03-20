export default {
    setup: {
        new_form_id: 'new-leave-compensation',
        info_form_id: 'leave-compensation-info',
        title: "Leave Compensation",
        layout_columns: 2,
        model: "Leave_Compensation"
    },
    fields: [
        {
            id: "employee",
            fieldlabel: "Employee No",
            fieldname: "name",
            fieldtype: "link",
            model: "Employee",
            linkfield: "name",
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
            fieldlabel: "Employee Name",
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
            id: "name",
            fieldlabel: "Leave Type",
            fieldname: "leave_type",
            fieldtype: "link",
            model: "Leave_Type",
            columns: 1,
            placeholder: " ",
            required: true,
            hidden: false,
        },
    
        {
            id: "department",
            fieldlabel: "Department /  Unit",
            fieldname: "department",
            fieldtype: "read-only",
            model: "Department",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            fetchfrom:"employee",
            fetchfield: "department"
        },
    
        {
            id: "details",
            fieldlabel: "",
            fieldname: "ci",
            fieldtype: "section-break",
            addborder: true,
            columns: 1,
            hidden: false,
        },
        {
            id: "from-date",
            fieldlabel: "Work From Date",
            fieldname: "from_date",
            fieldtype: "date",
            columns: 1,
            placeholder: " ",
            required: true,
            hidden: false,
            value: lite.utils.today()
        },
        {
            id: "to-date",
            fieldlabel: "Work End Date",
            fieldname: "to_date",
            fieldtype: "date",
            columns: 1,
            placeholder: " ",
            required: true,
            hidden: false,
            value: lite.utils.today()
        },
        {
            id: "reason",
            fieldlabel: "Reason",
            fieldname: "reason",
            fieldtype: "text",
            placeholder: " ",
            columns: 1,
            required: false,
            hidden: false,
        },
      
        {
            id: "half-day",
            fieldlabel: "Half Day",
            fieldname: "half_day",
            fieldtype: "check",
            columns: 1,
            required: false,
            hidden: false,
           
        },
    ],
}