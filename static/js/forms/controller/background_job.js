import { idlelize_job } from "../../overrides/form/controller/controller.js";

export default {
    setup: {
        new_form_id: 'new-background-job',
        info_form_id: 'background-job-info',
        title: "Background Job",
        layout_columns: 2,
        model: "Background_Job"
    },
    form_actions: [
        { 
            title: "Idlelize Job",
            icon: "zone_person_idle",
            icon_color: "orange",
            action: idlelize_job,
            for_docstatus: [0, 1],
            at_index:[1]
        }
    ],
    fields: [
        {
            id: "name",
            fieldlabel: "Background Job Name",
            fieldname: "name",
            fieldtype: "text",
            columns: 1,
            placeholder: "Enter Background Job Name",
            required: true,
            hidden: false,
        },
        {
            id: "module",
            fieldlabel: "Background Job Module",
            fieldname: "module",
            fieldtype: "link",
            model:"Module",
            // linkfield:"title",
            columns: 1,
            placeholder: "Enter Background Job Module",
            required: true,
            hidden: false,
        },
    ]
}