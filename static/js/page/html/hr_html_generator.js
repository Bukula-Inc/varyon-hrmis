

export default class HR_HTML_Generator{
    constructor(){
        this.default_colors = ["indigo", "orange", "teal", "purple", "blue", "green", "cyan","violet","pink"]
    }

    leave_review_stats (data) {
        let list = ''
        if (data.length > 0) {
            $.each (data, (_, item) => {
                if (_< 5) {
                    list += ``
                }
            })
        }
        return list
    }
    leave_commutation(data){
        let leave_card = ``
        if (data.length>0){
            $.each(data,  (index, value) => { 
                if (index< 12) {
                    leave_card += `
                    <div class="flex flex-col">
                        <div class="flex items-center gap-2 mb-2">
                        <div class="bg-teal-400 h-4 w-4 rounded-md shadow-sm"></div>
                        <div class="text-sm">${value.name}</div>
                        </div>
                        <div class="flex justify-between ml-6">
                        <div class="flex gap-2 items-center">
                            <p class="text-xs text-gray-500">Total Commutable Days:</p>
                            <p class="text-sm font-semibold text-gray-800">${value.total_commutable_days}</p>
                        </div>
                        <div class="flex gap-2 items-center">
                            <p class="text-xs text-gray-500">Value:</p>
                            <p class="text-sm font-semibold text-gray-800">${value.total_value}</p>
                        </div>
                        </div>
                    </div>
                    `
                }
            });
        }
        return leave_card
    }
    recent_welfare(data){
        let leave_card = ``
        if (data.length>0){
            $.each(data,  (index, value) => { 
                if (index< 12) {
                    leave_card += `
                    <div class="flex-1">
                        <div class="flex justify-between items-start">
                            <h4 class="font-medium text-gray-800">${value.welfare_type}</h4>
                        </div>
                        <div class="flex gap-2">
                            <div class="flex rounded-full bg-gray-200 border border-default w-[28px] h-[28px]">
                                <img src="/media/defaults/avatas/dp.jpeg" class="w-full h-full rounded-full object-cover object-top" alt="">
                            </div>
                            <p class="text-sm text-gray-600 mt-1">${value.employee_name}</p>
                        </div>
                        <div class="flex justify-between items-center mt-2">
                            <div class="text-sm text-gray-600">
                                <span>Total Expense: </span>
                                <span class="font-medium text-default">${value.welfare_expense}</span>
                                <span class="text-xs text-gray-500 ml-2">(Staff Covered: <strong class="text-default">${value.staff_covered_expense}</strong>)</span>
                            </div>
                        </div>
                    </div>
                    `
                }
            });
        }
        return leave_card
    }
    training_program(data){
        let training_program = ``
        if (data.length>0){
            $.each(data,  (index, value) => { 
                if (index< 12) {
                    training_program += `
                        <div class="w-full grid grid-cols-4 border-b h-auto text-12 p-2 intro-x">
                            <div class="col-span-2 flex flex-col">
                                <label class="text-gray-600 text-xs mb-1">Training Program</label>
                                <a href="#" class="w-full flex items-center justify-start h-full">
                                    <span class="material-symbols-outlined mr-1 text-orange-600">
                                        event_available
                                    </span>
                                    ${value.Training_Program}
                                </a>
                            </div>
                            <div class="flex flex-col">
                                <label class="text-gray-600 text-xs mb-1">Number of Attendees</label>
                                <div class="w-full flex items-center justify-start h-full">
                                    <span class="material-symbols-outlined mr-1">
                                        trending_up
                                    </span>
                                    ${value.Number_of_Attendees}
                                </div>
                            </div>
                        </div>

                    `
                }
            });
        }
        return training_program
    }

    recent_grieves(data){
        let grievance = ``
        if (data.length>0){
            $.each(data,  (index, value) => { 
                if (index< 12) {
                    grievance += `
                        <div class="flex items-center bg-white w-full border-b py-1 rounded-lg transition-all duration-300">
                            <img src="/media/defaults/avatas/dp.jpeg" alt="Aaron Mubanga" class="w-12 h-12 rounded-full border-2 border-indigo-800 dark:border-blue-900 mr-2">
                            <div>
                                <h3 class="text-[12px] font-semibold text-slate-700">${value.employee_name}</h3>
                                <p class="text-[9px] text-gray-600 ">${value.department}</p>
                            </div>
                        </div>
                    `
                }
            });
        }
        return grievance
    }

    recent_actions(data){
        let grievance = ``
        if (data.length>0){
            $.each(data,  (index, value) => { 
                if (index< 12) {
                    grievance += `
                        <a href="#"
                            class="bg-gray-100 flex-grow border-l-8 border-red-500 rounded-md px-3 py-2 w-full">
                            ${value.action}
                            <div class="text-slate-800 font-thin text-[9px]">
                                <span class="w-16 truncate">Grievence: ${value.name}</span>
                                </br>
                                <span>Date: ${value.date}</span>
                            </div>
                        </a>
                    `
                }
            });
        }
        return grievance
    }

