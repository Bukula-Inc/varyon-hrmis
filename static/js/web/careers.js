import Form_Controller from "../page/form_controller/index.js";
export default class Careers {
    constructor () {
        this.form_controller = undefined
        this.$opportunities_wrapper = $ ("#opportunities-wrapper")
        this.$field_wrapper = $("#job-application-wrapper")
        this.$application_form_wrapper = $ ("#application-form")
        this.$careers_opportunity_wrapper = $ ("#job-opening-careers")
        this.$opportunity_info = $ ("#opportunity-info")
        this.$job_company = $ ("#job-company")
        this.$job_designation = $ ("#job-designation")
        this.$job_salary = $ ("#job-salary")
        this.$applyBtn = $ ("#apply-for-job")
        this.$enquiry_form = $("#new-career-job-application")
        this.$medical_clearance = $("#_medical_clearance_id")
        this.init_get_medical_clearance()
    }
    
    init(){
        this.opportunities ()
        // this.init_job_application_form()
    }

    // init_job_application_form(){
       
    // }

    init_get_medical_clearance(){
        const site = lite.utils.get_current_app()
        if(site == "medical_clearance"){
            this.get_medical_clearance()
        }
    }


    loadForm () {
        return
        const content_type = lite.utils.get_url_parameters("content_type")
        if (content_type == "careers") {
            this.form_controller = new Form_Controller({
                page_controller: this,
                session: this.session,
                utils: this.utils,
                connect: this.connect,
                alerts: this.alerts,
                lite_date_picker:this.lite_date_picker
            })

            this.apply_for_the_job (this.form_controller)
            this.add_Skill_row()
            this.remove_Skill_row()
            this.add_files()
            this.remove_files()
            this.
            this.form_controller?.init_form()
        }
    }

    opportunity_btns () {
        $.each ($("a[career-open]"), (_, btn) => {
            const $btn = $ (btn)
            $btn.on ("click" , () => {
                this.$opportunities_wrapper.addClass ("hidden")
                this.$opportunity_info.removeClass ("hidden")
                this.get_opportunity ($btn.attr ("career-open"))
            }) 
        })
    }

    async get_opportunity(opportunity_) {
        const opportunity = await lite.connect.x_post("get_job_opening", { name: opportunity_ })
        if (opportunity.status == lite.status_codes.ok) {
            const data = opportunity.data;
  
            $("#job-company").html(data.company || "Company Name Not Available");
   
            $("#job-title").html(`Job Title: ${data.name || data.job_title || 'Not Available'}`);

            $("#job-designation").html(`Designation: ${data.designation || "Not Specified"}`);

            if (data?.publish_salary != 0) {
                $("#job-salary").html(`Salary: ${data.lower_range} - ${data.upper_range} ZMW`);
            } else {
                $("#job-salary").html("Salary: Not Disclosed");
            }
    
            $("#job-description").html(`<b>Job Description:</b> ${data.description ? data.description : 'No Description Available'}`).fadeIn();
            this.init_applications(data.name);
        }
    }
    
    
    

    init_applications (opportunity) {
        this.$applyBtn.off ().on ("click", () => {
            lite.utils.update_url_parameters ({
                app: "web",
                page: "new-form",
                content_type: "careers",
                op: opportunity
            })

            this.$opportunities_wrapper.addClass ("hidden")
            this.$opportunity_info.addClass ("hidden")
            this.$application_form_wrapper.removeClass ("hidden")
            new Form_Controller()
            
        })
    }
    async apply_for_the_job() {
        $("#apply_for_job").on("click", async function(event) {
            event.preventDefault();
            $("#job-page").show();
            const application_data = {
                applicant_first_name: $("#first_name").val().trim(),
                applicant_last_name: $("#last_name").val().trim(),
                email: $("#email").val().trim(),
                mobile: $("#phone").val().trim(),
                designation: $("#position").val().trim(),
                job_opening: $("#job_opening").val().trim(),
                cover_letter: $("#cover_letter").val().trim(),
                job_skills: [],
                documents: []
            };

            $("#skills-container input").each(function() {
                const skill = $(this).val().trim();
                if (skill) {application_data.job_skills.push({skill: skill});}
            });

            const filePromises = [];
            $("#documents-container tr").each(function() {
                const fileInput = $(this).find('input[type="file"]');
                const textInput = $(this).find('input[type="text"]');
                const file = fileInput[0].files[0];  
                if (file) {
                    filePromises.push(new Promise((resolve) => {
                        const reader = new FileReader();
                        reader.onload = function(e) {
                            resolve({
                                qualification: file.name,
                                qualification_type: textInput.val().trim(),
                            });
                        };
                        reader.readAsDataURL(file);
                    }));
                }
            });
    
            application_data.documents = await Promise.all(filePromises);
            const job_application = await lite.connect.x_post("submit_job_application_", application_data);
            if (job_application.status == lite.status_codes.ok) {
                lite.alerts.toast({
                    toast_type: lite.status_codes.ok,
                    title: "Application Submission",
                    message: "Application Submitted Successfully"
                })
            }
            return
           
        });
    }
    
    
    
    remove_Skill_row() {
        $(".remove-skill").on("click", function() {
            const skillsContainer = $("#skills-container");
            if (skillsContainer.children("tr").length > 1) {
                skillsContainer.children("tr").last().remove();
            }
        });
    }
    
