export default class About{
    constructor(){
        this.$enquiry_form = $("#enquiry-form")
    }
    init(){
        this.$enquiry_form?.off("submit")?.submit(e=>{
            e.preventDefault()
            this.$enquiry_form?.find("button").prop("disabled",true)
            this.enquiry_data = {}
            $.each(this.$enquiry_form?.find("input,textarea"),(_,f)=>this.enquiry_data[$(f).attr("id")] = $(f).val())
            const loader_id = lite.alerts.loading_toast({
                title: "Submitting your enquiry.", 
                message:`Please wait your enquiry gets submitted.`
            })
            lite.connect.x_post("submit_enquiry_from_web", this.enquiry_data).then(resolve => {
                this.$enquiry_form?.find("button").prop("disabled",false)
                lite.alerts.destroy_toast(loader_id)
                if (resolve?.status === lite.status_codes.ok) {
                    lite.alerts.toast({
                        toast_type: resolve.status,
                        title: `Submitted Successfully`,
                        message: `
                            <h4 class="leading-[1.1]">Your enquiry has been submitted successfully</h4>
                            <div>We will get back to you at the earliest</div>
                            <h3 class="leading-[1.1] text-orange-500 font-bold text-20">Thank you!</h3>
                        `,
                    })
                    this.$enquiry_form?.trigger("reset")
                }
            })
            
        })
    }
}