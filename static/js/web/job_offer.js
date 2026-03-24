;
import Form_Controller from "../page/form_controller/index.js";
export default class Job_Offer {
    constructor () {
        this.$job_offer =$ ("#job-offer-confirmation-careers")
        this.$job_offer_confirmation_careers_visible_body =$("#job-offer-confirmation-careers-visible-body")
        this.$job_offer_applicant_details = $("#job-offer-applicant-details")
        this.$job_offer_submission =$ ("#job-details-submission")
        // this.submit_details()
        // this.form_controller =undefined
    }
    loadForm () {
        const document = lite.utils.get_url_parameters ("document")
        console.log(document);
        if (document == "job_offer_confirmation") {
            this.form_controller = new Form_Controller({
                page_controller: this,
                session: this.session,
                utils: this.utils,
                connect: this.connect,
                alerts: this.alerts,
                lite_date_picker:this.lite_date_picker
            })
            this.form_controller?.init_form()
        }
    
    }

    async update_job_doc(choice, job_offer_doc){
        console.log(job_offer_doc);
        
        let doc_update =null
        if(choice =="Accept"){
            doc_update =await lite?.connect?.x_post("job_offer_confirmation", {"id": job_offer_doc.id, "response": choice})  
        }else{
            this.$job_offer_confirmation_careers_visible_body.html(`<div class="w-full text-center">Thank you for response.</div>`)    
        }
        this.$job_offer_confirmation_careers_visible_body.addClass("place-content-center")
        $("#jo-confirmation-page").remove()
        this.$job_offer_applicant_details.removeClass("hidden")
        if(doc_update.status ==lite?.status_codes.ok){
            this.$job_offer_confirmation_careers_visible_body.html(`<div class="w-full text-center">You Feedback successful Submitted. Thank you for response.</div>`)
        }else{
            this.$job_offer_confirmation_careers_visible_body.html(`<div class="w-full text-center">Thank you for response.</div>`)
        }
    }

    init_applications (job_offer) {
        // lite.utils.update_url_parameters ({
        //     module: "web",
        //     app: "web",
        //     page: "info",
        //     document: "job_offer_confirmation",
        //     doc: job_offer.id
        // })

        // this.loadForm (job_offer)


        this.$job_offer_confirmation_careers_visible_body.removeClass("place-content-center")
        this.$job_offer_confirmation_careers_visible_body.html(
            `
                <div class="h-full w-full" id="jo-confirmation-page">
                    <div class="grid grid-cols-2 gap-4 p-4 text-secoundary">
                        <div class="span-col-1">
                            <span class="flex text-lg my-2">Applicant Name : <h3 class="bg-slate-50 rounded-lg font-semibold ml-[1rem] px-4" id="job-offer-applicant-name">${job_offer.applicant_name}</h3></span>
                            <span class="flex text-lg my-2">Applicant Email : <h3 class="bg-slate-50 rounded-lg font-semibold ml-[1rem] px-4" id="job-offer-applicant-name">${job_offer.applicant_email}</h3></span>
                        </div>
                        <div class="span-col-1">
                            <span class="flex text-lg my-2">Company: <h3 class="bg-slate-50 rounded-lg font-semibold ml-[1rem] px-4" id="job-offer-applicant-name">${job_offer.company}</h3></span>
                            <span class="flex text-lg my-2">Designation: <h3 class="bg-slate-50 rounded-lg font-semibold ml-[1rem] px-4" id="job-offer-applicant-name">${job_offer.designation}</h3></span>
                            <span class="flex text-lg my-2">Offer On: <h3 class="bg-slate-50 rounded-lg font-semibold ml-[1rem] px-4" id="job-offer-applicant-name">${job_offer.offer_date}</h3></span>
                            <span class="flex text-lg my-2">Due On: <h3 class="bg-slate-50 rounded-lg font-semibold ml-[1rem] px-4" id="job-offer-applicant-name">${job_offer.offer_due_date}</h3></span>
                        </div>
                        <div class="col-span-2 bg-slate-50 p-4 rounded-lg">
                            <title class="w-full place-items-center">Terms And Conditions</title>
                            <p>
                                ${job_offer.terms_and_conditions}
                            </p>
                        </div>
                    </div>
                    <div class="w-full h-[4rem] place-items-center mt-4">
                        <div class="w-[12rem] flex justify-between" id="job-offer-confirm-choice">
                            <span class="p-4 bg-primary text-theme_text_color rounded-lg">Accept</span>
                            <span class="p-4 bg-primary text-theme_text_color rounded-lg">Reject</span>                    
                        </div>
                    </div>
                </div>
            `
        )

        $("#job-offer-confirm-choice").on("click", (e)=>{
            const choice =e?.target?.textContent  
            this.update_job_doc(choice, job_offer)    
        })
    }

    async fetch_data(applicant_details){  

        const job_offer =await lite?.connect.x_post("applicants_job_offer", {"applicant_details": applicant_details})
        
        if(job_offer.status ==lite.status_codes.ok){
            this.$job_offer_applicant_details.addClass("hidden")
            this.init_applications(job_offer.data)
            
        }else{
            this.$job_offer_applicant_details.html(`<div class="w-full text-center">Sorry no job offer was found for the creditails provided...</div>`)
        }
        
    }

    submit_details(){
        // this.form_controller =new Form_Controller()


        lite.utils.update_url_parameters ({
            module: "web",
            app: "web",
            page: "info",
            document: "job_offer_confirmation",
            doc: 1,
        })

        
        this.$job_offer_submission.on("click",()=>{
            this.$job_offer_submission.fadeOut(50).fadeIn(50);
            let fields = {};    

            $("#job-offer-applicant-details input").each(function() {
                let key = $(this).attr("id") || $(this).attr("name");                 
                fields[key] = $(this).val();                        
            });
            let missing_fields =0
            
            if(fields.first_name ==""){  
                $("#first_name").css("border", "2px solid red");  
                $("#first_name_missing").removeClass("hidden");             
                $("#first_name_missing").html("Data is missing...");      
                missing_fields +=1       
            }
            if(fields.other_names ==""){      
                $("#other_names").css("border", "2px solid red");   
                $("#other_names_missing").removeClass("hidden");             
                $("#other_names_missing").html("Data is missing...");          
                missing_fields +=1       
            }
            if(fields.applicat_email ==""){
                $("#applicat_email").css("border", "2px solid red");     
                $("#applicat_email_missing").removeClass("hidden");           
                $("#applicat_email_missing").html("Data is missing...");        
                missing_fields +=1       
            }
            if(fields.job_designation ==""){   
                $("#job_designation").css("border", "2px solid red");    
                $("#job_designation_missing").removeClass("hidden");           
                $("#job_designation_missing").html("Data is missing...");          
                missing_fields +=1       
            }

            if(missing_fields ==0){
                this.fetch_data(fields)
            }else{
                return
            }

        })
        
    }
}