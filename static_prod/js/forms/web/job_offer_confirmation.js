
    
export default {
    setup: {
        info_form_id: 'career-job-offer-confirmation-info',
        title: "Job Offer",
        layout_columns: 3,
        allow_submit: true,
        allow_cancel: true,
        allow_delete: false,
        allow_print: false,
        allow_sending_mail: true,
        model: "Job_Offer"
    },
    form_actions: [
        {
            // title: "Create Appointment Letter",
            // icon: "unsubscribe",
            // icon_color: "indigo",
            // action: create_appointment_letter,
            // for_docstatus: [1],
            // for_status: ["Submitted", "Confirmed"],
        },
    ],
    fields: [
        {
            id: "job_application",
            fieldlabel: "Job Application",
            fieldname: "job_application",
            fieldtype: "link",
            model: "Job_Application",
            columns: 1,
            placeholder: "Job Application",
            required: true,
            hidden: false,
        },
        {
            id: "applicant_name",
            fieldlabel: "Applicant Name",
            fieldname: "applicant_name",
            fieldtype: "read-only",
            columns: 1,
            placeholder: "Applicant Name",
            required: false,
            hidden: false,
            fetchfrom:"job_application",
            fetchfield: "applicant_name"
        },
        {
            id: "applicant_email",
            fieldlabel: "Applicant Email",
            fieldname: "applicant_email",
            fieldtype: "read-only",
            columns: 1,
            placeholder: "Applicant Email",
            required: false,
            hidden: false,
            fetchfrom:"job_application",
            fetchfield: "email"
        },
        
        {
            id: "offer-date",
            fieldlabel: "Offer Date",
            fieldname: "offer_date",
            fieldtype: "date",
            model: "",
            columns: 1,
            placeholder: "Enter Date",
            required: false,
            hidden: false,
            default: ""
        },
        {
            id: "offer_due_date",
            fieldlabel: "Offer Due Date",
            fieldname: "offer_due_date",
            fieldtype: "date",
            columns: 1,
            placeholder: "Enter Due Date",
            required: true,
            hidden: false,
        },
        {
            id: "designation",
            fieldlabel: "Job Title",
            fieldname: "designation",
            fieldtype: "read-only",
            columns: 1,
            placeholder: "Enter Job Title",
            required: false,
            hidden: false,
            fetchfrom:"job_application",
            fetchfield: "designation"

        },
        {
            id: "company",
            fieldlabel: "Company",
            fieldname: "company",
            fieldtype: "link",
            model: "Company",
            columns: 1,
            placeholder: "Enter Company",
            required: false,
            hidden: true,
            default: lite.user.company.name
            
        },

        {
            id: "resume",
            fieldlabel: "Job Offer Terms",
            fieldname: "ci",
            fieldtype: "section-break",
            addborder: true,
            columns: 1,
            hidden: false,
        },
    
        {
            id: "terms-and-conditions",
            fieldlabel: "Terms and Conditions",
            fieldname: "terms_and_conditions",
            fieldtype: "rich",
            height:340,
            columns: 3,
            placeholder: " Enter Terms",
            required: false,
            hidden: false,
        },
    ],
}