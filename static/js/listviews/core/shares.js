export default {
    setup: {
        model: 'Share',
        list_height: 50,
        allow_submit: true,
        allow_cancel: true,
        allow_delete: true,
        allow_export_csv: true,
        allow_export_excel: true,
        allow_print: true
    },
    filters: [
        {
            id: "name",
            fieldname: "name",
            fieldtype: "link",
            model: 'Share',
            linkfield: "name",
            columns: 1,
            placeholder: "Share Name",
        },
      
    ],
    actions: {
        main: [],
        row: []
    },
    columns: [
        {
            column_title: "Total Shares",
            column_name: "total_shares",
            column_type: "figure",
            is_figure: true,
            columns: 1
        },
        {
            column_title: "Total Shareholders",
            column_name: "total_shareholders",
            column_type: "figure",
            is_figure: true,
            columns: 1
        },
    ]
}