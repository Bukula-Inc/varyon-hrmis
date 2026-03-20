import { short_list_applicant, create_employee } from '../../overrides/form/hr/core.js';

export default {
  setup: {
    new_form_id: 'new-acting-appointment-settings',
    info_form_id: 'acting-appointment-settings-info',
    title: "Acting Appointment",
    layout_columns: 12,
    allow_submit: false,
    allow_cancel: true,
    allow_delete: true,
    allow_print: false,
    model: "Acting_Appointment_Settings"
  },
  form_actions: [
    // {
    //   title: "Short List Applicant",
    //   icon: "price_check",
    //   icon_color: "convert_to_text",
    //   action: short_list_applicant,
    //   for_docstatus: [0, 1],
    // //   for_status: ["Applied"],
    //   index: 1,
    // },
    // {
    //   title: "Create Employee",
    //   icon: "price_check",
    //   icon_color: "convert_to_text",
    //   action: create_employee,
    //   for_docstatus: [1],
    //   for_status: ["Applied"],
    //   index: 2,
    // },
  ],
  fields: [
    {
        id: "name",
        fieldlabel: "Name",
        fieldname: "name",
        fieldtype: "text",
        columns: 4,
        placeholder: " ",
        required: false,
        hidden: true,
        default: "ECZ"
    },
    {
        id: "section-break-maturity-period",
        fieldlabel: "Default Maturity Period (Days)",
        fieldname: "",
        fieldtype: "section-break",
        columns: 4,
    },
    {
        id: "position-holder-in-country",
        fieldlabel: "Position Holder in Country",
        fieldname: "position_holder_in_country",
        fieldtype: "select",
        columns: 4,
        placeholder: " ",
        required: false,
        hidden: false,
        options: [0,1,2,3,4,5,6,7,8,9,10,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,30],
        default: "0"
    },
    {
        id: "position-holder-not-in-country",
        fieldlabel: "Position Holder not in Country",
        fieldname: "position_holder_outside_country",
        fieldtype: "select",
        columns: 4,
        placeholder: " ",
        required: false,
        hidden: false,
        options: [0,1,2,3,4,5,6,7,8,9,10,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,30],
        default: "0"
    },

    {
        id: "grade_exceptions",
        fieldlabel: "Grades Excluded from the Default Maturity Period",
        fieldname: "grade_exceptions",
        fieldtype: "table",
        columns: 12,
        placeholder: " ",
        required: false,
        hidden: false,
        model: "Acting_Appointment_Grade_Exception",
        fields:[
            {
                id: "employee-grade",
                fieldlabel: "Employee Grade",
                fieldname: "employee_grade",
                fieldtype: "link",
                model: "Employee_Grade",
                columns: 4,
                placeholder: " ",
                required: false,
                hidden: false,
            },
            {
                id: "minimum-maturity-period-in-country",
                fieldlabel: "While in the Country",
                fieldname: "within_country",
                fieldtype: "select",
                // model: "Employee_Grade",
                columns: 4,
                placeholder: " ",
                required: false,
                hidden: false,
                default: "0",
                options: [0,1,2,3,4,5,6,7,8,9,10,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,30]
            },
            {
                id: "out-side-country",
                fieldlabel: "While Outside the Country",
                fieldname: "out_side_country",
                fieldtype: "select",
                // model: "Employee_Grade",
                columns: 4,
                placeholder: " ",
                required: false,
                hidden: false,
                default: "0",
                options: [0,1,2,3,4,5,6,7,8,9,10,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,30]
            },
        ]
    },
  ],
};