    degree_holder(data){
        let degree_emps =``
        if (data.length>0){
            $.each(data,  (index, value) => { 
                if (index< 12) {
                    degree_emps += `
                    <div class="flex items-center gap-4 bg-white p-4 rounded-lg">
                        <span class="material-symbols-outlined text-default text-4xl">person</span>
                        <div>
                            <h3 class="text-lg font-semibold text-gray-800">${value.employee_name}</h3>
                            <p class="text-sm text-default">
                                <strong class="font-medium">Job Title:</strong> ${value.designation}
                            </p>
                        </div>
                    </div>

                    `
                }
            });
        }
        return degree_emps 
    }
    masters_data(data){
        let masters_degr =``
        if (data.length>0){
            $.each(data,  (index, value) => { 
                if (index< 12) {
                    masters_degr += `
                    <div class="flex items-center gap-4 bg-white p-4 rounded-lg">
                    <span class="material-symbols-outlined text-default text-4xl">person</span>
                    <div>
                        <h3 class="text-lg font-semibold text-gray-800">${value.employee_name}</h3>
                        <p class="text-sm text-default">
                            <strong class="font-medium">Job Title:</strong> ${value.designation}
                        </p>
                    </div>
                </div>

                    `
                }
            });
        }
        return masters_degr 
    }
    diploma_data(data){
        let diploma_holder =``
        if (data.length>0){
            $.each(data,  (index, value) => { 
                if (index< 12) {
                    diploma_holder += `
                    <div class="flex items-center gap-4 bg-white p-4 rounded-lg">
                        <span class="material-symbols-outlined text-default text-4xl">person</span>
                        <div>
                            <h3 class="text-lg font-semibold text-gray-800">${value.employee_name}</h3>
                            <p class="text-sm text-default">
                                <strong class="font-medium">Job Title:</strong> ${value.designation}
                            </p>
                        </div>
                    </div>

                    `
                }
            });
        }
        return diploma_holder 
    }
    certificate_data(data){
        let diploma_holder =``
        if (data.length>0){
            $.each(data,  (index, value) => { 
                if (index< 12) {
                    diploma_holder += `
                     <div class="flex items-center gap-4 bg-white p-4 rounded-lg">
                        <span class="material-symbols-outlined text-default text-4xl">person</span>
                        <div>
                            <h3 class="text-lg font-semibold text-gray-800">${value.employee_name}</h3>
                            <p class="text-sm text-default">
                                <strong class="font-medium">Job Title:</strong> ${value.designation}
                            </p>
                        </div>
                    </div>

                    `
                }
            });
        }
        return diploma_holder 
    }
    up_coming_interviews(data){
        let interviews =``
        if (data.length>0){
            $.each(data,  (index, value) => { 
                if (index< 12) {
                    interviews += `
                    <div class="grid grid-cols-2 items-center p-3 border-b border-default">
                        <div class="flex items-center gap-3">
                            <div class="bg-purple-600 h-6 w-6 rounded-full"></div>
                            <div class="text-sm text-gray-900 font-semibold tracking-wide">${value.employee_name}</div>
                        </div>
                        <div class="text-sm font-medium text-purple-700 text-right bg-purple-100 px-3 py-1 rounded-md flex items-center justify-center shadow">
                            <i class="material-symbols-outlined text-purple-700 text-lg mr-1">calendar_today</i>
                            2024-01-24
                        </div>
                    </div>

                    `
                }
            });
        }
        return interviews
    }
    unsettled_employees (data) {
        let unsettled_final_st =``
        if (data.length>0){
            $.each(data,  (index, value) => { 
                console.log(value);
                
                if (index< 12) {
                    unsettled_final_st += `
                    <div class="w-full h-[50px] flex items-center justify-between border-b border-gray-200 bg-gray-50 hover:bg-gray-100 transition-colors rounded-md p-2">
                        <div class="flex items-center space-x-3">
                            <!-- Icon -->
                            <div class="flex items-center justify-center bg-green-100 rounded-full p-1">
                                <span class="material-symbols-outlined text-green-600 text-2xl">check_circle</span>
                            </div>
                            <!-- Employee Name -->
                            <div class="text-gray-800 font-medium text-sm sm:text-base">
                                ${value.employee_name}
                            </div>
                        </div>

                    </div>
                    `
                }
            });
        }
        return unsettled_final_st
    }
    leave_history (data) {
        let tb_row = ''
        if (data.length > 0) {
            $.each (data, (_, row) => {
                if (_< 10) {
                    tb_row += `
                        <div class="grid grid-cols-13 w-full h-[45px] bg-gray-100/50 p-2 text-11 rounded-t rounded-md mt-2">
                            <span class="flex items-center justify-start col-span-1">
                                ${row.id}
                            </span>
                            <span class="flex items-center justify-start col-span-2">
                                ${row.leave_dates}
                            </span>
                            <span class="flex items-center justify-start col-span-2">
                                ${row.leave_types}
                            </span>
                            <span class="flex items-center justify-start col-span-4">
                                ${row.leave_notes}
                            </span>
                            <span class="flex items-center justify-start col-span-2">
                                <span class="p-[5px] rounded-md bg-[${row.leave_status.status_color}] text-[${row.leave_status.inner_color}]">
                                    ${row.leave_status.name}
                                </span>
                            </span>

                            <span class="flex items-center justify-start col-span-2">
                                28 May, 2024
                            </span>
                        </div>
                    `
                }
            })
        }
        return tb_row
    }

    get_random_color(){
        return this.default_colors[Math.floor(Math.random() * this.default_colors.length)]
    }

    separated_employees (list) {
        let list_card = ""
        if (list.length > 0) {
            $.each (list, (_, item) => {
                if (_ <= 6) {
                    list_card += `
                        <div class="w-full h-[45px] flex items-center justify-between border-b">
                            <div class="flex items-center justify-start">
                                <div class="flex items-ceenter justify-center mr-3">
                                    <span class="material-symbols-outlined text-default text-17"> check_circle </span>
                                </div>
                                <div class="text-gray-700">${item.employee_name}</div>
                            </div>
                        </div>
                    `
                }
            }) 
        }

        return list_card
    }
    interviews_this_week(data){
        let interview = ''
        $.each(data,(index,value)=>{
            if(index <=4){
                interview += `
                <span class="font-semibold flex items-center">
                    <span class="material-symbols-outlined text-[14px] mr-1 text-orange-600">
                        total_dissolved_solids
                    </span>
                    <small class="whitespace-nowrap">${value.applicant_name}</small>
                    <small class="text-slate-500 ml-5 w-[90%] whitespace-nowrap">
                        ${value.schedule_date}
                    </small>
                </span>

                `
            }
        })

        return interview
    }
    leave_type_side_view (data) {
        let card = ""
        if (lite.utils.array_has_data (data)) {
            $.each (data, (_, element) => {
                if (_ <= 17) {
                    card += `
                        <div class="w-full h-[40px] flex items-center justify-between">
                            <div class="flex items-center justify-start">
                                <div class="flex ietms-center justify-center relative w-[30px] h-[20px] mr-1">
                                    <div class="absolute w-[15px] h-[15px] border-2 border-orange-600 rounded-md rotate-[50deg] mt-1"></div>
                                    <div class="absolute w-[15px] h-[15px] border-2 border-indigo-600 rounded-md rotate-[40deg]"></div>
                                </div>
                                <span>${element.leave_type}</span>
                            </div>
                            <div>
                                ${element.pending_count}
                            </div>
                        </div>
                    `
                }
            })
        }
        return card
    }

