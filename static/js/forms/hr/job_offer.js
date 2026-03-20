
import { create_employee_from_job_offer} from "../../overrides/form/hr/core.js"
console.log(lite);

export default {
    setup: {
        new_form_id: 'new-job-offer',
        info_form_id: 'job-offer-info',
        title: "Job Offer",
        layout_columns: 6,
        allow_submit: true,
        allow_cancel: true,
        allow_delete: false,
        allow_print: true,
        allow_preview:true,
        allow_sending_mail: true,
        model: "Job_Offer"
    },
    form_actions: [{
        title: "Create as Employee",
        icon: "add",
        icon_color: "green",
        action: create_employee_from_job_offer,
        for_docstatus: [1],
        for_status: ["Submitted", "Confirmed"],
    },
    ],
    fields: [
        {
            id: "interview",
            fieldlabel: "Interview",
            fieldname: "interview",
            fieldtype: "link",
            model: "Interview",
            columns: 1,
            placeholder: " ",
            required: true,
            hidden: false,
        },
        {
            id: "short-listed-applicant",
            fieldlabel: "Short Listed Applicant",
            fieldname: "short_listed_applicant",
            fieldtype: "link",
            model: "Applicant_Short_List",
            columns: 1,
            placeholder: "Applicant Short List",
            required: true,
            hidden: true,
        },
        // {
        //     id: "short-listed-applicant",
        //     fieldlabel: "Short Listed Applicant",
        //     fieldname: "short_listed_applicant",
        //     fieldtype: "link",
        //     model: "Applicant_Short_List",
        //     columns: 1,
        //     placeholder: "Applicant Short List",
        //     required: true,
        //     hidden: true,
        // },
        {
            id: "applicant_name",
            fieldlabel: "Applicant Name",
            fieldname: "applicant_name",
            fieldtype: "read-only",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            fetchfrom:"interview",
            fetchfield: "applicant"
        },
        {
            id: "applicant_email",
            fieldlabel: "Applicant Email",
            fieldname: "applicant_email",
            fieldtype: "read-only",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            fetchfrom:"interview",
            fetchfield: "applicant_email"
        },
        
        {
            id: "offer-date",
            fieldlabel: "Offer Date",
            fieldname: "offer_date",
            fieldtype: "date",
            model: "",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            default: lite?.utils?.today(),
        },
        {
            id: "offer_due_date",
            fieldlabel: "Offer Due Date",
            fieldname: "offer_due_date",
            fieldtype: "date",
            columns: 1,
            placeholder: " ",
            required: true,
            hidden: false,
            default: lite?.utils?.add_days(lite?.utils?.today(), 10),
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
            fetchfrom:"interview",
            fetchfield: "offered_job_title"

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

        // NEW
    
        {
            id: "job-application",
            fieldlabel: "Job Application",
            fieldname: "job_application",
            fieldtype: "link",
            model: "Job_Application",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
        },
        {
            id: "location",
            fieldlabel: "Location",
            fieldname: "location",
            fieldtype: "text",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            fetchfrom:"short-listed-applicant",
            fetchfield: "location"
        },
    
        {
            id: "applicant-contact-info",
            fieldlabel: "Applicant Contact Info",
            fieldname: "applicant_contact_info",
            fieldtype: "text",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            fetchfrom:"interview",
            fetchfield: "contact_no"
        },
    
        {
            id: "grade",
            fieldlabel: "Salary Grade",
            fieldname: "grade",
            fieldtype: "link",
            model: "Employee_Grade",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
        },
    
        {
            id: "salary",
            fieldlabel: "Salary",
            fieldname: "salary",
            fieldtype: "currency",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            fetchfrom:"grade",
            fetchfield: "basic_pay"
        },
        {
            id: "hr-hod",
            fieldlabel: "HR HOD",
            fieldname: "hr_hod",
            fieldtype: "link",
            model: "Employee",
            height:340,
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
        },

        // NEW ENDS

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
            id: "entitlements-of-service",
            fieldlabel: "Entitlements of Service",
            fieldname: "entitlements_of_service",
            fieldtype: "table",
            model: "Job_Offer_Entitlement_List",
            columns: 3,
            placeholder: " ",
            required: false,
            hidden: false,
            fields: [    
                {
                    id: "entitlement",
                    fieldlabel: "Entitlement",
                    fieldname: "entitlement",
                    fieldtype: "text",
                    columns: 6,
                    placeholder: "",
                    required: false,
                    hidden: false,
                },    
                {
                    id: "entitlement-amount",
                    fieldlabel: "Entitlement Amount",
                    fieldname: "entitlement_amount",
                    fieldtype: "float",
                    columns: 6,
                    placeholder: " ",
                    required: false,
                    hidden: false,
                    default: "0.00"
                },
                {
                    id: "frequency",
                    fieldlabel: "Frequency",
                    fieldname: "frequency",
                    fieldtype: "select",
                    columns: 6,
                    placeholder: " ",
                    required: false,
                    hidden: false,
                    options:[
                        "Daily",
                        "Weekly",
                        "Monthly",
                        "Quarterly",
                        "Semi-Annual",
                        "Yearly"
                    ]
                },

            ]
        },    
        {
            id: "working-hours",
            fieldlabel: "Working Hours",
            fieldname: "working_hours",
            fieldtype: "table",
            height:340,
            columns: 3,
            placeholder: " ",
            required: false,
            hidden: false,
            fields: [    
                {
                    id: "reporting-hour",
                    fieldlabel: "Reporting Hour",
                    fieldname: "reporting_hour",
                    fieldtype: "time",
                    columns: 6,
                    placeholder: "",
                    required: false,
                    hidden: false,
                },    
                {
                    id: "leaving-hour",
                    fieldlabel: "Leaving Hour",
                    fieldname: "leaving_hour",
                    fieldtype: "time",
                    columns: 6,
                    placeholder: "",
                    required: false,
                    hidden: false,
                }, 

            ]
        },
    
        {
            id: "terms-and-conditions",
            fieldlabel: "Terms and Conditions",
            fieldname: "terms_and_conditions",
            fieldtype: "rich",
            height:340,
            columns: 6,
            placeholder: " ",
            required: false,
            hidden: false,
        },  

    ],
}