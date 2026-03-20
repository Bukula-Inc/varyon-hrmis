import {
    open_case_outcome,
    
} from "../../overrides/form/hr/core.js";

export default {
    setup: {
        new_form_id: 'new-disciplinary',
        info_form_id: 'employee-disciplinary-info',
        title: "Employee Disciplinary",
        layout_columns: 3,
        allow_submit: true,
        allow_cancel: false,
        allow_delete: false,
        allow_print: false,
        allow_sending_mail: true,
        model: "Employee_Disciplinary"
    },
    form_actions: [{
        title: "View The Case Outcome",
        icon: "folder_open",
        icon_color: "indigo",
        action: open_case_outcome,
        for_docstatus: [1],
    },
  
    ],

    fields: [
        {
            id: "charge",
            fieldlabel: "Charge",
            fieldname: "charge",
            fieldtype: "text",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            // filters: {
            //     status: "Submitted",
            // }, 
        },
        {
            id: "charging-officer",
            fieldlabel: "Charging Officer Id",
            fieldname: "issue_raiser",
            fieldtype: "link",
            model: "Employee",
            columns: 1,
            placeholder: " ",
            required: true,
            hidden: false,
            filters: {
                status: "Active",
            }, 
            fetchfrom:"issue",
            fetchfield: "raised_by"
        },
      
        {
            id: "charging-officer-name",
            fieldlabel: "Charging Officer's Name",
            fieldname: "issue_raiser_name",
            fieldtype: "text",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            fetchfrom:"charging-officer",
            fetchfield: "full_name"
        },
        {
            id: "charging-officer-department",
            fieldlabel: "Charging Officer's Department",
            fieldname: "issue_raiser_department",
            fieldtype: "link",
            model: "Department",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            fetchfrom:"charging-officer",
            fetchfield: "department"
        },
        {
            id: "charging-officer-reports-to",
            fieldlabel: "Charging Officer Reports to",
            fieldname: "issue_raiser_reports_to",
            fieldtype: "text",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            fetchfrom:"charging-officer",
            fetchfield: "report_to"
        },

            
        {
            id: "date-of-warning",
            fieldlabel: "Date of Warning",
            fieldname: "date_of_warning",
            fieldtype: "date",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: true,
            value: lite.utils.today()
        },
       
        {
            id: "sec",
            fieldlabel: "",
            fieldname: "sec",
            fieldtype: "section-break",
            columns: 1,
            addborder: true,
            required: false,
            hidden: false,
        },
        {
            id: "accused-officer",
            fieldlabel: "Accused Officer Id",
            fieldname: "subject",
            fieldtype: "link",
            model: "Employee",
            columns: 1,
            required: true,
            hidden: false,
            filters: {
                status: "Active",
            }, 
            fetchfrom:"charge",
            fetchfield: "grievance_against"
        },
      
        {
            id: "accused-officer-name",
            fieldlabel: "Accused Officer's Names",
            fieldname: "subject_name",
            fieldtype: "text",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            fetchfrom:"accused-officer",
            fetchfield: "full_name"
        },
        {
            id: "accused-officer-department",
            fieldlabel: "Accused Officer's Department",
            fieldname: "subject_department",
            fieldtype: "link",
            model: "Department",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            fetchfrom:"accused-officer",
            fetchfield: "department"
        },
        {
            id: "accused-officer-reports-to",
            fieldlabel: "Accused Officer Supervisor",
            fieldname: "subject_reports_to",
            fieldtype: "text",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            fetchfrom:"accused-officer",
            fetchfield: "report_to"
        },

        {
            id: "sec",
            fieldlabel: "",
            fieldname: "sec",
            fieldtype: "section-break",
            columns: 1,
            addborder: true,
            required: false,
            hidden: false,
        },
        {
            id: "violation-type",
            fieldlabel: "Violation Type ",
            fieldname: "violation_type",
            fieldtype: "link",
            model: "Violation_Type",
            columns: 1,
            placeholder: " ",
            required: true,
            hidden: false,
        },
       
        {
            id: "violation-from-date",
            fieldlabel: "Violation From Date",
            fieldname: "violation_date",
            fieldtype: "date",
            columns: 1,
            placeholder: " ",
            required: true,
            hidden: false,
            value: lite.utils.today()
        },
       
        {
            id: "violation-to-date",
            fieldlabel: "Violation to Date",
            fieldname: "violation_to_date",
            fieldtype: "date",
            columns: 1,
            placeholder: " ",
            required: true,
            hidden: false,
            value: lite.utils.today()
        },
        {
            id: "place-of-occurance",
            fieldlabel: "Place of Occurrence",
            fieldname: "violation_location",
            fieldtype: "text",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
        },
        {
            id: "accused-officer-report",
            fieldlabel: "Accused Officer's Report",
            fieldname: "accused_officer_report",
            fieldtype: "file",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
        },
        {
            id: "sec",
            fieldlabel: "",
            fieldname: "sec",
            fieldtype: "section-break",
            columns: 1,
            addborder: true,
            required: false,
            hidden: false,
        },

        {
            id: "details-of-occurance",
            fieldlabel: "Details of Occurrence",
            fieldname: "subject_statement",
            fieldtype: "rich",
            height: 300,
            columns: 3,
            placeholder: " ",
            required: false,
            hidden: false,
        },
        {
            id: "sec",
            fieldlabel: "",
            fieldname: "sec",
            fieldtype: "section-break",
            columns: 1,
            addborder: true,
            required: false,
            hidden: false,
        },
        {
            id: "description-of-violation",
            fieldlabel: "Details of Charge",
            fieldname: "description_of_violation",
            fieldtype: "rich",
            height: 300,
            columns: 3,
            placeholder: " ",
            required: false,
            hidden: false,
        },
    ],
}