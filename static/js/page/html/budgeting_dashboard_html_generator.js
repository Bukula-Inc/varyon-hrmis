import { color_codes } from "../../constants/colors.js"

export default class Budgeting_Dashboard_HTML_Generator{
    constructor(){
        this.color_codes = color_codes
    }

    // budgeting dashboard

    create_revenue_line_row(data){
        return `
            <div class="flex items-start justify-start overflow-hidden intro-y">
                <span class="material-symbols-outlined text-17 mr-2 text-default"> trending_up </span>
                <a href="/app/budgeting/budget_item?app=budget_item&page=info&content_type=budget%20item&doc=${data?.id}" class="hover:text-default overflow-ellipsis truncate">${data.name}</a>
            </div>
        `
    }
    create_expense_row(data){
        return `
            <div class="flex items-start justify-start overflow-hidden intro-y">
                <span class="material-symbols-outlined text-17 mr-2 text-default"> trending_down </span>
                <a href="/app/budgeting/budget_item?app=budget_item&page=info&content_type=budget%20item&doc=${data?.id}" class="hover:text-default overflow-ellipsis truncate">${data.name}</a>
            </div>
        `
    }
    create_top_income_expense_rows(data) {
        let rows = '';
        data.forEach(item => {
            if (item.total !== undefined) {
                let row = `<div><h4>${item.key}</h4><small class="text-gray-500 text-11">ZMW&nbsp;${lite.utils.thousand_separator(item.total, 2)}</small></div>`;
                rows += row;
            }
        });
        return rows;
    }
    create_objective_row(text){
        return `<p class="">  ${text}</p>`;
    }

    create_departmental_analysis_row(data) {
        let income_percent = parseInt(data.income_ratio) - 100;
        let expense_percent = parseInt(data.expense_ratio) - 100;
    
        let income_trend = "trending_up";
        let income_trend_color = "green";
    
        if (income_percent < 0) {
            income_trend = "trending_down";
            income_trend_color = "red";
        }
        else if (income_percent == 0) {
            income_trend = "trending_flat";
            income_trend_color = "gray";
        }
    
        let expense_trend = "trending_up";
        let expense_trend_color = "green";
    
        if (expense_percent < 0) {
            expense_trend = "trending_down";
            expense_trend_color = "red";
        }
        else if (expense_percent == 0) {
            expense_trend = "trending_flat";
            expense_trend_color = "gray";
        }
    
        return `
            <div class="w-full h-full flex items-center justify-start col-span-2">${data.department}</div>
            <div class="w-full h-full flex items-center justify-start col-span-2">
                <span class="material-symbols-outlined text-${income_trend_color}-400 mr-1"> ${income_trend} </span>${income_percent.toFixed(0)}% 
                (${lite.utils.thousand_separator(data.average_income || 0, 2) })
            </div>
            <div class="w-full h-full flex items-center justify-start col-span-2">
                <span class="material-symbols-outlined text-${expense_trend_color}-400 mr-1"> ${expense_trend} </span>${expense_percent.toFixed(0)}% 
                (${lite.utils.thousand_separator(data.average_expense || 0, 2) })
            </div>
        `;
    }
    
    create_budget_type_row(data, index) {
        return `<div class="w-full h-full flex items-center justify-center">${index + 1}</div>
                <div class="w-full h-full flex items-center ml-5 justify-start col-span-3">${data.name}</div>
                <div class="w-full h-full flex items-center ml-5 justify-start col-span-2">ZMW&nbsp;${lite.utils.thousand_separator(data.metrics.total_incomes || 0, 2) }</div>
                <div class="w-full h-full flex items-center ml-5 justify-start col-span-2">ZMW&nbsp;${lite.utils.thousand_separator(data.metrics.total_expenses || 0, 2)}</div>
                <div class="w-full h-full flex items-center ml-5 justify-start col-span-2">ZMW&nbsp;${lite.utils.thousand_separator(data.metrics.net_balance || 0, 2)}</div>`;
    }
    create_variance_row(data, index) {
        let actual_incomes = Math.random() * (data.metrics.total_incomes * 1.1)
        let actual_expenses = Math.random() * (data.metrics.total_expenses * 1.1)
        let actual_net_balance = actual_incomes - actual_expenses
        let variance = actual_net_balance - data.metrics.net_balance

        return `<div class="w-full h-full flex items-center justify-center">${index + 1}</div>
                <div class="w-full h-full flex items-center ml-5 justify-start col-span-3">${data.name}</div>
                <div class="w-full h-full flex items-center ml-5 justify-start col-span-2">ZMW&nbsp;${lite.utils.thousand_separator(data.metrics.total_incomes || 0, 2) }</div>
                <div class="w-full h-full flex items-center ml-5 justify-start col-span-2">ZMW&nbsp;${lite.utils.thousand_separator(actual_incomes || 0, 2) }</div>
                <div class="w-full h-full flex items-center ml-5 justify-start col-span-2">ZMW&nbsp;${lite.utils.thousand_separator(data.metrics.total_expenses || 0, 2)}</div>
                <div class="w-full h-full flex items-center ml-5 justify-start col-span-2">ZMW&nbsp;${lite.utils.thousand_separator(actual_expenses || 0, 2)}</div>
                <div class="w-full h-full flex items-center ml-5 justify-start col-span-2">ZMW&nbsp;${lite.utils.thousand_separator(variance || 0, 2)}</div>`;
    }
}