    // for the dashboard
    create_employee_by_department_card(key, value){
        const color = this.get_random_color()
        return `
            <div class="w-full flex items-center justify-between h-[60px] intro-y">
                <div class="flex items-center justify-start">
                    <div class="flex items-center justify-center  w-[40px] h-[40px] rounded-md bg-${color||"indigo"}-100 mr-2">
                        <span class="material-symbols-outlined text-23 text-${color||"indigo"}-800 .material-symbols-outlined-hidden">
                            work_history
                        </span>
                    </div>
                    <h6 class="truncate overflow-ellipsis">${key}</h6>
                </div>
                <div class="flex items-center justify-center font-bold mr-2 text-12 flex flex-col">
                    ${value}
                    <small class="text-gray-500">Employees</small>
                </div>
            </div>
        `
    }

    create_employee_designation_card(key, value){
        const color = this.get_random_color()
        return `
            <div class="border border-b-none w-full h-full p-3 intro-y bg-${color||"indigo"}-50">
                <div class="flex items-center justify-start">
                    <div class="w-[10px] h-[10px] rounded-full bg-${color||"indigo"}-700 mr-2">
                    </div>
                    <span class="truncate overflow-ellipsis text-12">${key}</span>
                </div>
                <small class="ml-4 text-gray-500 font-semibold">${value} Employee${value > 1 || value == 0 ? "s":""}</small>
            </div>
        `
    }

    create_employee_file_group_card(){
        return `
        <div class="file box px-5 py-3 mb-3 flex items-center shadow-none">
            <div class="w-7 file__icon file__icon--directory"></div>
            <div class="ml-4 mr-auto">
                <div class="font-medium">Employee Files</div>
                <div id="employee-files" class="text-slate-500 text-xs mt-1"></div>
            </div>
        </div>
        `
    }




    create_department_employees(data){
        let cards= ''
        const colors = ['bg-indigo-700', 'bg-[#F175E8]', 'bg-orange-600', 'bg-emerald-700', 'bg-purple-600', 'bg-[#f683ae]']
        $.each(data,(index, value)=>{
            if (index <= 5) {
                cards += `
                    <div class="border w-full h-full p-3 bgs-[#F6EAF5]">
                        <div class="flex items-center justify-start">
                            <div class="w-[10px] h-[10px] rounded-full ${colors[index]} mr-2">
                            </div>
                            <span class="">${value.department_name}</span>
                        </div>
                        <small class="ml-4 text-gray-700">${value.num_employees} Employees</small>
                    </div>
                `
            }
        })
        return cards
    }

    create_employment_type(data){
        let box= ''
        const icons = ['diversity_2', 'contract_edit', 'business_center', 'draw_abstract', 'On Part Time']
        const colors = ['bg-blue-100', 'bg-orange-100', 'bg-emerald-100', 'bg-indigo-100', 'bg-teal-100']
        $.each(data,(index, value)=>{
            if (index <=5){
                box += `
                <div class="w-full flex items-center justify-between h-[60px]">
                    <div class="flex items-center justify-start">
                        <div
                            class="flex items-center justify-center  w-[40px] h-[40px] rounded-md ${colors[index]} mr-2">
                            <span class="material-symbols-outlined text-23 text-orange-900">
                            ${icons[index]}
                            </span>
                        </div>
                        <h6>${value.employment_name}</h6>
                    </div>
                    <div class="flex items-center justify-center font-bold">${value.employment_employees}</div>
                </div>`
            }
        })
        return box
    }

    designation_card(data){
        let designation = ''
        // const icons = ['bar-chart-2', 'activity', 'calendar', 'calendar']
        // const colors = ['text-red-600', 'text-default', 'text-red-700', 'text-red-700']

        $.each(data,(index,value)=>{
            if(index <=4){
                designation += `
                <div class="flex items-center justify-between my-6">
                    <div class="flex items-center justify-start">
                        <i data-lucide="bar-chart-2" class="w-[17px] h-[17px] mr-2 text-default"></i>
                        ${value.designation_name}
                    </div>
                    <div class="text-gray-700 font-semibold text-[12px]">${value.number_of_employees}</div>
                </div>`
            }
        })

        return designation
    }

    employee_designation(data){
        let employee = ''

        $.each(data,(index,ele)=>{
            if (index <=7){
                employee += ` 
               <div class="flex items-center justify-between p-2">
                    <div class="flex items-center">
                        <div class="flex items-center justify-center relative w-[30px] h-[20px] mr-1">
                            <div class="absolute w-[15px] h-[15px] border-2 border-orange-600 rounded-md rotate-[50deg] mt-1"></div>
                            <div class="absolute w-[15px] h-[15px] border-2 border-indigo-600 rounded-md rotate-[40deg]"></div>
                        </div>
                        <span>${ele?.label}</span>
                    </div>
                    <div class="rounded-full bg-gray-100 font-bold flex items-center justify-center w-[25px] h-[25px]">
                        ${ele?.value}
                    </div>
                </div>
          `
            }
        })
        return employee
    }

    department_checkin(data){
        let checkin= ''
        $.each(data,(index, value)=>{
            if (index <= 5) {
                checkin += `
                <div class="flex items-center justify-between my-6">
                    <div class="flex items-center justify-start">
                    <i data-lucide="activity" class="w-[17px] h-[17px] mr-2 text-red-600"></i>
                    ${value.department_name}
                    </div>
                    <div class="text-gray-700 font-semibold text-[12px]">${value.number_of_employees}</div>
                </div>
                `
            }
        })
        return checkin
    }


    promoted_employees(data){
        let promotion= ''
        $.each(data,(index, value)=>{
            if (index <= 6) {
                promotion += `
                <div class="w-full h-[45px] flex items-center justify-between border-b">
                    <div class="flex items-center justify-start">
                        <div class="flex items-ceenter justify-center mr-3">
                            <span class="material-symbols-outlined text-default text-17"> check_circle </span>
                        </div>
                        <div class="text-gray-700"> ${value.employee_name}</div>
                    </div>
                    <div class="flex flex-col items-end justify-center">
                        <span class="font-semibold text-12">
                            <span class="material-symbols-outlined text-13 mr-1"> calendar_month </span>
                            ${value.date}
                        </span>
                        <small class="text-orange-500 text-10">Promoted</small>
                    </div>
               </div>
                `
            }
        })
        return promotion
    }

