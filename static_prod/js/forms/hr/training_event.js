
const ss = await lite.connect.get_system_settings()

import {
    create_training_feedback

} from "../../overrides/form/hr/core.js";

export default {
    setup: {
        new_form_id: 'new-training-event',
        info_form_id: 'training-event-info',
        title: "Training Event",
        layout_columns: 3,
        model: "Training_Event",
        allow_submit: true,
        allow_cancel: true,
        allow_delete: false,
        allow_print: false,
        allow_sending_mail: false,
    },
    form_actions: [{
        title: "Create Training Feedback",
        icon: "price_check",
        icon_color: "indigo",
        action: create_training_feedback,
        for_docstatus: [1],
        for_status: ["Submitted"],
    },


    ],
    fields: [
        {
            id: "event",
            fieldlabel: "Event Name",
            fieldname: "name",
            fieldtype: "text",
            columns: 1,
            placeholder: " ",
            required: true,
            hidden: false,
        },
        {
            id: "company",
            fieldlabel: "Council",
            fieldname: "company",
            fieldtype: "link",
            model: "Company",
            columns: 1,
            placeholder: " ",
            required: true,
            hidden: true,
            default: lite?.user?.company?.name,
        },
        {
            id: "type",
            fieldlabel: "Training Program Type",
            fieldname: "type",
            fieldtype: "link",
            model: "Training_Program_Type",
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
            id: "trainer",
            fieldlabel: "Trainer Name",
            fieldname: "trainer",
            fieldtype: "text",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,

        },
        {
            id: "trainer-email",
            fieldlabel: "Trainer Email",
            fieldname: "trainer_email",
            fieldtype: "text",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,

        },
        {
            id: "contact",
            fieldlabel: "Contact Number",
            fieldname: "contact",
            fieldtype: "text",
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
            id: "course",
            fieldlabel: "Course",
            fieldname: "course",
            fieldtype: "text",
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

        },
        {
            id: "duration",
            fieldlabel: "Time/Date",
            fieldname: "time_date",
            fieldtype: "select",
            columns: 1,
            required: true,
            hidden: false,
            placeholder: " ",
            options: ["Time", "Date"]
        },
        {
            id: "start_date",
            fieldlabel: "Start Date",
            fieldname: "start_date",
            fieldtype: "date",
            columns: 1,
            required: false,
            hidden: false,
            displayon: ["duration", "Date"]
        },
        {
            id: "end_date",
            fieldlabel: "End Dtae",
            fieldname: "end_date",
            fieldtype: "date",
            columns: 1,
            required: false,
            hidden: false,
            displayon: ["duration", "Date"]
        },
        {
            id: "start-time",
            fieldlabel: "Start Time",
            fieldname: "start_time",
            fieldtype: "time",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            displayon: ["duration", "Time"]

        },
        {
            id: "end-time",
            fieldlabel: "End Time",
            fieldname: "end_time",
            fieldtype: "time",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            displayon: ["duration", "Time"]
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
            id: "introduction",
            fieldlabel: "Description",
            fieldname: "introduction",
            fieldtype: "rich",
            height: 300,
            columns: 3,
            placeholder: " ",
            required: false,
            hidden: false,
        },
        {
            id: "sec",
            fieldlabel: "Attendees",
            fieldname: "sec",
            fieldtype: "section-break",
            columns: 1,
            addborder: true,
            required: false,
            hidden: false,
        },

        {
            id: "employees",
            fieldlabel: "Employees",
            fieldname: "employees",
            fieldtype: "table",
            required: true,
            hidden: false,
            
            model: "Employees_Training",
            fields: [
                {
                    id: "employee",
                    fieldlabel:  "Employee No",
                    fieldname: "employee",
                    fieldtype: "link",
                    model: "Employee",
                    columns: 1,
                    placeholder: " ",
                    required: true,
                    hidden: false,
                    istablefield: true,
                    filters: {
                        status: "Active",
                    }, 
                },
                {
                    id: "email",
                    fieldlabel: "Employee Email",
                    fieldname: "email",
                    fieldtype: "read-only",
                    columns: 1,
                    placeholder: " ",
                    required: true,
                    hidden: false,
                    fetchfrom: "employee",
                    fetchfield: "email",
                },
                {
                    id: "employee-attendance",
                    fieldlabel: "Employee Attendance",
                    fieldname: "employee_attendance",
                    fieldtype: "select",
                    options: [
                        "Present",
                        "Absent",
                    ],
                    columns: 1,
                    placeholder: " ",
                    required: false,
                    hidden: true,
                },
                {
                    id: "mandatory",
                    fieldlabel: "Is Mandatory",
                    fieldname: "mandatory",
                    fieldtype: "check",
                    columns: 1,
                    required: false,
                    hidden: false,
                },

            ]
        },


    ],
}