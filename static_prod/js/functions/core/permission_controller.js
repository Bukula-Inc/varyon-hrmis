
export default class Permission_Controller{
    constructor(){   
        this.perms = []
        this.all = true
        if(lite.utils.array_has_data(lite?.user?.user_permissions)){
            // $.each(lite.user.user_permissions,(_,p)=>{
            //     this.perms.push(`${p.permission_model}_${p.permitted_action}`)
            // })
        }
    }
    
    init_permission_controller(){
        this.$new_btn = $(".new-action-btn")
        this.$save_btn = $(".save-action-btn")
        lite.page_controller.on_page_type_change(this.#handle_page_change,this)
    }

    #handle_page_change(data,cls){
        cls.#enforce_perm_controls(data)
    }

    
    #enforce_perm_controls(data){
        switch (data?.page || "list") {
            case "list":
                this.#enforce_listview_controls()
                break;
            case "info":
                this.#enforce_infoview_controls()
                break;
        
            default:
                break;
        }
    }


    async #enforce_listview_controls(){
        const setup = await lite.utils.delay_until(()=>{
            const stp = lite.page_controller.listview_controller?.listview?.setup
            if(stp)
                return stp
        },5000)
        
        if(!lite.utils.is_empty_object(setup)){
            const model = setup?.model
            const create_perm = `${model}_Create`
            if(!this.perms.includes(create_perm) && !this.all)
                this.$new_btn.remove()
        }
    }
    async #enforce_infoview_controls(){
        const setup = await lite.utils.delay_until(()=>{
            const stp = lite.page_controller.form_controller?.setup
            if(stp)
                return stp
        },5000)

        await lite.utils.delay_until(()=>{
            const btn = $(".update-action-btn")
            if(lite.utils.array_has_data(btn)){
                if(!lite.utils.is_empty_object(setup) && !this.all){
                    const model = setup?.model
                    const update_perm = `${model}_Update`
                    if(!this.perms.includes(update_perm))
                    btn.remove()
                }
                else btn.removeClass("hidden")
            }
        },10000)
        
    }
}