    allocation_view(data){
        let allocate= ''
        $.each(data, (index, value)=>{
            if (index <= 4) {
                allocate += `
                    <div class="w-full h-[45px] flex items-center justify-between border-b space-y-8">
                        <div class="flex items-center justify-start">
                            <div class="flex items-ceenter justify-center mr-3">
                                <span class="material-symbols-outlined text-default text-17"> check_circle </span>
                            </div>
                            <div class="text-gray-700">${value.employee_name}</div>
                        </div>
                        <div class="flex flex-col items-end justify-center">
                            <span class="font-semibold text-12">
                                <span class="material-symbols-outlined text-13 mr-1"> calendar_month </span>
                                ${value.total_leaves_allocated}
                            </span>
                            <small class="text-orange-500 text-10">Completed</small>
                        </div>
                    </div>
                `
            }
        })
        return allocate
    }

    appraisal_setup(data) {
        let setup = '';
        $.each(data, (index, value) => {
            if (index <= 6) {
                setup += `
                <div class="w-full h-[45px] flex items-center justify-between border-b">
                    <div class="flex items-center justify-start">
                        <div class="flex items-center justify-center mr-3">
                            <span class="material-symbols-outlined text-default text-17"> check_circle </span>
                        </div>
                        <div class="text-gray-700">In Draft</div>
                    </div>
                    <div class="flex flex-col items-end justify-center">
                        <span class="font-semibold text-12">
                            <span class="material-symbols-outlined text-13 mr-1"></span>
                            ${value.draft}
                        </span>
                    </div>
                </div>
                <div class="w-full h-[45px] flex items-center justify-between border-b">
                    <div class="flex items-center justify-start">
                        <div class="flex items-center justify-center mr-3">
                            <span class="material-symbols-outlined text-default text-17"> check_circle </span>
                        </div>
                        <div class="text-gray-700">Submitted</div>
                    </div>
                    <div class="flex flex-col items-end justify-center">
                        <span class="font-semibold text-12">
                            <span class="material-symbols-outlined text-13 mr-1"></span>
                            ${value.submitted}
                        </span>
                    </div>
                </div>
                     <div class="w-full h-[45px] flex items-center justify-between border-b">
                    <div class="flex items-center justify-start">
                        <div class="flex items-center justify-center mr-3">
                            <span class="material-symbols-outlined text-default text-17"> check_circle </span>
                        </div>
                        <div class="text-gray-700">Cancelled</div>
                    </div>
                    <div class="flex flex-col items-end justify-center">
                        <span class="font-semibold text-12">
                            <span class="material-symbols-outlined text-13 mr-1"></span>
                            ${value.cancelled}
                        </span>
                    </div>
                </div>
                <div class="w-full h-[45px] flex items-center justify-between border-b">
                <div class="flex items-center justify-start">
                    <div class="flex items-center justify-center mr-3">
                        <span class="material-symbols-outlined text-default text-17"> check_circle </span>
                    </div>
                    <div class="text-gray-700">Total</div>
                </div>
                <div class="flex flex-col items-end justify-center">
                    <span class="font-semibold text-12">
                        <span class="material-symbols-outlined text-13 mr-1"></span>
                        ${value.total}
                    </span>
                </div>
            </div>
                `;
            }
        });
        return setup;
    }
    

    staffing_plan(data){
        let staffing= ''
        $.each(data,(index, value)=>{
            if (index <= 7) {
                staffing += `
                </div>
                <div class="w-full h-[40px] flex items-center justify-between">
                    <div class="flex items-center justify-start">
                        <div class="flex ietms-center justify-center relative w-[30px] h-[20px] mr-1">
                            <div class="absolute w-[15px] h-[15px] border-2 border-orange-600 rounded-md rotate-[50deg] mt-1"></div>
                            <div class="absolute w-[15px] h-[15px] border-2 border-indigo-600 rounded-md rotate-[40deg]"></div>
                        </div>
                        <span>${value.department_name}</span>
                    </div>
                    <div class="rounded-full bg-gray-100 font-bold flex items-center justify-center w-[25px] h-[25px]">
                    ${value.number_of_departments}
                    </div>
                </div>
                `
            }
        })
        return staffing
    }


