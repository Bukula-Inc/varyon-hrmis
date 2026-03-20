export default {
    setup: {
        allow_submit: true,
        new_form_id: 'new-payroll-processor',
        info_form_id: 'payroll-processor-info',
        title: "Payroll Processor",
        layout_columns: 4,
        model: "Payroll_Processor",
        allow_cancel:true,
        fetch_fields_from_backend: true,
    }
}