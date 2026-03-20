import {edit_advance} from "../../overrides/form/hr/core.js"
export default {
    setup: {
        new_form_id: 'new-job-advertisement',
        info_form_id: 'job-advertisement-info',
        title: "Advertisement Edit",
        layout_columns: 12,
        model: "Job_Advertisement_Edit",
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
            id: "job-advertisement",
            fieldlabel: "Job Advertisement",
            fieldname: "job_advertisement",
            fieldtype: "link",
            model:"Job_Advertisement",
            columns: 3,
            placeholder: "Enter Job Advertisement",
            required: true,
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
        },
      
    ],
}