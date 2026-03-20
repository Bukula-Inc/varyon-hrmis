export default {
    setup: {
        allow_submit: false,
        new_form_id: 'new-country',
        info_form_id: 'country-info',
        title: "Country",
        layout_columns: 2,
        model: "Country"
    },
    fields: [
        {
            id: "name",
            fieldlabel: "Country Name",
            fieldname: "name",
            fieldtype: "text",
            columns: 1,
            placeholder: "Enter Country Name",
            required: true,
            hidden: false,
            description: "Country Name",
        },
        {
            id: "code",
            fieldlabel: "Country Code",
            fieldname: "code",
            fieldtype: "text",
            columns: 1,
            placeholder: "Enter Country Code",
            required: true,
            hidden: false,
            
        },
        {
            id: "date-format",
            fieldlabel: "Date Format",
            fieldname: "date_format",
            fieldtype: "text",
            columns: 1,
            placeholder: "Enter Date Format",
            required: false,
            hidden: false,
            
            default:"YYY-MM-DD"
        },
        {
            id: "time-format",
            fieldlabel: "Time Format",
            fieldname: "time_format",
            fieldtype: "text",
            columns: 1,
            placeholder: "Enter Time Format",
            required: true,
            hidden: false,
            
            default:"HH:MM:SS"
        },
        {
            id: "time-zones",
            fieldlabel: "Time Zone",
            fieldname: "time_zones",
            fieldtype: "text",
            columns: 1,
            placeholder: "Enter Zones",
            required: true,
            hidden: false,
            
        },

    ],
}