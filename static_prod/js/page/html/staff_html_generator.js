
export default class Staff_HTML_Generator{
    constructor(){
        this.default_colors = ["indigo", "orange", "teal", "purple", "blue", "green", "cyan","violet","pink"]
    }
    get_random_color(){
        return this.default_colors[Math.floor(Math.random() * this.default_colors.length)]
    }

    create_leave_summary_by_type(title, data){
        return `
            <div class="w-full flex items-center justify-start h-[30px] mb-2 border-b">
                <div class="w-[15px] h-[15px] flex items-center justify-center rounded-full border-[1px] border-indigo-800 bg-indigo-800/10">
                    <div class="w-[5px] h-[5px] flex items-center justify-center rounded-full border-[1px] border-indigo-800 bg-indigo-800"></div>
                </div>
                <span class="ml-2 text-11">${lite.utils.thousand_separator(data?.remaining_days,0)}/${lite.utils.thousand_separator(data?.total_days,0)} ${title}</span>
            </div>
        `
    }

    create_payslip_row(data){
        return `
            <div class="grid grid-cols-11 w-full h-[30px] text-11 rounded-t rounded-md mt-2">
                <span class=" truncate overflow-ellipsis col-span-2 truncate overflow-ellipsis">
                    2023-01-01
                </span>
                <span class="col-span-3 truncate overflow-ellipsis">${data.name}</span>
                <span class=" truncate overflow-ellipsis col-span-2">
                    ${lite.utils.currency(data.gross,lite.system_settings.currency_decimals, data.currency)}
                </span>
                <span class=" truncate overflow-ellipsis col-span-2">
                    ${lite.utils.currency(data.net,lite.system_settings.currency_decimals, data.currency)}
                </span>
                <span class=" truncate overflow-ellipsis col-span-2">
                    <button psid="${data.id}" class="download-payslip text-gray-700 flex items-center">
                        Download
                        <span class="material-symbols-outlined ml-2 text-indigo-600">download</span>
                    </button>
                </span>
            </div>
        `
    }
    payslips_infor(data) {
        let html = "";
        data.forEach(payslip => {
            html += `
                <div class="w-full border-b flex justify-between text-[11px] font-medium text-gray-800 py-1 px-2">
                    <div class="flex items-center gap-1 flex-[1.5] whitespace-nowrap min-w-[110px]">
                        <span class="material-symbols-outlined text-orange-600 text-sm">event_available</span>
                        ${payslip.created_on}
                    </div>
                    <div class="flex items-center gap-1 flex-1 whitespace-nowrap min-w-[90px]">
                        <span class="material-symbols-outlined text-purple-500 text-sm">add_card</span>
                        ${payslip.net}
                    </div>
                    <div class="flex items-center gap-1 flex-1 whitespace-nowrap min-w-[90px]">
                        <span class="material-symbols-outlined text-indigo-600 text-sm">attach_money</span>
                        ${payslip.ytd_deductions}
                    </div>
                    <div class="flex items-center gap-1 flex-1 whitespace-nowrap min-w-[90px]">
                        <span class="material-symbols-outlined text-emerald-500 text-sm">receipt_long</span>
                        ${payslip.ytd_gross}
                    </div>
                </div>
            `;
        });
        return html;
    }
    recent_leave_applications(data){
        let html = "";
        data.forEach(leave=>{
            html += `
                <div class="leave-applications-list grid gap-4">
                <!-- Leave Card 1 -->
                <div class="leave-card bg-white rounded-lg shadow-md p-4 border-l-4 border-blue-500 hover:shadow-lg transition-shadow">
                    <div class="flex justify-between items-start">
                        <div>
                            <span class="text-gray-500 text-sm">${leave.from_date}</span>
                            <h4 class="font-semibold text-gray-800 mt-1">Vacation</h4>
                        </div>
                        <span class="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full">Days ${leave.total_days}</span>
                    </div>
                    <div class="mt-3 flex items-center text-gray-600">
                        <span class="material-symbols-outlined text-sm mr-1">event</span>
                        <span class="text-sm">${leave.leave_type}</span>
                    </div>
                </div>

               
            </div>
    
            
            `
        })
    }
    recent_grievance(data){
        let html = "";
        data.forEach(grievance => {
            html += `
                <div class="w-full grid grid-cols-9 h-[45px] border-b rounded-t-md text-12 font-semibold">
                    <div class="w-full flex items-center justify-start h-full col-span-3 pl-2">
                        <span class="material-symbols-outlined mr-1 text-orange-600">
                            event_available
                        </span>
                        ${grievance.date_created}
                    </div>
                    <div class="w-full flex items-center justify-start h-full col-span-3">
                        <span class="material-symbols-outlined mr-1 text-purple-500">
                            person_remove
                        </span>
                        ${grievance.employee_name}
                    </div>
                    <div class="w-full flex items-center justify-start h-full col-span-3">
                        <span class="material-symbols-outlined mr-2 text-indigo-600">
                            toggle_on
                        </span>
                        ${grievance.status}
                    </div>
                </div>
            `;
        });
        return html;
    }