    job_opening(data){
        let job= ''
        $.each(data,(index, value)=>{
            if (index <= 7) {
                job += `
                </div>
                <div class="w-full h-[40px] flex items-center justify-between">
                    <div class="flex items-center justify-start">
                        <div class="flex ietms-center justify-center relative w-[30px] h-[20px] mr-1">
                            <div class="absolute w-[15px] h-[15px] border-2 border-orange-600 rounded-md rotate-[50deg] mt-1"></div>
                            <div class="absolute w-[15px] h-[15px] border-2 border-indigo-600 rounded-md rotate-[40deg]"></div>
                        </div>
                        <span>${value.department_name}</span>
                    </div>
                    <div class="rounded-full bg-gray-100 font-bold flex items-center justify-center w-[25px] h-[25px]">
                    ${value.number_of_departments}
                    </div>
                </div>
                `
            }
        })
        return job
    }




job_application(data){
    let application= ''
    $.each(data,(index, value)=>{
        if (index <= 6) {
            application += `
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
                            ${value.application_date}
                        </span>
                        <small class="text-orange-500 text-10">Applied</small>
                    </div>
               </div>
            `
        }
    })
    return application
}


job_application_stats (data){
    let application_stats= ''
    $.each(data,(index, value)=>{
        if (index <= 6) {
            application_stats += `
        <div> 
        <div class="w-full h-[45px] flex items-center justify-between">
        <div class="flex items-center justify-start">
            <div class="flex items-ceenter justify-center mr-3">
            </div>
                    <div class="text-gray-700">Number Of Job Openings</div>
                </div>
                <div class="flex flex-col items-center justify-center w-[20px] h-[20px] rounded-full bg-gray-100 text-12">
                ${value.number_of_job_openings}
                </div>
        </div>
        <div class="w-full h-[45px] flex items-center justify-between">
        <div class="flex items-center justify-start">
            <div class="flex items-ceenter justify-center mr-3">
                
            </div>
            <div class="text-gray-700">Number Of Job Applications</div>
        </div>
        <div class="flex flex-col items-center justify-center w-[20px] h-[20px] rounded-full bg-gray-100 text-12">
        ${value.number_of_job_applications}
        </div>
    </div>

    <div class="w-full h-[45px] flex items-center justify-between">
    <div class="flex items-center justify-start">
        <div class="flex items-ceenter justify-center mr-3">
            <div/>
            `
        }
    })
    return application_stats
}



interview(data){
    let interview = ''
    $.each(data,(index, value)=>{
        if (index <= 6) {
            interview += `
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
                       ${value.interview_date}
                   </span>
                   <small class="text-orange-500 text-10">Scheduled</small>
               </div>
          </div>   `
        }
    })
    return interview
}


interview_stats(data){
    let interview_stats= ''
    $.each(data,(index, value)=>{
        if (index <= 6) {
            interview_stats += `
            <div class="w-full h-[45px] flex items-center justify-between">
            <div class="flex items-center justify-start">
                <div class="flex items-ceenter justify-center mr-3">
                   
                </div>
                <div class="text-gray-700">Accepted Interviews</div>
            </div>
            <div class="flex flex-col items-center justify-center w-[20px] h-[20px] rounded-full bg-gray-100 text-12">
                ${value.accepted}
            </div>
       </div>
        <div class="w-full h-[45px] flex items-center justify-between">
            <div class="flex items-center justify-start">
                <div class="flex items-ceenter justify-center mr-3">
                    
                </div>
                <div class="text-gray-700">Rejected Interviews</div>
            </div>
            <div class="flex flex-col items-center justify-center w-[20px] h-[20px] rounded-full bg-gray-100 text-12">
            ${value.rejected}
            </div>
       </div>
        <div class="w-full h-[45px] flex items-center justify-between">
            <div class="flex items-center justify-start">
                <div class="flex items-ceenter justify-center mr-3">
                    
                </div>
                <div class="text-gray-700">Interviews Pending Approval</div>
            </div>
            <div class="flex flex-col items-center justify-center w-[20px] h-[20px] rounded-full bg-gray-100 text-12">
            ${value.pending}
            </div>
       </div>
            `
        }
    })
    return interview_stats
}




self_appraisal(data){
        let appraisal_self= ''
        $.each(data,(index, value)=>{
            if (index <= 6) {
                appraisal_self += `
                <div class="w-full h-[45px] flex items-center justify-between border-b">
                <div class="flex items-center justify-start">
                    <div class="flex items-ceenter justify-center mr-3">
                        <span class="material-symbols-outlined text-default text-17"> check_circle </span>
                    </div>
                    <div class="text-gray-700">${value.appraisal_name}</div>
                </div>
                <div class="flex flex-col items-end justify-center">
                    <span class="font-semibold text-12">
                        <span class="material-symbols-outlined text-13 mr-1"> calendar_month </span>
                        ${value.date}
                    </span>
                    <small class="text-orange-500 text-10"></small>
                </div>
           </div>  
                `
            }
        })
        return appraisal_self
    }


    appraisal(data){
        let appraisal= ''
        $.each(data,(index, value)=>{
            if (index <= 6) {
                appraisal += `
                <div class="w-full h-[45px] flex items-center justify-between border-b">
                <div class="flex items-center justify-start">
                    <div class="flex items-ceenter justify-center mr-3">
                        <span class="material-symbols-outlined text-default text-17"> check_circle </span>
                    </div>
                    <div class="text-gray-700">${value.appraisal_name}</div>
                </div>
                <div class="flex flex-col items-end justify-center">
                    <span class="font-semibold text-12">
                        <span class="material-symbols-outlined text-13 mr-1"> calendar_month </span>
                        ${value.date}
                    </span>
                  
                </div>
           </div>
                `
            }
        })
        return appraisal
    }

    work_plan_data(data){
        let plan= ''
        $.each(data,(index, value)=>{
            if (index <= 6) {
                plan += `
                <div class="w-full h-[45px] flex items-center justify-between border-b">
                <div class="flex items-center justify-start">
                    <div class="flex items-ceenter justify-center mr-3">
                        <span class="material-symbols-outlined text-default text-17"> check_circle </span>
                    </div>
                    <div class="text-gray-700">${value.employee_name}</div>
                </div>
                <div class="flex flex-col items-end justify-center">
                    <span class="font-semibold text-12">
                        <span class="material-symbols-outlined text-13 mr-1"> calendar_month </span>
                        ${value.month}
                    </span>
                    <small class="text-orange-500 text-10">Completed</small>
                </div>
           </div>
                `
            }
        })
        return plan
    }

    application(data){
        let apply= ''
        $.each(data,(index, value)=>{
            if (index <= 6) {
                apply += `
                <div class="w-full h-[45px] flex items-center justify-between border-b">
                <div class="flex items-center justify-start">
                    <div class="flex items-ceenter justify-center mr-3">
                        <span class="material-symbols-outlined text-default text-17"> check_circle </span>
                    </div>
                    <div class="text-gray-700">${value.employee_name}</div>
                </div>
                <div class="flex flex-col items-end justify-center">
                    <span class="font-semibold text-12">
                        
                        ${value.time_duration_formatted}
                    </span>
                    <small class="text-orange-500 text-10">${value.leave_type}</small>
                </div>
           </div>
                `
            }
        })
        return apply
    }

    leave_departments_stats(data){
        let depstats= ''
        $.each(data,(index, value)=>{
            if (index <= 6) {
                depstats += `
                <div class="w-full h-[45px] flex items-center justify-between">
                    <div class="flex items-center justify-start">
                        <div class="flex items-ceenter justify-center mr-3">
            
                        </div>
                        <div class="text-gray-700">${value.department_name}</div>
                    </div>
                    <div class="flex flex-col items-center justify-center w-[20px] h-[20px] rounded-full bg-gray-100 text-12">
                    ${value.number_of_employees}
                    </div>
               </div>
                `
            }
        })
        return depstats
    }

