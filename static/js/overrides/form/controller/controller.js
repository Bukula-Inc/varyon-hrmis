export const idlelize_job = async({form_controller}) =>{
    const values = form_controller.get_form_data()?.values
    const loader_id = lite.alerts.loading_toast({
        title: `Idlelizing ${values?.name || ''}`, 
        message:""
    })
    
    const {status, data, error_message} = await lite.connect.x_post("idlelize_job", {"job":values?.name})
    lite.alerts.destroy_toast(loader_id)
    if(status == lite.status_codes.ok){
        lite.alerts.toast({
            toast_type: status,
            title: "Process Completed",
            message: "Background Idlelized Successfully!",
            timer: 10000
        })
    }
}