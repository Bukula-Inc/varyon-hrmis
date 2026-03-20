export default class Dynamic_Crm_Html {
    constructor() {}
    create_pipeline_row_latest_sales (data) {
        let row = ''
        if (data.length > 0) {
            $.each (data, (_, ele) => {
                row += `
                    <div class="grid grid-cols-11 w-full h-[30px] bg-gray-100 text-11 rounded-t rounded-md mt-2 gap-4 px-4">
                        <span class="flex items-center justify-start col-span-4">
                            Bright Kunda Mulomba
                        </span>
                        <span class="flex items-center justify-start col-span-3">
                            <span class="material-symbols-outlined mr-1 text-indigo-600">diversity_3</span>
                            Bsk Inc.
                        </span>
                        <span class="flex items-center justify-end col-span-2">
                            ZMW 2300,000.00
                        </span>
                        <span class="flex items-center justify-end col-span-2">
                            12 June, 2024
                        </span>
                    </div>
                `
            })
        }

        return row
    }
    ticket_conversation(arr) {
        let chat = "";
    
        $.each(arr, (_, values) => {
            const user = values.main_role?.toLowerCase().includes("admin");
            const message = values.comment || values.action || "No message";
            const userName = values.action_taker || "Unknown";
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
    
    email_group_data(data) {
      let cards = ``;
      $.each(data, (index, Values) => {        
          if (index < 9) {
              cards += `
                  <div class="w-full flex items-center justify-between mt-2 mt-4 border-b pb-2">
                    <span class="flex items-start justify-start text-13 ">
                        <span class="material-symbols-outlined text-18 mr-1 text-orange-500 mt-1">radio_button_checked</span>
                        <div class="flex items-start justify-start flex-col">
                            <span class="text-12">${Values.group_name}</span>
                            <small>Created On: ${Values.created_on}</small>
                        </div>
                    </span>
                    <span class="flex items justify-end">
                      <button class="btn flex items-center justify-center btn-sm text-11">
                            <span class="material-symbols-outlined text-11 mr-1 text-indigo-900">task_alt</span>
                            view
                      </button>
                    </span>
                </div> 
              `;
          }
      });
      return cards;
    }
    top_relation_managers(arr) {
      let card = ``
      $.each(arr, (index, Values) => {               
          if (index < 8) {
              card += `
              <div class="w-full flex items-center justify-between mt-2 border-b pb-3">
                  <div class="flex items-start space-x-4">
                    <!-- Icon and Service Name -->
                    <span class="material-symbols-outlined text-2xl text-orange-500">radio_button_checked</span>
                    <div>
                      <span class="font-semibold text-indigo-900 block">${Values.name || "Unknown Service"}</span>
                      <div class="flex gap-2 text-sm text-gray-600">
                        <!-- Issue Count -->
                        <span class="flex items-center">
                          <span class="material-symbols-outlined text-lg text-purple-500">report_problem</span>
                          <span class="text-default text-xs">${Values.total_tickets || 0} Total Tickets</span>
                        </span>
                
                        <!-- High Priority -->
                        <span class="flex items-center">
                          <span class="material-symbols-outlined text-lg text-red-500">priority_high</span>
                          <span class="text-default text-xs">${Values.closed_tickets || 0} Closed</span>
                        </span>
                
                        <!-- Medium Priority -->
                        <span class="flex items-center">
                          <span class="material-symbols-outlined text-lg text-yellow-500">priority_high</span>
                          <span class="text-default text-xs">${Values.open_tickets || 0} Open</span>
                        </span>
                      </div>
                    </div>
                  </div>
                </div>       

              `
          }
      })
      return card; 
    }
    
    com_history_d(data) {
      let cards = ``;
      $.each(data, (index, Values) => {   
          if (index <5) {
              cards += `
                  <div class="grid grid-cols-11 w-full h-[30px] bg-gray-100 text-11 rounded-t rounded-md mt-2 p-2">
                      <span class="flex items-center justify-start col-span-2">
                          ${Values.created_on}
                      </span>
                      <span class="flex items-center justify-start col-span-3">
                          ${Values.group}
                      </span>
                      <span class="flex items-center justify-start col-span-2">
                          ${Values.subject}
                      </span>
                      <span class="flex items-center justify-start col-span-2">
                          ${Values.status}
                      </span>
                  </div>
              `;
          }
      });
      return cards;
    }
  
    lead_details(data) {
      let cards = `
        <div class="overflow-x-auto">
          <div class="align-middle inline-block min-w-full shadow-lg rounded-lg border border-gray-200">
            <table class="min-w-full border border-gray-200">
              <thead class="bg-gradient-to-r from-blue-100 to-indigo-200">
                <tr>
                  <th class="px-6 py-3 border-b border-gray-200 text-left text-sm leading-4 font-medium text-gray-900 uppercase tracking-wider">Sales Person</th>
                  <th class="px-6 py-3 border-b border-gray-200 text-left text-sm leading-4 font-medium text-gray-900 uppercase tracking-wider">Number Of Leads</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
      `;
  
      $.each(data, (index, Values) => {
        if (index < 5) {
          cards += `
            <tr class="${index % 2 === 0 ? 'bg-gray-50' : 'bg-white'} hover:bg-gray-100">
              <td class="px-6 py-4 whitespace-no-wrap">
                <div class="flex items-center">
                  <div class="flex-shrink-0 bg-indigo-200 h-10 w-10 rounded-full flex items-center justify-center">
                    <span class="material-symbols-outlined text-gray-600 text-28">
                      groups
                    </span>
                  </div>
                  <div class="ml-4">
                    <div class="text-sm leading-5 font-medium text-gray-900">${Values.name || ''}</div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-no-wrap">
                <div class="text-sm leading-5 text-gray-900 text-16">${Values.num_leads || ''}</div>
              </td>
            </tr>
          `;
        }
      });
  
      cards += `
              </tbody>
            </table>
            <div class="px-6 py-4 bg-gray-50 text-right">
              <a href="#" class="text-sm leading-5 font-medium text-gray-500 hover:text-gray-900 transition duration-150 ease-in-out">See more details</a>
            </div>
          </div>
        </div>
      `;
  
      return cards;
    }
    customer_data(data) {
      let cards = `
        <div class="overflow-x-auto">
          <div class="align-middle inline-block min-w-full shadow-lg rounded-lg border border-gray-200">
            <table class="min-w-full border border-gray-200">
              <thead class="bg-gradient-to-r from-blue-100 to-indigo-200">
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
      `;
    
      $.each(data, (index, Values) => {
        if (index < 5) {
          cards += `
             <a href="" class="w-full flex items-center justify-between mt-2">
                <span class="flex items-center justify-start text-12">
                    <span class="material-symbols-outlined text-18 mr-1 text-orange-800">person</span>
                    ${Values.customer_name}
                </span>
                <span class="flex items text-[10px] justify-end">
                    ${Values.number_of_services} Services
                    <span class="material-symbols-outlined text-15 ml-2">chevron_right</span>
                </span>
            </a> 
          `;
        }
      });
    
      cards += `
              </tbody>
            </table>
          </div>
        </div>
      `;
    
      return cards;
    }
    appointment(data) {
      let cards = `
        <div class="flex flex-col space-y-4">
          <div class="flex flex-row mb-4 p-4 bg-gray-100 rounded-lg shadow">
            <div class="w-1/3 text-sm font-semibold text-gray-700">Client</div>
            <div class="w-1/3 text-sm font-semibold text-gray-700">Date</div>
            <div class="w-1/3 text-sm font-semibold text-gray-700">Status</div>
          </div>
      `;
    
      $.each(data, (index, Values) => {
        if (index < 6) {
          cards += `
            <div class="flex flex-row mb-2 p-4 bg-white rounded-lg shadow hover:bg-gray-100 transition duration-200 ease-in-out">
              <div class="w-1/3 text-sm text-gray-800">${Values.customer_or_prospect_or_lead}</div>
              <div class="w-1/3 text-sm text-gray-800">${Values.created_on}</div>
              <div class="w-1/3 text-sm text-gray-800">${Values.status}</div>
            </div>
          `;
        }
      });
    
      cards += `
        </div>
      `;
    
      return cards;
    }
    
    top_sales_person(data) {        
        let card = `<h1></h1>`;
        $.each(data, (index, value) => {
            if (index < 3) {
                card += `
                   <div class="h-full flex-1 flex justify-center items-center flex-col">
                        <div class="h-[88px] w-[88px] bg-red-400 rounded-full border-[4px] border-slate-500 relative">
                            <img class="h-full w-full object-cover rounded-full" src="{% static 'images/avata/avata1.jpeg' %}" alt="avata">
                            <span class="flex justify-center items-center absolute -top-2 rounded-full right-3 h-[30px] w-[30px] bg-slate-500/60 backdrop-blur-[4px] text-white text-[12px] font-semibold">2nd</span>
                        </div>
                        <span class="font-semibold mt-2">${value.name || ""}</span>
                        <span class="font-light text-[12px]">No. Of Sales ${value.sales}</span>
                    </div>  
                `;
            }
        });
        return card;
      }

    weekly_task(data){
        let card = ``
        $.each(data,  (index, value) =>{           
          if (index < 4) {
            card += `
               <div class="flex flex-col items-center p-3 bg-default/10 rounded-md w-full">
                  <span class="material-symbols-outlined border border-default rounded-full h-8 w-8 flex items-center justify-center text-default text-lg">
                      pending
                  </span>
                  <p class="font-semibold text-base mt-2 text-default">${value.task_name}</p>
                  <div class="flex justify-between items-center gap-1 w-full mt-2">
                      <p class="text-xs text-default-500 ml-6">${value.expected_end_date}</p>
                  </div>
              </div> 
         `;
          }
           
        });
        return card
    }
    close_sales(data) {                
      let card = `<h1>
        <div class="grid grid-cols-11 w-full h-[30px] bg-default text-theme_text_color text-11 rounded-t rounded-md mt-2 gap-4 px-4">
            <span class="flex items-center justify-start col-span-4">
                <span class="material-symbols-outlined mr-1 text-orange-600">person</span>
                Customer
            </span>
            <span class="flex items-center justify-start col-span-3">
                <span class="material-symbols-outlined mr-1 text-indigo-600">diversity_3</span>
                Effective From
            </span>
            <span class="flex items-center justify-end col-span-2">
                <span class="material-symbols-outlined mr-1 text-blue-600">event</span>
                Expiring On
            </span>
        </div>
      </h1>`;
      $.each(data, (index, keys) => {
                if (index < 3) {
                  card += `
                  <div class="w-full h-full overflow-y-auto sales_pipeline_latest_closed_sales relative" id="">
                      <div class="grid grid-cols-11 w-full h-[30px] bg-gray-100 text-11 rounded-t rounded-md mt-2 gap-4 px-4">
                          <span class="flex items-center justify-start col-span-4">
                          ${keys.customer || ""}
                          </span>
                          <span class="flex items-center justify-start col-span-3">
                          ${keys.effective_date}
                          </span>
                          <span class="flex items-center justify-end col-span-2">
                          ${keys.expiring_date}
                          </span>
                      </div>
                  </div>
                  `;
                }
            });
            return card;
        }
    contract_stats_(data){
        let card =''
        $.each(data, (index, value)=>{
            if (index<=6){
                card += `
                <!-- Contract Item -->
                <div class="border border-dotted border-default rounded-lg bg-default/10">
                    <div class="flex gap-2 items-center">
                    <span class="material-symbols-outlined text-default text-xl flex items-center justify-center text-theme_text_color">contract_edit</span>
                    <p class=" text-default">${value.name}</p>
                    </div>
                    <div class="flex justify-center items-center justify-between p-2"><small class="text-sm text-default ml-6">Expiry Date</small>
                    <p class="border border-dotted border-default rounded-md h-4 w-28 flex justify-center items-center">${value.end_date}</p>
                    </div>
                </div> 
                            `
            }
        })
        return card
    }
    overdue_workplan_tasks(data){
      let card=``
      $.each(data,  (index, value) =>{ 
         if (index <=6){
          card += `
              <div class="flex items-center justify-center justify-between gap-2">
                    <div class="bg-red-200 h-8 w-2"></div>
                    <div class="flex flex-col">
                    <p class="">${value.task}</p>
                    <div class="flex items-center justify-center gap-6">
                        <small>Days Delayed</small>
                        <small>${value.days}</small>
                    </div>
                    </div>
                </div>
           `
         }
      });
      return card
    }
    top_selling_servivces(data){
      let card =''
      $.each(data, (index, value)=>{
          if (index<=6){
              card += `
               <!-- Product 1 -->
                <div class="flex gap-2 items-center">
                    <div class="bg-default h-4 w-4 rounded-md flex justify-center items-center"></div>
                    <div class="flex justify-between w-full">
                        <div class="text-gray-600 font-medium w-28 truncate">${value.product_name}</div>
                        <div class="text-gray-800 font-semibold flex justify-center items-center border border-gray-400 h-4 w-auto rounded-md">${value.quantity_sold}</div>
                    </div>
                </div>
                          `
          }
      })
      return card
  }
    create_dashboard_empty_content_card($wrapper) {
      lite.utils.add_empty_component({ $wrapper: $wrapper, text: "No Data Found.", classnames: "h-full mt-5" })
      $wrapper.append(`
          
      `)
   }
}
