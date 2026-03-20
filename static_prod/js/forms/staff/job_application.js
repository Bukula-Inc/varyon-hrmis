;

export default {
    setup: {
        new_form_id: 'staff-new-job-application',
        info_form_id: 'staff-job-application-info',
        title: "Job Application",
        layout_columns: 3,
        model: "Job_Application",
        allow_disable: false,
    },
    fields: [
        {
            id: "name",
            fieldlabel: "Applicant Name",
            fieldname: "name",
            fieldtype: "text",
            columns: 1,
            placeholder: " ",
            required: true,
            hidden: false,
        },
        {
            id: "job-opening",
            fieldlabel: "Job Opening",
            fieldname: "job_opening",
            fieldtype: "link",
            model: "Job_Advertisement",
            columns: 1,
            placeholder: " ",
            required: false,
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
            required: false,
            hidden: false,

        },

      
         {
            id: "country",
            fieldlabel: "Country",
            fieldname: "country",
            fieldtype: "link",
            model: "Country",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            default: "Zambia"
           
        },
        {
            id: "email",
            fieldlabel: "Email Address",
            fieldname: "email",
            fieldtype: "text",
            columns: 1,
            placeholder: " ",
            required: true,
            hidden: false,
        },
        {
            id: "mobile",
            fieldlabel: "Phone Number",
            fieldname: "mobile",
            fieldtype: "text",
            columns: 1,
            placeholder: " ",
            required: true,
            hidden: false,
        },
    
        {
            id: "resume",
            fieldlabel: "Resume",
            fieldname: "ci",
            fieldtype: "section-break",
            addborder: true,
            columns: 1,
            hidden: false,
        },
        {
            id: "cover-letter",
            fieldlabel: "Cover Letter",
            fieldname: "cover_letter",
            fieldtype: "rich",
            height: 300,
            columns: 3,
            placeholder: " ",
            required: false,
            hidden: false,
        },
       
        {
            id: "attachments",
            fieldlabel: "Resume Attachment",
            fieldname: "attachments",
            fieldtype: "table",
            model: "",
            required: false,
            hidden: false,
            
            fields: [
                {
                    id: "resume",
                    fieldlabel: "Attachment",
                    fieldname: "resume",
                    fieldtype: "file",
                    columns: 4,
                    placeholder: " ",
                    required: true,
                    hidden: false,
                    istablefield: true,
                },
                
                
            ]
        },

        {
            id: "details",
            fieldlabel: "Salary Expectation",
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