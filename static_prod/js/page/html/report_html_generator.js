import HTML_Builder from "./html_builder.js"

export default class Report_HTML_Generator{
    constructor(html_generator){
        this.html_generator = new HTML_Builder()
    }

    create_select_columns_on_report_download_form(columns){
        let cols = this.html_generator.build_form_field({
            id: "select-all-report-columns",
            fieldname: "select_all_columns",
            fieldtype:"check",
            fieldlabel: "Select All",
            omitlabels:true,
            classnames:"mb-1 p-3",
            label_class:"text-10",
            wrapper_class: "bg-default p-3 rounded-md font-bold"
        })
        $.each(columns,(_,col)=>{
            cols += this.html_generator.build_form_field({
                id: col.column_name,
                fieldname: col.column_name,
                fieldtype:"check",
                fieldlabel:col.column_title,
                omitlabels:true,
                classnames:"mb-1",
                label_class:"text-9",
            })
        })
        return `<form id="report-column-selection-form" class="grid grid-cols-2 gap-2 w-full h-max-content bg-gray p-3">${cols}</form>`
    }
}