    add_Skill_row() {
        $("#add-skill").on("click", function() {
            const newSkillRow = `
                <tr>
                    <td><input type="text" class="border p-2 w-full" placeholder="Enter Skill"/></td>
                </tr>
            `;
            $("#skills-container").append(newSkillRow);
        });
    }
    remove_files() {
        $("#remove-document").on("click", function() {
            const skillsContainer = $("#documents-container");
            if (skillsContainer.children("tr").length > 1) {
                skillsContainer.children("tr").last().remove();
            }
        });
    }
    add_files() {
        $("#add-document").on("click", function() {
            const newSkillRow = `
                <tr>
                    <td><input type="file" class="border p-2 w-full" accept=".pdf,.doc,.docx"/></td>
                     <td><input type="text" class="border p-2 w-full" accept=".pdf,.doc,.docx"/></td>
                </tr>
            `;
            $("#documents-container").append(newSkillRow);
        });
    }
    async get_medical_clearance() {
        const medical_clearance = await lite.connect.x_fetch("get_job_openings"); 
        console.log(medical_clearance);
        
        if (medical_clearance.status === lite.status_codes.ok && medical_clearance.data.medical_clearance || medical_clearance.status === lite.status_codes.ok && medical_clearance.data.medical_clearance.oath_of_secrecy) {
            $('#medical-clearance-doc').append(`
                <div class="bg-white rounded-lg p-4 border border-gray-200">
                    <h2 class="text-lg font-semibold text-gray-800 flex items-center">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5 text-default mr-2">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6m0 0l-3-3m3 3l3-3m-3 3V6m0 9h.01" />
                        </svg>
                        Medical Clearance
                    </h2>
                    <a href="${medical_clearance.data.medical_clearance}" 
                       download 
                       class="mt-3 flex items-center justify-center bg-default text-white px-4 py-2 transition w-full">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5 mr-2">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M4 15v2a2 2 0 002 2h12a2 2 0 002-2v-2M7 10l5 5m0 0l5-5m-5 5V3" />
                        </svg>
                        Download Medical Clearance Form
                    </a>
                </div>
            `);
            $('#oath_of_secrecy-doc').append(`
                <div class="bg-white rounded-lg p-4 border border-gray-200">
                    <h2 class="text-lg font-semibold text-gray-800 flex items-center">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5 text-default mr-2">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6m0 0l-3-3m3 3l3-3m-3 3V6m0 9h.01" />
                        </svg>
                        Oath Of Secrecy
                    </h2>
                    <a href="${medical_clearance.data.oath_of_secrecy}" 
                       download 
                       class="mt-3 flex items-center justify-center bg-default text-white px-4 py-2 transition w-full">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5 mr-2">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M4 15v2a2 2 0 002 2h12a2 2 0 002-2v-2M7 10l5 5m0 0l5-5m-5 5V3" />
                        </svg>
                        Download Medical Clearance Form
                    </a>
                </div>
            `);
        } 
    }
    
    async opportunities () {
        const opportunities = await lite.connect.x_fetch ("get_job_openings")
        if (opportunities.status == lite.status_codes.ok) {
            this.$careers_opportunity_wrapper.html ('')
            if (opportunities.data.job_openings.length > 0) {
                $.each (opportunities.data.job_openings, (_, opportunity) => {                    
                    this.$careers_opportunity_wrapper.append (`
                       <a career-open="${opportunity.job_title}" href="#" 
                        class="block card h-[150px] rounded-md col-span-1 bg-white shadow-md hover:shadow-lg transition duration-300 transform hover:-translate-y-1 p-4 border border-default border-dotted flex items-center gap-4">

                            <!-- Icon -->
                            <div class="h-12 w-12 bg-default/10 flex justify-center items-center rounded-full">
                                <span class="material-symbols-outlined text-default text-2xl">work</span>
                            </div>

                            <!-- Job Details -->
                            <div class="flex-1">
                                <!-- Company -->
                                <h3 class="text-md font-semibold text-default flex items-center gap-2">
                                    <span class="material-symbols-outlined text-default text-sm">business</span> 
                                    <span id="company">${opportunity.company}</span>
                                </h3>

                                <!-- Job Title -->
                                <p class="text-sm text-default font-medium capitalize mt-1">
                                    ${opportunity.job_title}
                                </p>

                                <!-- Designation -->
                                <p class="mt-1 text-sm text-default flex items-center gap-2">
                                    <span class="material-symbols-outlined text-default text-sm">badge</span> 
                                    <b>Designation:</b> <span id="designation">${opportunity.designation}</span>
                                </p>

                                <!-- Salary Range (If Available) -->
                                ${opportunity.salary ? `
                                    <p class="mt-1 text-sm text-default flex items-center gap-2">
                                        <span class="material-symbols-outlined text-default text-sm">attach_money</span> 
                                        <b>Salary:</b> <span id="salary">${opportunity.salary}</span>
                                    </p>` : ''}

                            </div>
                        </a>
                    `)
                })
                this.opportunity_btns ()
            }else {
                this.$careers_opportunity_wrapper.html (`<div class="col-span-3 h-full flex justify-center items-center">
                    <h2 class="mt-8 text-3xl font-bold">There Are No Job Opportunities</h2>
                </div>`)
            }
        }else {
            this.$careers_opportunity_wrapper.html (`<div class="col-span-3 h-full flex justify-center items-center">
                <h2 class="mt-8 text-3xl font-bold">There Are No Job Opportunities</h2>
            </div>`)
        }
    }
}