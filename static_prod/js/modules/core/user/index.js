// lite_file_picker

import Core_HTML_Generator from '../../../page/html/core_html_generator.js'
export default class User{
    constructor(){
        this.generator = new Core_HTML_Generator()
        this.$dp_field = $('.dp')
        this.$role_list_wrapper = $('.role-list')
        this.$permission_list_wrapper = $('.permission-list')
        this.$permission_searcher = $('.permission-searcher')
        this.$recent_users = $(".recent-users")
        this.$disabled_users = $(".disabled-users")
        lite.lite_file_picker.init_file_picker(this.handle_dp_changed_picker, this)
        // lite.page_controller.on_page_type_change(this.on_page_type_change, this)
        this.populate_dashboard()
    }


    async handle_dp_changed_picker(data, cls){
        if(data && data.file){
            const updated = await lite.connect.upload({files: data.file})
            if(updated.status === lite.status_codes.ok){
                const update_url = await lite.connect.x_post("update_user_dp", {"url": updated?.data?.data?.path,"uid": lite.form_data?.id})
                if(update_url.status == lite.status_codes.ok){
                    cls.$dp_field?.siblings("img")?.attr("src", updated?.data?.data?.path)
                    lite.alerts.toast({
                        toast_type: lite.status_codes.ok,
                        title: "Update Successful",
                        message: "Your profile picture has been changed successfully!"
                    })
                }
                else{
                    lite.alerts.toast({
                        toast_type:lite.status_codes.internal_server_error,
                        title:"Update Failed",
                        message:"An error occurred while updating your profile picture!"
                    })
                }
            }
        }
    }


    async populate_dashboard(){
        const dashboard_content = await lite.connect.dashboard("user")
        lite.utils.init_dashboard(true)
        if(dashboard_content.status === lite.status_codes.ok){
            const data = dashboard_content.data
            const recent_users = data.recent_users, disabled_users = data.disabled_users
            if(lite.utils.array_has_data(recent_users)){
                $.each(recent_users,(_, ru)=>{
                    this.$recent_users.append(this.generator.create_recent_user(ru))
                })
            }
            if(lite.utils.array_has_data(disabled_users)){
                $.each(disabled_users,(_, ru)=>{
                    this.$disabled_users.append(this.generator.create_disabled_user(ru))
                })
            }
        }
    }








    // init_permission_searcher(){
    //     const permissions_cards = $(".permission-card")
    //     this.$permission_searcher.off("keyup").keyup(e=>{
    //         const search_key = lite.utils.lower_case($(e.currentTarget).val())
    //         $(".permission-card, .permission-list-title").addClass("hidden")
    //         if(!search_key){
    //             $(".permission-card, .permission-list-title").removeClass("hidden")
    //         }
    //         else{
    //             $.each(permissions_cards,(_,pc)=>{
    //                 const props = this.get_permission_card_properties(pc)
    //                 if(lite.utils.lower_case(props?.model)?.includes(search_key) || lite.utils.lower_case(props?.title)?.includes(search_key)){
    //                     $(pc).removeClass("hidden")
    //                     $(`.permission-list-title[module="${props?.module}"]`).removeClass("hidden")
    //                 }
    //             })
    //         }
    //     })
    // }
}