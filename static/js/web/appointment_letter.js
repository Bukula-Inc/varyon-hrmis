;
import Form_Controller from "../page/form_controller/index.js";
export default class Appointment_Letter
 {
    constructor () {
        this.$appointment =$ ("#appointment-letter-confirmation-careers")
        this.$appointment_letter_confirmation_careers_visible_body =$("#appointment-letter-confirmation-careers-visible-body")
        this.$appointment_letter_applicant_details = $("#appointment-letter-applicant-details")
        this.$appointment_letter_submission =$ ("#appointment-details-submission")
        this.submit_details()
        // this.form_controller =undefined
    }
    // loadForm () {
    //     const document = lite.utils.get_url_parameters ("document")
        
    //     if (document == "appointment_confirmation") {
    //         this.form_controller = new Form_Controller({
    //             page_controller: this,
    //             session: this.session,
    //             utils: this.utils,
    //             connect: this.connect,
    //             alerts: this.alerts,
    //             lite_date_picker:this.lite_date_picker
    //         })
    //         this.form_controller?.init_form()
    //     }
    
    // }

    async update_job_doc(choice, appointment_doc, reporting_date){
        let doc_update =null
        
        if(choice =="Accept"){
            doc_update =await lite?.connect?.x_post("appointment_letter_confirmation", {"id": appointment_doc.id, "response": choice, "date": reporting_date}) 
        }else{
            this.$appointment_letter_confirmation_careers_visible_body.html(`<div class="w-full text-center">Thank you for response.</div>`)    
        }
        this.$appointment_letter_confirmation_careers_visible_body.addClass("place-content-center")
        $("#appointment-letter-confirmation-page").remove()
        this.$appointment_letter_applicant_details.removeClass("hidden")
        if(doc_update){
            if(doc_update.status ==lite?.status_codes.ok){
                this.$appointment_letter_confirmation_careers_visible_body.html(`<div class="w-full text-center">You Feedback was successfully Submitted. Thank you for response.</div>`)
            }else{
                this.$appointment_letter_confirmation_careers_visible_body.html(`<div class="w-full text-center">Thank you for response.</div>`)
            }
        }
    }

    init_applications (appointment) {

        this.$appointment_letter_confirmation_careers_visible_body.removeClass("place-content-center")
        this.$appointment_letter_confirmation_careers_visible_body.html(
            `
                <div class="h-full w-full" id="appointment-letter-confirmation-page">
                    <div class="grid grid-cols-2 gap-4 p-4 text-secoundary">
                        <div class="span-col-1">
                            <span class="flex text-lg my-2">Applicant Name : <h3 class="bg-slate-50 rounded-lg font-semibold ml-[1rem] px-4" id="appointment-letter-applicant-name">${appointment.applicant}</h3></span>
                            <span class="flex text-lg my-2">Applicant Email : <h3 class="bg-slate-50 rounded-lg font-semibold ml-[1rem] px-4" id="appointment-letter-applicant-name">${appointment.applicant_email}</h3></span>
                        </div>
                        <div class="span-col-1">
                            <span class="flex text-lg my-2">Company: <h3 class="bg-slate-50 rounded-lg font-semibold ml-[1rem] px-4" id="appointment-letter-applicant-name">${appointment.company}</h3></span>
                            <span class="flex text-lg my-2">Designation: <h3 class="bg-slate-50 rounded-lg font-semibold ml-[1rem] px-4" id="appointment-letter-applicant-name">${appointment.designation}</h3></span>
                            <span class="flex text-lg my-2">Issue Date: <h3 class="bg-slate-50 rounded-lg font-semibold ml-[1rem] px-4" id="appointment-letter-applicant-name">${appointment.date}</h3></span>
                            <span class="flex text-lg my-2">Your Date Of Reporting : <h3 class="bg-slate-50 rounded-lg font-semibold ml-[1rem] px-4" id="appointment-letter-applicant-name"><input type="text" name="reporting_date" placeholder="YYYY-mon-day" class="border-none" id="reporting_date_by_applicant"/></h3></span>
                        </div>
                        <div class="col-span-2 bg-slate-50 p-4 rounded-lg">
                            <title class="w-full place-items-center">Terms And Conditions</title>
                            <p>
                                ${appointment.appointment_context}
                            </p>
                        </div>
                    </div>
                    <div class="w-full h-[4rem] place-items-center mt-4">
                        <div class="w-[12rem] flex justify-between" id="appointment-letter-confirm-choice">                   
                            <span class="p-4 bg-primary text-theme_text_color rounded-lg">Accept</span>
                            <span class="p-4 bg-primary text-theme_text_color rounded-lg">Reject</span>                    
                        </div>
                    </div>
                </div>
            `
        )

        $("#appointment-letter-confirm-choice").on("click", (e)=>{
            const choice =e?.target?.textContent  
            const reporting_date =$("#reporting_date_by_applicant").val()

            console.log(reporting_date)         
            this.update_job_doc(choice, appointment, reporting_date)    
        })
    }

    async fetch_data(applicant_details){  
        
        const appointment =await lite?.connect.x_post("appointment_letter_approval", applicant_details)
        
        if(appointment.status ==lite.status_codes.ok){
            this.$appointment_letter_applicant_details.addClass("hidden")
            this.init_applications(appointment.data)
            
        }else{
            this.$appointment_letter_applicant_details.html(`<div class="w-full text-center">Sorry no job offer was found for the creditails provided...</div>`)
        }
        
    }

    submit_details(){
        // this.form_controller =new Form_Controller()
        this.$appointment_letter_submission.on("click",()=>{
            this.$appointment_letter_submission.fadeOut(50).fadeIn(50);
            let fields = {};    

            $("#appointment-letter-applicant-details input").each(function() {
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