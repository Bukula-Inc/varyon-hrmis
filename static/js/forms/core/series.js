export default {
    setup: {
        new_form_id: 'form',
        info_form_id: 'info',
        title: "Naming Series",
        layout_columns: 2,
        model: "Series"
    },
    fields: [
        {
            id: "name",
            fieldlabel: "Page Type",
            fieldname: "name",
            fieldtype: "link",
            model:"Model",
            columns: 1,
            placeholder: "Select Page Type",
            required: true,
            hidden: false,
        },
        {
            id: "name-format",
            fieldlabel: "Name Format",
            fieldname: "name_format",
            fieldtype: "text",
            columns: 1,
            placeholder: "Enter Name Format",
            required: true,
            hidden: false,
        },
        {
            id: "series-count",
            fieldlabel: "Series Count Starts From",
            fieldname: "series_count",
            fieldtype: "int",
            columns: 1,
            placeholder: "Count Starts From",
            required: false,
            hidden: false,
            default:"0"
        },
        {
            id: "series-digits",
            fieldlabel: "Series Digits",
            fieldname: "series_digits",
            fieldtype: "int",
            columns: 1,
            placeholder: "Series Digits eg. 4",
            required: false,
            hidden: false,
            default:"0"
        },

    ],
}