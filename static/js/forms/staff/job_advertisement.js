import {edit_advance} from "../../overrides/form/hr/core.js"
export default {
    setup: {
        new_form_id: 'new-job-advertisement',
        info_form_id: 'job-advertisement-info',
        title: "Job Advertisement",
        layout_columns: 12,
        model: "Job_Advertisement",
        allow_submit: true,
        allow_cancel: true,
        allow_delete: false,
        allow_print: false,
        allow_sending_mail: false,
    },
    form_actions: [
            {
                title: "Edit Advertisement",
                icon: "edit",
                icon_color: "green",
                action: edit_advance,
                for_docstatus: [1],
                at_index:[1]
            },
        ],
    fields: [
        {
            id: "designation",
            fieldlabel: "Job Title",
            fieldname: "designation",
            fieldtype: "link",
            model:"Designation",
            columns: 3,
            placeholder: "Enter Job Title",
            required: true,
            hidden: false,

        },
        {
            id: "company",
            fieldlabel: "Council",
            fieldname: "company",
            fieldtype: "link",
            model: "Company",
            columns: 3,
            placeholder: " ",
            required: true,
            hidden: true,
            default: lite.user.company.name
           
        },
        {
            id: "department",
            fieldlabel: "Department /  Unit",
            fieldname: "department",
            fieldtype: "link",
            model: "Department",
            columns: 3,
            placeholder: " ",
            required: false,
            hidden: false,
            fetchfrom: "designation",
            fetchfield: "department",
          
        },
        {
            id: "vacancies",
            fieldlabel: "Vacancies",
            fieldname: "vacancies",
            fieldtype: "int",
            columns: 3,
            placeholder: " ",
            required: false,
            hidden: false,
          
        },

        {
            id: "from_date",
            fieldlabel: "From Date",
            fieldname: "from_date",
            fieldtype: "date",
            columns: 3,
            placeholder: " ",
            required: false,
            hidden: false,
          
        },
        {
            id: "to_date",
            fieldlabel: "To Date",
            fieldname: "to_date",
            fieldtype: "date",
            columns: 3,
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
            id: "publish",
            fieldlabel: "Publish on website",
            fieldname: "publish",
            fieldtype: "check",
            columns: 3,
            required: false,
            hidden: false,
        },
        {
            id: "source-of-recruitment",
            fieldlabel: "Source of Recruitment",
            fieldname: "source_of_recruitment",
            fieldtype: "select",
            columns: 2,
            placeholder: " ",
            required: false,
            hidden: false,
            description: "",
            options: [
                "Internally",
                "Externally",
                "Other"
            ],
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
            fieldtype: "rich",
            columns: 12,
            height: 300,
            placeholder: " ",
            required: false,
            hidden: false,
            fetchfrom: "designation",
            fetchfield: "description",
        },
        {
            id: "details",
            fieldlabel: "",
            fieldname: "ci",
            fieldtype: "section-break",
            addborder: true,
            columns: 2,
            hidden: false,
        },
        {
            id: "currency",
            fieldlabel: "Currency",
            fieldname: "currency",
            fieldtype: "read-only",
            model: "Currency",
            columns: 3,
            placeholder: " ",
            required: false,
            hidden: false,
            default: "ZMW"
          
        },
        
        {
            id: "lower-range",
            fieldlabel: "Lower Range",
            fieldname: "lower_range",
            fieldtype: "text",
            columns: 3,
            required: false,
            placeholder: " ",
            hidden: false,
            default:"0.00"
           
        },
        {
            id: "upper-range",
            fieldlabel: "Upper Range",
            fieldname: "upper_range",
            fieldtype: "text",
            columns: 3,
            required: false,
            placeholder: " ",
            hidden: false,
            default:"0.00",
           
        },
    
        {
            id: "salary-range",
            fieldlabel: "Publish Salary Range",
            fieldname: "salary_range",
            fieldtype: "check",
            columns: 3,
            required: false,
            hidden: false,
           
        },
      
    ],
}