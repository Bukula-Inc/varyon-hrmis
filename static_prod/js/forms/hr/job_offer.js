
import { create_appointment_letter} from "../../overrides/form/hr/core.js"
console.log(lite);

export default {
    setup: {
        new_form_id: 'new-job-offer',
        info_form_id: 'job-offer-info',
        title: "Job Offer",
        layout_columns: 3,
        allow_submit: true,
        allow_cancel: true,
        allow_delete: false,
        allow_print: true,
        allow_preview:true,
        allow_sending_mail: true,
        model: "Job_Offer"
    },
    form_actions: [{
        title: "Create Appointment Letter",
        icon: "unsubscribe",
        icon_color: "indigo",
        action: create_appointment_letter,
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
            fetchfield: "email"
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
            fetchfield: "designation"

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
            id: "salary",
            fieldlabel: "Salary",
            fieldname: "salary",
            fieldtype: "currency",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            fetchfrom:"short-listed-applicant",
            fetchfield: "salary_expectation"
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
            id: "terms-and-conditions",
            fieldlabel: "Terms and Conditions",
            fieldname: "terms_and_conditions",
            fieldtype: "rich",
            height:340,
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: true,
        },

        // NEW 
    
        {
            id: "housing-allowance",
            fieldlabel: "Housing Allowance",
            fieldname: "housing_allowance",
            fieldtype: "currency",
            height:340,
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
        },
    
        {
            id: "transport-allowance",
            fieldlabel: "Transport Allowance",
            fieldname: "transport_allowance",
            fieldtype: "currency",
            height:340,
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
        },
    
        {
            id: "medical-scheme",
            fieldlabel: "Medical Scheme",
            fieldname: "medical_scheme",
            fieldtype: "text",
            height:340,
            columns: 1,
            placeholder: "Medical Scheme",
            required: false,
            hidden: false,
        },
    
        {
            id: "pension-scheme",
            fieldlabel: "Pension Scheme",
            fieldname: "pension_scheme",
            fieldtype: "text",
            height:340,
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
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

    ],
}