    staff_stats_infor(data) {
        return `
            <div class="rounded-2xl p-6 w-full h-full flex flex-col relative transition-all">
            
            <!-- Status Badge -->
            <div class="absolute top-4 right-4 flex items-center bg-green-100 text-default px-3 py-1 rounded-full text-xs font-semibold">
                <div class="relative flex h-2.5 w-2.5 mr-1">
                    <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-700 opacity-75"></span>
                    <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-default"></span>
                </div>
                Active
            </div>

            <!-- Avatar -->
            <div class="flex justify-center mb-5 mt-2 relative">
                <div class="relative group">
                    <div class="absolute inset-0 bg-default rounded-full blur-lg opacity-10 group-hover:opacity-30 transition-all duration-500"></div>
                    <div class="h-24 w-24 rounded-full overflow-hidden border-4 border-white">
                        <img src="/media/defaults/avatas/db.jpeg" class="h-full w-full object-cover" alt="Avatar">
                    </div>
                    <div class="absolute bottom-0 right-0 bg-white rounded-full p-1 shadow-md">
                        <div class="bg-blue-500 rounded-full p-1">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                            </svg>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Name & Role -->
            <div class="text-center">
                <h2 class="text-2xl font-semibold text-white">${data.full_name}</h2>
                <p class="text-sm text-white font-medium mt-0.5">Senior Software Developer</p>
                <p class="text-xs text-default mt-1">ID: ${data.emp_id}</p>
            </div>

            <!-- Quick Stats -->
            <div class="mt-5 grid grid-cols-3 gap-3 text-center bg-white border border-gray-200 rounded-xl py-3 px-4 shadow-sm">
                <div>
                    <div class="text-xs text-default">Years</div>
                    <div class="text-base font-bold text-gray-700">-</div>
                </div>
                <div class="border-x border-gray-200 px-2">
                    <div class="text-xs text-default">Projects</div>
                    <div class="text-base font-bold text-purple-600">-</div>
                </div>
                <div>
                    <div class="text-xs text-default">Rating</div>
                    <div class="flex items-center justify-center font-bold text-yellow-500 text-base">
                        -
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-0.5" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                        </svg>
                    </div>
                </div>
            </div>

            <!-- Info List -->
            <div class="mt-6 space-y-3 text-sm">
                <div class="flex items-center justify-between bg-purple-50 py-2 px-3 rounded-lg shadow-sm">
                    <span class="flex items-center text-default">
                        <svg class="w-4 h-4 mr-2 text-purple-700" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16" />
                        </svg>
                        Department
                    </span>
                    <span class="font-medium text-default">${data.department}</span>
                </div>

                <div class="flex items-center justify-between bg-purple-50 py-2 px-3 rounded-lg shadow-sm">
                    <span class="flex items-center text-default">
                        <svg class="w-4 h-4 mr-2 text-purple-700" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                        </svg>
                        NRC
                    </span>
                    <span class="font-medium text-default">${data.id_nrc}</span>
                </div>

                <div class="flex items-center justify-between bg-purple-50 py-2 px-3 rounded-lg shadow-sm">
                    <span class="flex items-center text-default">
                        <svg class="w-4 h-4 mr-2 text-purple-700" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M3 5a2 2 0 012-2h3.28l1.498 4.493a1 1 0 01-.502 1.21L7.02 10.83a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502L19 17v2a2 2 0 01-2 2H5a2 2 0 01-2-2V5z" />
                        </svg>
                        Contact
                    </span>
                    <span class="font-medium text-default">${data.contact_no || "-"}</span>
                </div>

                <div class="flex items-center justify-between bg-purple-50 py-2 px-3 rounded-lg shadow-sm">
                    <span class="flex items-center text-default">
                        <svg class="w-4 h-4 mr-2 text-purple-700" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8" />
                        </svg>
                        Email
                    </span>
                    <span class="font-medium text-default truncate max-w-[130px]">${data.email}</span>
                </div>
            </div>
        </div>


           
        `;
    }


