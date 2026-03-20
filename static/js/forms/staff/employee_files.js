;
const ss = await lite.connect.get_system_settings()

export default {
    setup: {
        new_form_id: 'new-staff-employee-files',
        info_form_id: 'staff-employee-files-info',
        title: "Employee Files",
        layout_columns: 3,
        allow_submit: true,
        allow_cancel: true,
        allow_delete: false,
        allow_print: false,
        allow_sending_mail: false,
        model: "Employee_Files",
        allow_delete: false,
        allow_disable: false,
    },
    fields: [
        {
            id: "employee",
            fieldlabel: "Employee ",
            fieldname: "employee",
            fieldtype: "link",
            model: "Employee",
            columns: 1,
            placeholder: " ",
            required: true,
            hidden: false,
            default: lite?.employee_info?.name
        },
        {
            id: "staff-id",
            fieldlabel: "Staff ID",
            fieldname: "staff_id",
            fieldtype: "read-only",
            model: "Employee",
            columns: 2,
            required: false,
            hidden: true,
            placeholder: " ",
            default: lite.employee_info?.name,
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
            fetchfrom:"employee",
            fetchfield: "full_name"
        },
       
  
        {
            id: "company",
            fieldlabel: "Council",
            fieldname: "company",
            fieldtype: "link",
            model: "Company",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            fetchfrom:"employee",
            fetchfield: "company",
            default:ss?.data?.default_company
        },
        {
            id: "department",
            fieldlabel: "Department /  Unit",
            fieldname: "department",
            fieldtype: "link",
            model:"Department",
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
            fieldtype: "link",
            model:"Designation",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            fetchfrom:"employee",
            fetchfield: "designation"
        },
       {
            id: "sec",
            fieldlabel: "File",
            fieldname: "sec",
            fieldtype: "section-break",
            addborder: true,
            columns: 1,
            hidden: false,
        },
 
       
        {
            id: "files",
            fieldlabel: "Files",
            fieldname: "files",
            fieldtype: "table",
            columns: 2,
            required: false,
            hidden: false,
            
            fields: [
                {
                    id: "attachment",
                    fieldlabel: "Attachment",
                    fieldname: "attachment",
                    fieldtype: "file",
                    columns: 1,
                    placeholder: " ",
                    required: false,
                    hidden: false,
                    istablefield: true,
                },
                
                
            ]
        },

        
    ],
}