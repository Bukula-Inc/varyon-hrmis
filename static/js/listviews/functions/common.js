;
export const open_document = (data) => {
    const values = data.values
    // console.log(data)
    data.config.utils.update_url_parameters({ page: 'info', doc: values.id })
    data.config.page_controller.init_page_url_changed()
}
export const submit_selected_rows = (data) => {
    console.log(data)
}
export const cancel_selected_rows = (data) => {
    console.log(data)
}

export const delete_selected_rows = (data) => {
    console.log(data, "====================")
}
export const delete_row = async (params) => {
    // await lite.utils.delay_until(()=>{ if(lite.connect){ return }},10000)
    const {controller, row_html, values, setup} = params
    const {id} = values
    if(id){
        console.log(lite.connect,"\\\\\\\\\\")
        // const deleted = await lite.connect.delete(({model: setup, doc:[932839]}))
        // console.log(deleted)
        controller.refresh_list(null, controller)
    }
}

export const export_selected_rows_to_csv = (data) => {
    console.log(data)
}

export const export_selected_rows_to_excel = (data) => {
    console.log(data)
}