    memo_card(data){      
        let memorandum= ''
        $.each(data,(index, value)=>{
            if (index <= 6) {
                console.log(index)
                memorandum += `
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
                        <small class="text-orange-500 text-10">${value.from}</small>
                    </div>
                </div>
                `
            }
        })
        console.log(memorandum);
        
        return memorandum
    }


    employee_performance (data){

        let top_performers = ''
        $.each(data,(index, value)=>{
            let value_text = value.percentage_of_completion > 50 ? "Above Average" : "Below Average";
            let value_color = value.percentage_of_completion > 50 ? "emerald" : "red";
            if (index <= 6) {
                top_performers += `
                <div class="grid grid-cols-3 w-full h-[35px] bg-gray-100 text-11 rounded-t rounded-md mt-2 px-2">
                <span class="flex items-center justify-start col-span-2 font-semibold">
                  ${value.employee} 
                </span>
                <span class="flex items-center justify-start col-span-1 ">
                    <span class="p-[3px] px-4 bg-white-500/30 font-semibold text-${value_color}-700 rounded-md">${value_text}</span>
                </span>
            </div>
                `
            }
        })
        return top_performers
    }


    employee_attendance (data){
        let attendance = ''
        $.each(data,(index, value)=>{
            if (index <= 5) {
                attendance += `
                <div class="grid grid-cols-3 w-full h-[35px] bg-gray-100 text-11 rounded-t rounded-md mt-2 px-2">
                <span class="flex items-center justify-start col-span-2 font-semibold">
                  ${value.employee} 
                </span>
                <span class="flex items-center justify-start col-span-1 ">
                    <span class="p-[3px] px-4 bg-white-500/30 font-semibold text-${value.value_color}-700 rounded-md">${value.Category}</span>
                </span>
            </div>
                `
            }
        })
        return attendance
    }

    create_performance_by_department_card(key, value){
        return `
            <tr class="">
        <td class="py-3 px-2">${value.appraisal_type}</td>
         <td class="py-3 px-2">${value.department}</td>
        <td class="py-3 px-2">${value.lowest_score}</td>
        <td class="py-3 px-2">${value.average_score}</td>
        <td class="py-3 px-2">${value.highest_score}</td>
       
      </tr>
        `
    }

