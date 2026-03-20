const ss = await lite.connect.get_system_settings()
import { approve_application } from "../../overrides/form/hr/core.js"

export default {
    setup: {
        model: "Training_Program_Application",
        new_form_id: 'new-training-program-form',
        info_form_id: 'scholarship-form-info',
        title: "Training Program Applicant",
        layout_columns: 3,
        allow_submit: true,
        allow_cancel: true,
        allow_delete: false,
        allow_print: false,
        allow_sending_mail: false,
    },
    form_actions: [
        {
           title: "Approve Application",
           icon: "done_all",
           icon_color: "indigo",
           action: approve_application,
           for_docstatus: [1]
       },
    
      
   ],
    fields: [
        {
            id: "name",
            fieldlabel: "Applicant Name",
            fieldname: "name",
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
            id: "first_name",
            fieldlabel: "Applicant First Name",
            fieldname: "first_name",
            fieldtype: "read-only",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            fetchfrom: "name",
            fetchfield: "first_name",
        },
        {
            id: "last_name",
            fieldlabel: "Applicant First Name",
            fieldname: "last_name",
            fieldtype: "read-only",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            fetchfrom: "name",
            fetchfield: "last_name",
        },
        {
            id: "gender",
            fieldlabel: "Gender",
            fieldname: "gender",
            fieldtype: "read-only",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            fetchfrom: "name",
            fetchfield: "last_name",
        },
        {
            id: "email",
            fieldlabel: "Applicant Email Address",
            fieldname: "email",
            fieldtype: "read-only",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            fetchfrom: "name",
            fetchfield: "email",
        },
        {
            id: "department",
            fieldlabel: "Department /  Unit",
            fieldname: "department",
            fieldtype: "text",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,  
           
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
            hidden: true,
            default: lite.user.company.name
        },
        {
            id: "training_program",
            fieldlabel: "Training Program",
            fieldname: "training_program",
            fieldtype: "link",
            model: "Training_Program_Type",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            
        },
        {
            id: "course",
            fieldlabel: "Area of Interest",
            fieldname: "course",
            fieldtype: "text",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
        },
        {
            id: "level",
            fieldlabel: "Level",
            fieldname: "level",
            fieldtype: "text",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
        },
        
    ]
}
