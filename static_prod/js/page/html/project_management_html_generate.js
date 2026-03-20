export default class Dynamic_Project_Management_Html {
    constructor() {
    }
    project_details(data) {
        let cards = `
        <table class="min-w-full bg-white rounded-lg overflow-hidden">
             <thead class="bg-violet-950 text-white">
                <tr>
                    <th class="py-2 px-4 text-left font-semibold">Project Name</th>
                    <th class="py-2 px-4 text-left font-semibold">Project Manager</th>
                    <th class="py-2 px-4 text-left font-semibold">Status</th>
                </tr>
            </thead>
        `;
    
        $.each(data, (index, value) => {            
            if (index < 5) {
                cards += `
               <tbody class="text-gray-700">
                    <tr class="bg-gray-100 border-b border-gray-200">
                        <td class="py-2 px-4">${value.Project_Name}</td>
                        <td class="py-2 px-4">${value.Project_Manager || ""}</td>
                        <td class="py-2 px-4 text-purple-600">${value.Status}</td>
                    </tr>
                </tbody>
                `;
            }
        });
    
        cards += `
             </table>
        `;
    
        return cards;
    }
    project_timeline(data){
        let cards = ``;
        $.each(data, (index, value) => {            
            if (index < 3) {
                cards += `
                  <div class="p-2">
                    <p class="text-default">${value.project_name}</p>
                    <div class="flex justify-between text-sm text-default">
                        <div class="flex items-center gap-2">
                        <span class="ml-4">Total Days:</span>
                        <span>${value.total_days}</span>
                        </div>
                        <div class="flex items-center gap-2">
                        <span class="ml-4">Remaining Days:</span>
                        <span>${value.remaining_days}</span>
                        </div>
                    </div>
                    </div>

                `;
            }
        });
        return cards;
    }
    get_top_team_member(data)
    {
        let cards = ``;
        $.each(data, (index, value) => {            
            if (index < 3) {
                cards += `
                   <!-- Content -->
                    <div class="relative w-full overflow-hidden p-2 rounded-lg border border-dotted border-b">
                        <!-- Icon and Name -->
                        <div class="flex items-center gap-2 mb-2">
                            <span class="material-symbols-outlined flex justify-center items-center bg-gray-100 border border-dotted border-default h-4 w-4 rounded-full text-theme_text_color">
                                person
                            </span>
                            <p class="font-medium text-gray-800 text-xs">${value.team_member}</p>
                        </div>

                        <!-- Task Stats -->
                        <div class="ml-5 flex justify-between">
                            <p class="flex items-center gap-1 text-gray-600 text-xs rounded-md">
                                <span>Total Tasks:</span>
                                <span class="font-bold text-gray-800 border border-dotted border-default h-4 w-4 rounded-full flex items-center justify-center">${value.total_tasks}</span>
                            </p>
                            <p class="flex items-center gap-1 text-gray-600 text-xs rounded-md">
                                <span>Completed:</span>
                                <span class="font-bold text-green-600 border border-dotted border-default h-4 w-4 rounded-full flex items-center justify-center">${value.completed_on_time}</span>
                            </p>
                        </div>
                    </div>
                `;
            }
        });
        return cards;
    }
    p_overdue_tasks(data){
        let cards = ``;
        $.each(data, (index, value) => {            
            if (index < 3) {
                cards += `
                   <!-- Content -->
                    <div class="relative w-full overflow-hidden p-2 rounded-lg border border-dotted border-b">
                        <!-- Icon and Name -->
                        <div class="flex items-center gap-2 mb-2">
                            <span class="material-symbols-outlined flex justify-center items-center bg-gray-100 border border-dotted border-default h-4 w-4 rounded-full text-theme_text_color">
                                person
                            </span>
                            <p class="font-medium text-gray-800 text-xs">${value.name}</p>
                        </div>

                        <!-- Task Stats -->
                        <div class="ml-5 flex justify-between">
                            <p class="flex items-center gap-1 text-gray-600 text-xs rounded-md">
                                <span>Total Tasks:</span>
                                <span class="font-bold text-gray-800 border border-dotted border-default h-4 w-4 rounded-full flex items-center justify-center">${value.total}</span>
                            </p>
                            <p class="flex items-center gap-1 text-gray-600 text-xs rounded-md">
                                <span>Overdue Tasks:</span>
                                <span class="font-bold text-green-600 border border-dotted border-default h-4 w-4 rounded-full flex items-center justify-center">${value.overdue}</span>
                            </p>
                        </div>
                    </div>
                `;
            }
        });
        return cards;
    }
    project_tasks(data) {
        let cards = `
            <table class="min-w-full bg-white rounded-lg overflow-hidden">
             <thead class="bg-violet-950 text-white">
                <tr>
                    <th class="py-2 px-4 text-left font-semibold">Task Name</th>
                     <th class="py-2 px-4 text-left font-semibold">Project</th>
                    <th class="py-2 px-4 text-left font-semibold">End Date</th>
                    <th class="py-2 px-4 text-left font-semibold">Status</th>
                    <th class="py-2 px-4 text-left font-semibold">Assigned To</th>
                </tr>
            </thead>
        `;
    
        $.each(data, (index, value) => {
            if (index < 5) {
                cards += `
                   <tbody class="text-gray-700">
                    <tr class="bg-gray-100 border-b border-gray-200">
                        <td class="py-2 px-4">${value.Task_Name}</td>
                        <td class="py-2 px-4">${value.Project_Name}</td>
                        <td class="py-2 px-4">${value.End_Date}</td>
                        <td class="py-2 px-4 text-purple-600">${value.status}</td>
                        <td class="py-2 px-4 text-purple-600">${value.individual}</td>
                    </tr>
                  </tbody>
                `;
            }
        });
    
        cards += `
             </table>
        `;
    
        return cards;
    }

    // project teams 
    project_management_teams(data) {
        let cards = `
        <table class="min-w-full rounded-lg">
        <thead class="bg-blue-200">
            <tr>
                <th class="px-6 py-3 border-b-2 border-blue-300 text-left leading-4 text-gray-700 tracking-wider">Project Management Team</th>
            </tr>
        </thead>
        <tbody>
        `;

        $.each(data, (index, value) => {
            if (index < 5) {
                cards += `
                <tr class="hover:bg-blue-100 transition duration-150 ease-in-out ${index % 2 === 0 ? 'bg-blue-50' : 'bg-white'}">
                    <td class="px-6 py-4 border-b border-blue-300 flex items-center">
                        <div class="flex items-center justify-center bg-purple-100 rounded-full h-10 w-10">
                            <span class="material-icons text-orange-600 text-3xl"></span>
                        </div>
                        <div class="ml-3">
                            <h5 class="font-semibold text-lg text-gray-800">${value?.team_name}</h5>
                        </div>
                    </td>
                </tr>
                `;
            }
        });

        cards += `
            </tbody>
        </table>
        `;

        return cards;
    }
    create_review_data(data) {
        let cards = ``;
        $.each(data, (index, value) => {
            if (index < 3) {
                cards += `
                <div class="space-y-4 border border-default">
                    <div class="flex p-4 bg-purple-50 rounded-lg items-center justify-between">
                        <div class="flex-1">
                            <h3 class="font-semibold text-gray-800">Project: ${value?.Project_Name}</h3>
                            <p class="text-sm text-gray-500">Reviewed On: ${value?.Reviewed_On}</p>
                            <p class="text-sm text-purple-700 mt-2">Project Manager: ${value?.Project_Manager}</p>
                        </div>
                        <div class="shrink-0 flex justify-center items-center bg-purple-200 border border-purple-700 h-12 w-12 rounded-md">
                            <span class="material-symbols-outlined text-[28px] text-purple-500">assessment</span>
                        </div>
                    </div>
                </div>
                `;
            }
        });
        return cards;
    }
    project_manager(data) {
        let card = `
       
        `;
    
        $.each(data, (index, value) => {
            if (index < 3) {
                card += `
                    <li class="flex items-center mb-4">
                        <div>
                            <p class="text-lg font-semibold text-gray-800">${value.Project_Manager}</p>
                            <p class="text-sm text-gray-600">Projects Completed: ${value.Number_of_Projects}</p>
                        </div>
                    </li>
                `;
            }
        });
    
        card += `
              
        `;
    
        return card;
    }
    
    project_duration_overview(data) {          
        const { project_completion_times, data: tasks } = data; 
    
        let content = `
        <!-- Project Duration Overview -->
        <div class="my-8 text-default space-y-4 p-4">
            <h2 class="font-bold text-default">Project Completion Time</h2>
            <p><strong>Shortest Possible Completion:</strong> <span id="shortest-completion">${project_completion_times.shortest_completion || ''} days</span></p>
            <p><strong>Latest Possible Completion:</strong> <span id="latest-completion">${project_completion_times.latest_completion || ''} days</span></p>
            <p><strong>Current Expected Completion:</strong> <span id="current-completion">${project_completion_times.current_expected_completion || ''} days</span></p>
        </div>
    
        <!-- Task Table -->
        <div class="overflow-x-auto my-8">
            <table class="min-w-full table-auto border-collapse border border-gray-300">
                <thead class="bg-default/20">
                    <tr>
                        <th class="border border-default px-4 py-2 text-left">Task Name</th>
                        <th class="border border-default px-4 py-2 text-left">Duration (Days)</th>
                        <th class="border border-default px-4 py-2 text-left">Dependencies</th>
                        <th class="border border-default px-4 py-2 text-left">Start Date</th>
                        <th class="border border-default px-4 py-2 text-left">End Date</th>
                        <th class="border border-default px-4 py-2 text-left">Earliest Start</th>
                        <th class="border border-default px-4 py-2 text-left">Earliest Finish</th>
                        <th class="border border-default px-4 py-2 text-left">Lastest Start</th>
                        <th class="border border-default px-4 py-2 text-left">Lastest Finish</th>
                        <th class="border border-default px-4 py-2 text-left">Slack (Float)</th>
                        <th class="border border-default px-4 py-2 text-left">Status</th>
                        <th class="border border-default px-4 py-2 text-left">Delayed (Days)</th>
                    </tr>
                </thead>
                <tbody>
        `;    
        $.each(tasks, (index, task) => {            
            content += `
            <tr class="text-default">
                <td class="border border-default text-default px-4 py-2">${task['Task_Name']}</td>
                <td class="border border-default text-default px-4 py-2">${task['Duration (Days)']}</td>
                <td class="border border-default text-default px-4 py-2">${task.Dependencies || "No Dependancy Task"}</td>
                <td class="border border-default text-default px-4 py-2">${task['Start_Date'] || "No Date"}</td>
                <td class="border border-default text-default px-4 py-2">${task['End_Date'] || "No Date"}</td>
                <td class="border border-default text-default px-4 py-2">${task['Earliest_Start'] || "No Date"}</td>
                <td class="border border-default text-default px-4 py-2">${task['Earliest_Finish'] || "No Date"}</td>
                 <td class="border border-default text-default px-4 py-2">${task['Latest_Start'] || "No Date"}</td>
                <td class="border border-default text-default px-4 py-2">${task['Latest_Finish'] || "No Date"}</td>
                <td class="border border-default text-default px-4 py-2">${task.Slack || '0'}</td>
                <td class="border border-default text-default px-4 py-2">${task.Status || ''}</td>
                <td class="border border-default text-default px-4 py-2">${task.delayed_days || '0'}</td>
            </tr>
            `;
        });
    
        content += `
                </tbody>
            </table>
        </div>
    
        <!-- Project Impact of Delayed Tasks -->
        <div class="my-8 text-default space-y-4 p-4">
            <h2 class="font-bold text-[18px] text-default">Project Delay Overview</h2>
            <p>The project completion time has been impacted by <strong id="delayed-tasks-impact">${project_completion_times.delayed_days_impact || 0} days</strong> due to delayed tasks.</p>
        </div>
        `;
    
        return content;
    }
    project_review(data) {
        let cards = ``;
        $.each(data, (index, value) => {
            console.log(value);
            
            if (index < 3) {
                cards += `
                <div class="flex items-center justify-between rounded-lg pb-2 border border-default p-2">
                    <div>
                        <p class="font-medium text-slate-700 text-sm">${value.project_name}</p>
                        <p class="text-xs text-slate-500">Project Manager: ${value.project_manager}</p>
                    </div>
                    <span class="text-default text-xs font-semibold">${value.review_date}</span>
                    </div>
                </div>
                `;
            }
        });
        return cards;
    }
    p_stats(data) {
        let card = `
        <thead class="bg-gray-100 border-b">
          <tr>
            <th class="px-4 py-3 text-left text-sm font-semibold text-default">Project Name</th>
            <th class="px-4 py-3 text-center text-sm font-semibold text-default">Total Tasks</th>
             <th class="px-4 py-3 text-center text-sm font-semibold text-default">Completed Tasks</th>
            <th class="px-4 py-3 text-center text-sm font-semibold text-default">Overdue Tasks</th>
            <th class="px-4 py-3 text-center text-sm font-semibold text-default">Completion %</th>
          </tr>
        </thead>
        `;
        $.each(data, (index, value) => {   
            card += `
                <tr class="border-b hover:bg-gray-50">
                    <td class="px-4 py-3 text-gray-700 font-medium">${value.Project}</td>
                    <td class="px-4 py-3 text-center text-gray-700">${value.Total_Tasks}</td>
                    <td class="px-4 py-3 text-center text-blue-600 font-semibold">${value.Completed_Tasks}</td>
                    <td class="px-4 py-3 text-center text-red-600 font-semibold">${value.Overdue_Tasks}</td>
                    <td class="px-4 py-3 text-center">
                    <span class="text-sm bg-default/20 text-default py-1 px-2 rounded">${value.Completion_Percentage}</span>
                    </td>
                </tr>
            `;
        });
        return card;
    }
    
    create_dashboard_empty_content_card($wrapper) {
        lite.utils.add_empty_component({ $wrapper: $wrapper, text: "No Data Found.", classnames: "h-full mt-5" })
        $wrapper.append(`
            
        `)
    }
}