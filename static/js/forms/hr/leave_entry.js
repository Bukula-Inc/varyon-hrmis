export default {
    setup: {
        new_form_id: 'new-leave-entry',
        info_form_id: 'leave-entry-info',
        title: "Leave Entry",
        layout_columns: 3,
        model: "Leave_Entry",
        allow_submit:true,
        allow_cancel:true,
        allow_delete:true
    },
    fields: [
        {
            id: "employee",
            fieldlabel: "Employee No",
            fieldname: "employee",
            fieldtype: "link",
            model: "Employee",
            columns: 1,
            placeholder: "Enter Employee No",
            required: false,
            hidden: false,
            filters: {
                status: "Active"
            }
        },
        {
            id: "employee-name",
            fieldlabel: "Employee Name",
            fieldname: "employee_name",
            fieldtype: "text",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            
        },
        {
            id: "leave-type",
            fieldlabel: "Leave Type",
            fieldname: "leave_type",
            fieldtype: "link",
            model: "Leave_Type",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            
        },
   
  
        {
            id: "from-date",
            fieldlabel: "From Date",
            fieldname: "from_date",
            fieldtype: "date",
            columns: 1,
            placeholder: " ",
            required: true,
            hidden: false,
            default: lite.utils.today()
        },
        {
            id: "to-date",
            fieldlabel: "To Date",
            fieldname: "to_date",
            fieldtype: "date",
            columns: 1,
            placeholder: " ",
            required: true,
            hidden: false,
            default: lite.utils.add_days(lite.utils.today(), 2)
        },
        {
            id: "total-days",
            fieldlabel: "Total Days ",
            fieldname: "total_days",
            fieldtype: "int",
            columns: 1,
            placeholder: " ",
            required: true,
            hidden: false,
        },
       {
            id: "used-leaves-days",
            fieldlabel: "Used Leave days",
            fieldname: "used_leave_days",
            fieldtype: "int",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            default:'0',
            
        },
        {
            id: "remaining-leaves-days",
            fieldlabel: "Leave Balance",
            fieldname: "remaining_leave_days",
            fieldtype: "int",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            default:'0',
            
        },
    ],
}