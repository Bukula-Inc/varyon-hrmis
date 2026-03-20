export default {
    setup: {
        new_form_id: 'new-interview-type',
        info_form_id: 'job-interview-type-info',
        title: "Interview Type",
        layout_columns: 2,
        model: "Interview_Type"
    },
    fields: [
        {
            id: "name",
            fieldlabel: "Name",
            fieldname: "name",
            fieldtype: "text",
            columns: 2,
            placeholder: " ",
            required: true,
            hidden: false,
        },
        {
            id: "description",
            fieldlabel: "Description",
            fieldname: "description",
            fieldtype: "longtext",
            classnames: "h-[400px] p-2",
            columns: 2,
            placeholder: " ",
            required: false,
            hidden: false,
        }
    ],
}