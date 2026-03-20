;
const ss = await lite.connect.get_system_settings()
import { create_jobopening } from "../../overrides/form/hr/core.js"
import {
    create_jobapplication
}from "../../overrides/form/staff/core.js"

export default {
    setup: {
        new_form_id: 'new-staff-job-opening',
        info_form_id: 'staff-job-opening-info',
        title: "Job Advertisement",
        layout_columns: 2,
        model: "Job_Advertisement",
        allow_delete: false,
        allow_disable: false,
    },
    form_actions: [{
        title: "Create Job Application",
        icon: "price_check",
        icon_color: "indigo",
        action: create_jobapplication,
        for_docstatus: ["submitted","draft"]
    },
    ],
    fields: [
        {
            id: "title",
            fieldlabel: "Job Title",
            fieldname: "name",
            fieldtype: "text",
            columns: 1,
            placeholder: "Enter Job Opening",
            required: true,
            hidden: false,
        },
        {
            id: "designation",
            fieldlabel: "Job Title",
            fieldname: "designation",
            fieldtype: "link",
            model:"Designation",
            columns: 1,
            placeholder: " ",
            required: true,
            hidden: false,

        },

      
         {
            id: "company",
            fieldlabel: "Company",
            fieldname: "company",
            fieldtype: "link",
            model: "Company",
            columns: 1,
            placeholder: " ",
            required: true,
            hidden: true,
            default:ss?.data?.default_company
           
        },
        {
            id: "department",
            fieldlabel: "Department /  Unit",
            fieldname: "department",
            fieldtype: "link",
            model: "Department",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
          
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
            id: "description",
            fieldlabel: "Description",
            fieldname: "description",
            fieldtype: "text",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
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
            id: "currency",
            fieldlabel: "Currency",
            fieldname: "currency",
            fieldtype: "link",
            model: "Currency",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
          
        },
        
        {
            id: "lower-range",
            fieldlabel: "Lower Range",
            fieldname: "lower_range",
            fieldtype: "text",
            columns: 1,
            required: false,
            placeholder: " ",
            hidden: false,
           
        },
        {
            id: "upper-range",
            fieldlabel: "Upper Range",
            fieldname: "upper_range",
            fieldtype: "text",
            columns: 1,
            required: false,
            placeholder: " ",
            hidden: false,
           
        },
   
      
    ],
}