    gratuity(data){
        let gratuity = ''
        $.each(data,(index, value)=>{
            if (index <= 5) {
                overtime += `
                   <div class="w-full h-[45px] flex items-center justify-between border-b">
                   <div class="flex items-center justify-start">
                       <div class="flex items-ceenter justify-center mr-3">
                           <span class="material-symbols-outlined text-default text-17"> check_circle </span>
                       </div>
                       <div class="text-gray-700">${value.employee_name}</div>
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
        return gratuity
    }


    gratuity_stats(data){
        let gratuity_stats= ''
        $.each(data,(index, value)=>{
            if (index <= 5) {
                gratuity_stats += `
                <div class="w-full h-[45px] flex items-center justify-between">
                <div class="flex items-center justify-start">
                    <div class="flex items-ceenter justify-center mr-3">
                       
                    </div>
                    <div class="text-gray-700">Approved Overtimes</div>
                </div>
                <div class="flex flex-col items-center justify-center w-[20px] h-[20px] rounded-full bg-gray-100 text-12">
                    ${value.approved}
                </div>
           </div>
            <div class="w-full h-[45px] flex items-center justify-between">
                <div class="flex items-center justify-start">
                    <div class="flex items-ceenter justify-center mr-3">
                        
                    </div>
                    <div class="text-gray-700">Rejected Overtimes</div>
                </div>
                <div class="flex flex-col items-center justify-center w-[20px] h-[20px] rounded-full bg-gray-100 text-12">
                ${value.rejected}
                </div>
           </div>
            <div class="w-full h-[45px] flex items-center justify-between">
                <div class="flex items-center justify-start">
                    <div class="flex items-ceenter justify-center mr-3">
                        
                    </div>
                    <div class="text-gray-700">Pending Approval</div>
                </div>
                <div class="flex flex-col items-center justify-center w-[20px] h-[20px] rounded-full bg-gray-100 text-12">
                ${value.pending}
                </div>
           </div>
                `
            }
        })
        return gratuity_stats
    }


    

    employee_grievance(data){
        let grievance= ''
        $.each(data, (index, value) => {            
            if (index <= 3) {
                grievance += `
               <div class="mt-4 my-8">
                    <ul class="space-y-3">
                        <!-- Grievance 1 -->
                        <li class="flex justify-between items-center p-3 bg-gray-50 rounded-md shadow-sm">
                            <div>
                                <p class="text-sm font-medium text-gray-800">${value.Grievance_ID}</p>
                                <p class="text-xs text-gray-500">Raised on: ${value.Raised_on}</p>
                            </div>
                            <span class="text-xs text-purple-800 bg-purple-100 px-2 py-1 rounded">Status: ${value.Status}</span>
                        </li>
                    </ul>
                </div>
                `
            }
        })
        return grievance
    }
    case_outcomes(data){
        let grievance= ''
        $.each(data, (index, value) => {  
            
            if (index <= 3) {
                grievance += `
                <div class="flex justify-between items-center bg-purple-100 p-3 rounded-md">
                    <div class="flex items-center">
                        <span class="material-symbols-outlined text-red-600 mr-2">
                            error
                        </span>
                        <span class="font-semibold text-gray-800">${value.Most_Common_Grievance}</span>
                    </div>
                    <span class="text-sm font-medium text-red-600">Cases: ${value.Count}</span>
                </div>
                `
            }
        })
        return grievance
    }
    weeekly_applicants(data){
        let weekly_applic= ''
        $.each(data, (index, value) => {              
            if (index <= 3) {
                weekly_applic += `
                <div class="flex flex-col border-b border-gray-300">
                    <div class="flex items-center gap-3 ">
                        <div class="flex items-center justify-center rounded-full bg-gray-100 border border-gray-400 w-[16px] h-[16px]">
                            <img src="/media/defaults/avatas/dp.jpeg" class="w-full h-full rounded-full object-cover object-top" alt="User Avatar">
                        </div>
                        <p class="font-semibold text-gray-800">${value.applicant_name}</p>
                    </div>                                            
                    <div class="flex justify-between items-center text-default">
                        <small class="ml-5 text-default flex items-center gap-1">
                            📅 <span class="font-medium">${value.start_date}</span>
                        </small>
                        <div class="flex items-center gap-3 bg-default/10 px-3 py-1 rounded-md border border-default shadow-sm">
                            <small class="text-default-700">🗓️ Total Days</small>
                            <p class="font-semibold text-default">${value.leave_duration}</p>
                        </div>
                    </div>
                </div>

                `
            }
        })
        return weekly_applic
    }
    commutation(data){
        let leave_commuted= ''
        $.each(data, (index, value) => {              
            if (index <= 3) {
                leave_commuted += `
                <div class="flex flex-col bg-white border border-dotted border-gray-300 p-4">
                    <div class="flex items-center gap-3">
                        <div class="flex items-center justify-center rounded-full bg-gray-200 border border-gray-300 w-[16px] h-[16px] shadow-sm">
                            <img src="/media/defaults/avatas/dp.jpeg" class="w-full h-full rounded-full object-cover object-top" alt="User Avatar">
                        </div>
                        <small class="text-gray-800 font-medium">${value.employee}</small>
                    </div>

                    <div class="space-y-2 bg-default/20">
                        <div class="flex justify-between">
                            <small class="text-gray-600">📅 Days Commutated</small>
                            <p class="border border-dotted border-gray-400 h-7 w-20 rounded-md flex justify-center items-center font-semibold text-gray-800 bg-gray-100">${value.commutated_days}</p>
                        </div>
                        <div class="flex justify-between">
                            <small class="text-gray-600">💰 Value</small>
                            <p class="border border-dotted border-gray-400 h-7 w-20 rounded-md flex justify-center items-center font-semibold text-gray-800 bg-gray-100">${value.value}</p>
                        </div>
                    </div>
                </div>
                `
            }
        })
        return leave_commuted
    }
    get_emps_with_hlds(data){
        let emps_whlds= ''
        $.each(data, (index, value) => { 
            console.log(value);
                         
            if (index <= 3) {
                emps_whlds += `
               <div class="grid grid-cols-2 items-center gap-4">
                    <div class="flex items-center gap-3 border-r border-default pr-4">
                        <div class="flex items-center justify-center rounded-full bg-gray-100 border border-default w-[32px] h-[32px] shadow">
                            <img src="/media/defaults/avatas/dp.jpeg" class="w-full h-full rounded-full object-cover aspect-square" alt="User Avatar text-default">
                        </div>
                        <p class="text-default font-semibold truncate max-w-[120px]" title="${value.employee_name}">
                            ${value.employee_name}
                        </p>
                    </div>
                    
                    <div class="flex items-center gap-3">
                        <p class="text-default text-sm font-medium">Total Days</p>
                        <small class="border border-dotted border-default h-6 w-12 flex items-center justify-center rounded-md text-blue-800 font-semibold bg-blue-50 shadow-sm">
                            ${value.total_leaves_allocated}
                        </small>
                    </div>
                </div>
                `
            }
        })
        return emps_whlds
    }
    staffing_plan_by_department(dept, data) {
        return `<div class="w-full h-[40px] flex items-center justify-between">
                    <div class="flex items-center justify-start">
                        <div class="flex ietms-center justify-center relative w-[30px] h-[20px] mr-1">
                            <div class="absolute w-[15px] h-[15px] border-2 border-orange-600 rounded-md rotate-[50deg] mt-1"></div>
                            <div class="absolute w-[15px] h-[15px] border-2 border-indigo-600 rounded-md rotate-[40deg]"></div>
                        </div>
                        <span>${dept}</span>
                    </div>
                    <div class="rounded-full bg-gray-100 font-bold flex items-center justify-center w-[25px] h-[25px]">
                        ${data}
                    </div>
                </div>`
    }
    create_dashboard_hr_empty_content_card($wrapper){
        lite.utils.add_empty_component({$wrapper: $wrapper, text:"No Data Found.",classnames:"h-full mt-5"})
        $wrapper.append(`
            <div class="flex items-center justify-center flex-col mt-5">
                <a href="/app/accounting/banking/?loc=banking&type=new&document=Bank%20Account" class="border border-indigo-300 px-2 py-1 rounded-md text-12 flex items-center justify-center btn">
                    No Content 
                    <span class="material-symbols-outlined ml-2"> east </span>
                </a>
            </div>
        `)
    }

    leave_plan_sv_stats(data){
        let plsvsstats= ''
        const color =['#1f1847', '#4941ED', '#306DF9', '#EDB141', '#A030F9', '#C8A11C', '#C85B1C','#eb73bb']
        $.each(data,(index, value)=>{
            if (index <= 6) {
                plsvsstats += `
                <span class="grid grid-cols-12 gap-4 bg-theme_text_color text-default rounded-md px-2">
                    <div class="col-span-8 text-center font-semi-bold text-lg  p-2 place-content-center text-start"><h2>${value.leave_type}</h2></div>
                    <div class="col-span-4 h-full w-full ">
                        <div class="mt-1 bg-red-100 px-2 rounded-lg text-end">
                            <div class="">
                                <h5 class="inline-block text-md font-bold">${lite.utils.thousand_separator(value.avg_len, 0)}</h5><span><small> Days</small><span>
                            </div>
                            <small class="text-primary">Average Days Taken</small>
                        </div>
                    </div>
                </span>
                `
            }
        })
        return plsvsstats
    }

    attendance_list_cards(data){
        let card =""
        $.each(data,(_, emp)=>{
            card +=`
                <div lite-attendance-card="${emp?.name}" lite-name="${emp?.full_name}" class="${emp?.attended? "pointer-events-none":'cursor-pointer '} min-h-[350px] max-h-[350px] gap-3 p-2 col-span-2 box rounded-md">
                    <div class=" ${emp?.attended? "bg-emerald-500 text-white" : ''} h-full pointer-events-none w-full p-2">
                        <div class="h-[70%] w-full">
                            <div class="h-full pointer-events-none w-full overflow-hidden">
                                <img src="${emp.img? emp?.img: "/media/defaults/avatas/dp.jpeg"}" alt="${emp?.full_name}" class="w-full pointer-events-none h-full object-cover">
                            </div>
                        </div>
                        <div class="h-[30%] w-full pointer-events-none">
                            <div class="h-full pointer-events-none w-full flex-col flex items-center gap-2 flex-wrap">
                                <p class="text-xl pointer-events-none font-semibold flex justify-center items-center flex-wrap capitalize">${emp?.full_name}</p>
                                <p class="text-md pointer-events-none capitalize">${emp?.department}</p>
                                <p class="pointer-events-none font-semibold text-indigo-700 capitalize">${emp?.designation}</p>
                            </div>
                        </div>
                    </div>
                </div>
            ` })
        return card
    }

    emp_under_disciplinary(data){
        let card =""
        $.each(data,(_, value)=>{
            card +=`
                <li class="flex items-center justify-between py-2 border-b border-slate-300/60 last:pb-0">
                    <div class="flex items-center">
                        <img
                            src="/media/defaults/avatas/dp.jpeg"
                            alt=${value.emp_name}
                            class="relative inline-block h-8 w-8 mr-4 rounded-full object-cover object-center"
                        />
                        <span class="text-[13px] font-semibold">${value.emp_name}</span>
                    </div>
                    <span class="text-purple-400 text-[11px] font-semibold">${value.action_taken}</span>
                </li>
            ` })
        return card
    }

    recent_separations(data){
        let card =""
        $.each(data,(_, value)=>{
            card +=`
                <li class="flex items-center justify-between py-2 border-b border-slate-300/60 last:pb-0">
                    <div class="flex items-center">
                        <div class="relative h-8 w-8 mr-4 flex justify-center items-center rounded-full object-cover object-center">
                            <span class="material-symbols-outlined text-[25px] text-rose-500">
                                sync_problem
                            </span>
                        </div>
                        <span class="text-[13px] font-semibold">${value?.name}</span>
                    </div>
                    <div class="flex flex-col gap-1"><span class="text-orange-400 text-[11px] font-semibold">${value.date_of_application}</span>
                        <div class="flex flex-col items-end gap-1"><span class="text-rose-400 text-[11px] font-semibold">${value.status}</span>

                    </div>
                </li>
            ` })
        return card
    }

    separation_settlements(data){
        let card =""
        for(let i=0; i<Math.floor(data); i++){
            card +=`
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"
                    class="w-4 h-auto">
                    <path fill-rule="evenodd"
                        d="M10.788 3.21c.448-1.077 1.976-1.077 2.424 0l2.082 5.007 5.404.433c1.164.093 1.636 1.545.749 2.305l-4.117 3.527 1.257 5.273c.271 1.136-.964 2.033-1.96 1.425L12 18.354 7.373 21.18c-.996.608-2.231-.29-1.96-1.425l1.257-5.273-4.117-3.527c-.887-.76-.415-2.212.749-2.305l5.404-.433 2.082-5.006z"
                        clip-rule="evenodd">
                    </path>
                </svg>
            ` }
        return card
    }

    emp_profile(data){
        let card =""
        console.log(data);
        
        $.each(data,(_, value)=>{
            card +=`
                <div class="w-full flex items-center justify-between border-b border-dotted min-h-[30px]">
                    <div class="flex items-center justify-start py-2">
                        <a href="" class="flex items-center justify-start">
                            <div class="w-[27px] h-[27px] rounded-md bg-red-100 text-indigo-900 flex items-center justify-center mr-2">
                                <span class="material-symbols-outlined text-20 .material-symbols-outlined-hidden"> event </span>
                            </div>
                            <div class="flex flex-col">
                                <span class="text-13">${value.leave_type}</span>
                                <small class="text-gray-400 text-10">${value.total_leave_days} Days</small>
                            </div>
                        </a>
                    </div>
                    <div>
                        <div class="span text-purple-700 text-13 font-semibold">Used Days</div>
                        <small class="text-10 text-gray-600">${value.used_leave_days} day</small>
                    </div>
                </div>
            `
        })

        return card
    }

    welfare_transactions_table(data){
        let card =""
        $.each(data,(_, value)=>{
            card +=`
                <div class="w-full grid grid-cols-10 border-b h-[50px] text-12 pl-2 intro-x">
                    <div class="w-full flex items-center justify-start h-full col-span-5 pl-2">
                        <div class="h-full w-full flex items-center gap-x-2">
                            <div class="h-[35px] w-[35px] rounded-lg bg-red-400 overflow-hidden">
                                <img src="/media//defaults//avatas/dp.jpeg" alt="Avatar" class="w-full h-full">
                            </div>
                            <div class="mt-1">
                                <p class="font-bold">${value?.staff}</p>
                                <p class="text-[9px]">${value?.department}</p>
                            </div>
                        </div>
                    </div>
                    <a href="#" class="w-full flex items-center justify-start h-full col-span-2">
                        <span class="material-symbols-outlined mr-1 text-orange-600">
                            event_available
                        </span>
                        ${value?.welfare}
                    </a>
                    <div class="w-full flex items-center  col-span-2 justify-start h-full">
                        <span class="material-symbols-outlined mr-1">
                            event
                        </span>
                        ${value.date}
                    </div>
                    <div class="w-full flex items-center justify-start h-full">
                        <span class="material-symbols-outlined mr-1">
                            trending_up
                        </span>
                        ${value?.amount}
                    </div>
                </div>
            `
        })

        return card
    }




    recent_application_table(data){
        let card =""
        
        $.each(data,(_, value)=>{
            card +=`
                
                <div class="w-full grid grid-cols-5 h-[45px] bg-gray-100 rounded-t-md text-12 font-semibold">
                    <div class="w-full flex items-center justify-start h-full col-span-2 pl-2">
                        <span class="material-symbols-outlined mr-1 text-orange-600">
                            event_available
                        </span>
                        ${value?.welfare}
                    </div>
                    <div class="w-full flex items-center col-span-2 justify-start h-full">
                        <span class="material-symbols-outlined mr-1">
                            event
                        </span>
                        ${value?.date}
                    </div>
                    <div class="w-full flex items-center justify-start h-full">
                        <span class="material-symbols-outlined mr-2">
                            trending_up
                        </span>
                        ${value?.amount}
                    </div>
                </div>

            `
        })

        return card
    }
}
