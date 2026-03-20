

export default class Dynamic_Help_Desk_Html {
    constructor(){
    }
    chat_content(arr) {
        let chat = "";
    
        $.each(arr, (_, values) => {
            const user = values.main_role?.toLowerCase().includes("admin");
            const message = values.comment || values.action || "No message";
            const userName = values.taken_by || "Unknown";
            const avatar = user ? "/static/images/avata/avata8.jpeg" : "/static/images/avata/avata8.jpeg"; 
            const justify = user ? "justify-start" : "justify-end";
            const bgColor = user ? "bg-default" : "bg-default";
            const alignment = user ? "left" : "right";
            const time = `${values.date}, ${values.time}`;
    
            chat += `
                <div class="w-full mb-4 flex ${justify}">
                    <div class="flex flex-col max-w-[60%] ${user ? "items-start" : "items-end"}">
                        <span class="text-[10px] text-white mb-1">${values.time}</span>
                        
                        <div class="relative p-3 ${bgColor} rounded-xl shadow-sm">
                            <div class="flex items-start gap-2">
                                ${user ? `
                                    <img src="${avatar}" class="w-8 h-8 rounded-full object-cover mt-1" />
                                ` : ""}
    
                                <div class="text-sm leading-relaxed text-white">
                                    <p class="font-semibold text-white">${userName}</p>
                                    <p>${message}</p>
                                </div>
    
                                ${!user ? `
                                    <img src="${avatar}" class="w-8 h-8 rounded-full object-cover mt-1" />
                                ` : ""}
                            </div>
    
                            <div class="w-full flex justify-between items-center mt-2 text-[10px] text-white">
                                <span>${time}</span>
                                <span class="material-symbols-outlined text-xs">done_all</span>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        });
    
        return chat;
    }
    
    side_ticket_dashboard (arr) {
        let list_item = ''
        $.each (arr, (_, item) => {
            if (_ < 10) {
                list_item += `
                    <div class="shadow-sm overflow-hidden bg-slate-200/30 rounded-md px-2">
                        <div class="h-full w-full flex items-center justify-between gap-2">
                            <div class="w-[70%] h-full flex px-2 items-center">
                                <h4 class="font-light text-[12px] capitalize">${item?.ticket_name}</h4>
                            </div>                                
                            <div class="w-[30%] h-[50%] rounded-md flex justify-center items-center bg-[${item?.status.status_color}] p-1">
                                <span class="text-[10px] text-[${item?.status.inner_color}] font-light">${item?.status.name}</span>
                            </div>
                        </div>
                    </div>
                `
            }
        })
        return list_item
    }

    social_media (arr) {
        let cr = ""
        $.each (arr, (_, ele) => {
            if (_ <= 6) {
            cr += `
                <div class="grid grid-cols-11 w-full h-[30px] bg-gray-100 text-11 rounded-t rounded-md mt-2 p-2">
                    <span class="flex items-center justify-start col-span-2">
                        ${ele.posting_date}
                    </span>
                    <span class="flex items-center justify-start col-span-4">
                        ${ele.name}
                    </span>
                    <span class="flex items-center justify-start col-span-2">
                        Facebook
                    </span>
                    <span class="flex items-center justify-start col-span-1">
                        0
                    </span>
                </div>`
            }
        })

        return cr
    }
    affected_services(arr) {
        let card = `
        `;
    
        $.each(arr, (index, Values) => {
            if (index < 8) {
                card += `
                    <div class="w-full border-gray-300">
                        <div class="grid grid-cols-3 gap-1 p-3 bg-gray-50 rounded-md shadow-sm">
                            <!-- Left Section: Icon and Service Name -->
                            <div class="flex flex-col font-medium text-theme_text_color overflow-hidden">
                            <div class="flex items-center space-x-2">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-theme_text_color" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 9a3.75 3.75 0 113.75 3.75A3.75 3.75 0 019.75 9zm6.25 3.75V18a3.25 3.25 0 01-6.5 0v-5.25m-3.25 0V18a6.5 6.5 0 0113 0v-5.25" />
                                </svg>
                                <p class="text-gray-800 truncate">${Values.service_name || ""}</p>
                            </div>
                            <!-- Team Section -->
                            <p class="text-xs text-gray-500 ml-8 truncate whitespace-nowrap">
                                Team: ${Values.team || ""}
                            </p>
                            </div>

                            <!-- Middle Section: Empty Column for Alignment -->
                            <div class="flex flex-col justify-center items-center text-center"></div>

                            <!-- Right Section: Ticket Number -->
                            <div class="flex justify-end items-center">
                            <div class="w-8 h-8 rounded-full bg-default/20 text-theme_text_color flex justify-center items-center text-sm font-bold">
                                ${Values.number_tickets || 0}
                            </div>
                            </div>
                        </div>
                    </div>                   
                `;
            }
        });
    
        return card; 
    }
    
    customer_feedback(arr) {
        let card = ``
        $.each(arr, (index, Values) => {            
            if (index < 3) {
                card += `
                <div class="w-full flex items-center justify-between mt-2 mt-4 border-b pb-2">
                    <span class="flex items-start justify-start text-13 ">
                        <span class="material-symbols-outlined text-18 mr-1 text-orange-500 mt-1">radio_button_checked</span>
                        <div class="flex items-start justify-start flex-col">
                            <small>From: ${Values.customer || ""}</small>
                             <small>Feedback: ${Values.feedback_type || ""}</small>
                        </div>
                    </span>
                    <a href="/app/crm/customer_feedback/?app=customer_feedback&page=list&content_type=customer feedback">
                        <span class="flex items justify-end">
                            <button class="btn flex items-center justify-center btn-sm text-11">
                                <span class="material-symbols-outlined text-11 mr-1 text-indigo-900">task_alt</span>
                                view
                            </button>
                        </span>
                    </a>
                </div> 
            `
            }
           
        })
        return card; 
    }
   
    contracts (arr) {
        let cr = ""
        $.each (arr, (_, ele) => {
            if (_ <= 2) {
            cr += `
                <div class="w-full border-t">
                    <div class="h-full w-full text-[10px] rounded-md px-2 flex justify-between items-center">
                        <p class="w-[33%] font-semibold text-indigo-900">${ele.customer}</p>
                        <p class="w-[33%] font-light text-right text-indigo-900">${moment(ele.end_date).format('Do MMM, YYYY')}</p>
                    </div>
                </div> 
                `
            }
        })

        return cr
    } 
    recent_prospects(arr) {
        let card = ""
        $.each(arr, (_, val) => { 
            console.log(val.name);
            if (_ <= 5){
                card += `
                <div class="flex justify-between justify-center items-center p-4 border border-b">
                <div>${val.name}</div>
                <div>${val.email}</div>
                </div>
            `
            }
        })
        return card
    }
    contract_stats_(arr){
        let card =''
        $.each(arr, (_, value)=>{
            if (_<=6){
                card += `
                 <!-- Contract Item -->
                <div class="border border-dotted border-default rounded-lg bg-gray-50">
                    <div class="flex gap-2 items-center">
                    <span class="material-symbols-outlined text-gray-500 text-xl flex items-center justify-center text-theme_text_color">contract_edit</span>
                    <p class=" text-gray-700">${value.contract_name}</p>
                    </div>
                    <div class="flex justify-center items-center justify-between p-2"><small class="text-sm text-gray-500 ml-6">Milestone</small>
                    <p class="border border-dotted border-default rounded-full h-4 w-4">${value.objectives_achieved}</p>
                    </div>
                </div> 
                            `
            }
        })
        return card
    }
    create_dashboard_empty_content_card($wrapper, text) {
        lite.utils.add_empty_component({
            $wrapper: $wrapper,
            text: text,
            classnames: "h-full mt-5"
        })
        $wrapper.append(`<div class="flex items-center justify-center flex-col mt-5">
                    <span class="text-gray-500">${text}</span>
            </div>
        `)
    }
}
