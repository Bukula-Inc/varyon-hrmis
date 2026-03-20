import {
    renew_contract,
    terminate_contract,
} from "../../overrides/form/hr/core.js";

export default {
    setup: {
        new_form_id: 'new-contact-hr',
        info_form_id: 'contact-info-hr',
        title: "Contract",
        layout_columns: 8,
        model: "Hr_Contract",

        allow_submit: true,
        allow_councel: true,
        allow_print: false,
        allow_delete: true,
    },
    form_actions: [
        {
            title: "Renew Contract",
            icon: "price_check",
            icon_color: "indigo",
            action: renew_contract,
            for_docstatus: [1],
            for_status: ["Submitted"],
        },
        {
            title: "Terminate Contract",
            icon: "price_check",
            icon_color: "indigo",
            action: terminate_contract,
            for_docstatus: [1],
            for_status: ["Submitted"],
        },
    ],
    
    fields: [
        {
            id: "contract_type",
            fieldlabel: "Select Contract Type",
            fieldname: "contract_type",
            fieldtype: "link",
            model: "Hr_Contract_Type",
            columns: 2,
            placeholder: " ",
            required: true,
            hidden: false,
        },
        {
            id: "employee",
            fieldlabel: "Select Employee By Id",
            fieldname: "employee",
            fieldtype: "link",
            model: "Employee",
            columns: 2,
            placeholder: " ",
            required: true,
            hidden: false,
            filters: {
                "status": "Active"
            }
        },
        {
            id: "full_name",
            fieldlabel:  "Employee No",
            fieldname: "full_name",
            fieldtype: "text",
            columns: 2,
            placeholder: " ",
            fetchfrom: "employee",
            fetchfield: "full_name",
            required: false,
            hidden: false,
        },

        {
            id: "company",
            fieldlabel: "Council",
            fieldname: "company",
            fieldtype: "link",
            model: "Company",
            columns: 2,
            placeholder: " ",
            default: "Company",
            required: false,
            hidden: true,
            default: lite.user.company.name,
        },

        {
            id: "period",
            fieldlabel: "Add Period",
            fieldname: "period",
            fieldtype: "check",
            columns: 2,
            placeholder: " ",
            required: false,
            hidden: false,
        },

        {
            id: "effective_date",
            fieldlabel: "Effective Date",
            fieldname: "effective_date",
            fieldtype: "date",
            columns: 2,
            placeholder: " ",
            required: false,
            hidden: false,
            displayon: ["period", 1]
        },
        {
            id: "end_date",
            fieldlabel: "End Date",
            fieldname: "end_date",
            fieldtype: "date",
            columns: 2,
            placeholder: " ",
            required: false,
            hidden: false,
            displayon: ["period", 1]
        },
        {
            id: "contract_content",
            fieldlabel: "Contract Content",
            fieldname: "contract_content",
            fieldtype: "rich",
            height: 300,
            columns: 8,
            placeholder: " ",
            required: false,
            hidden: false,
        },

    ],
}