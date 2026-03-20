export default {
    setup: {
        model: "Appointment_Letter",
        new_form_id: 'new-appointment-letter',
        info_form_id: 'appointment-letter-info',
        title: "Appointment Letter",
        layout_columns: 12,
        allow_submit: true,
        allow_cancel: true,
        allow_delete: false,
        allow_print: false,
        allow_sending_mail: false,
    },
    fields: [
        {
            id: "job_offer",
            fieldlabel: "Job Offer",
            fieldname: "job_offer",
            fieldtype: "link",
            model: "Job_Offer",
            columns: 3,
            placeholder: " ",
            required: false,
            hidden: false,
            description: ""
        },
        {
            id: "designation",
            fieldlabel: "Job Title",
            fieldname: "designation",
            fieldtype: "read-only",
            columns: 3,
            placeholder: " ",
            required: false,
            hidden: false,
            description: "",
            fetchfrom: "job_offer",
            fetchfield: "designation"
        },
        {
            id: "applicant",
            fieldlabel: "Job Applicant",
            fieldname: "applicant",
            fieldtype: "read-only",
            columns: 3,
            placeholder: " ",
            required: false,
            hidden: false,
            description: "",
            fetchfrom: "job_offer",
            fetchfield: "applicant_name"
        },
        {
            id: "applicant_email",
            fieldlabel: "Applicant Email",
            fieldname: "applicant_email",
            fieldtype: "read-only",
            columns: 3,
            placeholder: " ",
            required: false,
            hidden: false,
            fetchfrom:"job_offer",
            fetchfield: "applicant_email"
        },
        
        {
            id: "date",
            fieldlabel: "Appointment Date",
            fieldname: "date",
            fieldtype: "date",
            columns: 3,
            placeholder: " ",
            required: true,
            hidden: false,
            value: lite.utils.today()
        },
        {
            id: "company",
            fieldlabel: "Council",
            fieldname: "company",
            fieldtype: "link",
            model: "Company",
            columns: 3,
            placeholder: " ",
            required: false,
            hidden: true,
            default: lite.user.company.name
        },
        {
            id: "info",
            fieldlabel: "",
            fieldname: "ci",
            fieldtype: "section-break",
            addborder: true,
            columns: 4,
            required: false,
            hidden: false,
        },
       
        {
            id: "appointment-context",
            fieldlabel: "appointment Context",
            fieldname: "appointment_context",
            fieldtype: "rich",
            height:340,
            columns: 12,
            placeholder: " ",
            required: true,
            hidden: false,
        },

    ]
}