    overtime(data){
        let overtime = ''
        $.each(data,(index, value)=>{
            if (index <= 5) {
                overtime += `
                   <div class="w-full h-[45px] flex items-center justify-between border-b">
                   <div class="flex items-center justify-start">
                       <div class="flex items-ceenter justify-center mr-3">
                           <span class="material-symbols-outlined text-default text-17"> check_circle </span>
                       </div>
                       <div class="text-gray-700">${value.applicant_name}</div>
                   </div>
                   <div class="flex flex-col items-end justify-center">
                       <span class="font-semibold text-12">
                           <span class="material-symbols-outlined text-13 mr-1"> calendar_month </span>
                           ${value.overtime_date}
                       </span>
                       <small class="text-orange-500 text-10">Applied</small>
                   </div>
              </div>   `
            }
        })
        return overtime
    }

    imprest(data){
        let imprest = ''
        $.each(data,(index, value)=>{
            if (index <= 5) {
                imprest += `
                   <div class="w-full h-[45px] flex items-center justify-between border-b">
                   <div class="flex items-center justify-start">
                       <div class="flex items-ceenter justify-center mr-3">
                           <span class="material-symbols-outlined text-default text-17"> check_circle </span>
                       </div>
                       <div class="text-gray-700">${value.name}</div>
                   </div>
                   <div class="flex flex-col items-end justify-center">
                       <span class="font-semibold text-12">
                           <span class="material-symbols-outlined text-13 mr-1"> calendar_month </span>
                           ${value.date}
                       </span>
                       <small class="text-orange-500 text-10">Applied</small>
                   </div>
              </div>   `
            }
        })
        return imprest
    }
    staff_project_task(data){
        let project_task = ''
        $.each(data,(index, value)=>{
            if (index <= 5) {
                project_task += `
                   <div class="w-full h-[45px] flex items-center justify-between border-b">
                   <div class="flex items-center justify-start">
                       <div class="flex items-ceenter justify-center mr-3">
                           <span class="material-symbols-outlined text-default text-17"> check_circle </span>
                       </div>
                       <div class="text-gray-700">${value.task_name}</div>
                   </div>
                   <div class="flex flex-col items-end justify-center">
                       <span class="font-semibold text-12">
                           <span class="material-symbols-outlined text-13 mr-1"> calendar_month </span>
                           ${value.creation_date}
                       </span>
                       <small class="text-orange-500 text-10">Created</small>
                   </div>
              </div>   `
            }
        })
        return project_task
    }

    leave_breakdown (data) {
        let leave_card = ""
        $.each (data, (_, leave_type) => {
            if (_ <= 7) {
                const color = this.get_random_color ()
                leave_card += `
                    <div class="rounded-md bg-${color || "indigo"}-300/20">
                        <div class="h-full w-full flex justify-center flex-col items-center">
                            <p class="text-[9px]">${leave_type.leave_type}</p>
                            <div class="flex justify-center item-center flex-col">
                                <p class="font-semibold slate-600 text-[9px]">Available: ${leave_type.remaining_days} days</p>
                            </div>
                        </div>
                    </div> 
                `
            }
        })
        return leave_card
    }

    staff_appraisal(data) {
        let staff_appraisal = '';
        $.each(data, (index, value) => {
            if (index <= 5) {
                staff_appraisal += `
                    <div class="w-full h-full text-13 mt-1 pending-appraisals">
                        <a href="" class="w-full flex items-center justify-between mt-2">
                            <span class="flex items-center justify-start text-13 name">
                                <span class="material-symbols-outlined text-18 mr-1 text-orange-800"></span>
                                ${value.name}
                            </span>
                            <span class="flex items justify-end appraisal-date">
                                ${value.appraisal_date}
                                <span class="material-symbols-outlined text-15 ml-2"></span>
                            </span>
                        </a> 
                    </div>
                `;
            }
        });
        return staff_appraisal;
    }


}