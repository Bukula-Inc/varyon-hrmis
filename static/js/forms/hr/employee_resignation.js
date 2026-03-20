
export default {
    setup: {
        new_form_id: 'new-employee-resignation',
        info_form_id: 'employee-resignation-info',
        title: "Employee Resignation",
        layout_columns: 3,
       model: "Employee_Seperation",
        allow_submit: true,
        allow_cancel: true,
        allow_delete: false,
        allow_print: false,
        allow_sending_mail: false,
    },
    form_actions: [
        { 
            title: "Approve",
            icon: "done_outline",
            icon_color: "indigo",
            action: null,
            for_docstatus: [1] ,
            at_index:1
        },
        { 
            title: "Create Exit Interview ",
            icon: "social_distance",
            icon_color: "indigo",
            action: null,
            for_docstatus: [1] ,
            at_index:2
        }
    ],
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
            fieldlabel: "Employee Name",
            fieldname: "name",
            fieldtype: "text",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            fetchfrom:"employee",
            fetchfield: "full_name",
            
        },
     
        {
            id: "department",
            fieldlabel: "Department /  Unit",
            fieldname: "department",
            fieldtype: "read-only",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
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
            hidden: false,
            fetchfrom:"employee",
            fetchfield: "designation"
        },
        {
            id: "resignation-date",
            fieldlabel: "Date of Resignation",
            fieldname: "resignation_date",
            fieldtype: "date",
            columns: 1,
            placeholder: " Enter Resignation Date",
            required: true,
            hidden: false,
            default: lite.utils.today()
        },
        {
            id: "reports-to",
            fieldlabel: "Reports To",
            fieldname: "reports_to",
            fieldtype: "read-only",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            fetchfrom:"employee",
            fetchfield: "report_to"
        },
        {
            id: "notice-period",
            fieldlabel: "Notice Period of last days of work",
            fieldname: "notice_period",
            fieldtype: "text",
            columns: 1,
            placeholder: " ",
            required: true,
            hidden: false,
        },
        {
            id: "attachment",
            fieldlabel: "Attach Separation Letter",
            fieldname: "attachment",
            fieldtype: "file",
            columns: 1,
            placeholder: "attach separation letter",
            required: false,
            hidden: false,
        },
        {
            id: "sec",
            fieldlabel: "Separation Activities",
            fieldname: "sec",
            fieldtype: "section-break",
            columns: 1,
            addborder: true,
            required: false,
            hidden: false,
        },
        {
            id: "interview-summary",
            fieldlabel: "Exit Interview Summary",
            fieldname: "interview_summary",
            fieldtype: "longtext",
            classnames: "h-[300px]",
            columns: 3,
            placeholder: " ",
            required: false,
            hidden: false,
        },
      
    ],
}