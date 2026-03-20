// Index JS
import {
    calculate_payroll,
    on_payroll_load,
    on_end_time_field_change,
    get_salary_components_payroll,
    validate_imprest,
    update_imprest_retirement_row,
    update_imprest_amount,
    employee_annual_salary,
    populate_form,
    update_retired_amount,
    update_retired_and_bal_amount,
    provide_model,
    update_with_doc_data,
    populate_personal_loan,
    recalculate_totals,
    get_ot_claim,
    calc_ot_amt,
    load_temp_employees,
    calc_rate_and_amount,
} from "./core.js";

// export const payroll_processor = {
//     on_load: [on_payroll_load],
//     on_field_change: {
//         company: [calculate_payroll],
//         currency: [calculate_payroll],
//         convertion_rate: [calculate_payroll],
//         from_date: [on_payroll_load],
//         to_date: [on_payroll_load],
//     },
//     on_row_remove: [recalculate_totals],
// }

export const payroll_processor = {
    on_load: [on_payroll_load],
    on_field_change: {
        company: [calculate_payroll],
        currency: [calculate_payroll],
        convertion_rate: [calculate_payroll],
        from_date: [on_payroll_load],
        to_date: [on_payroll_load],
    },
    on_row_remove: [recalculate_totals],
}

export const overtime = {
    on_field_change: {
        end_time: [on_end_time_field_change],
    },
}
export const overtime_claim = {
    on_field_change: {
        employee: [get_ot_claim],
        to_time: [calc_ot_amt],
    },
}

export const employee_grade = {
    // on_load: [get_salary_components_payroll]
}

export const imprest_form_20_a = {
    custom_validation: [validate_imprest],
    on_field_change: {
        amounts: [update_imprest_amount],
        initiator: [employee_annual_salary],
    },
    on_row_remove: [update_imprest_amount],
    
}

export const imprest_form_20_b = {
    custom_validation: [validate_imprest],
    on_field_change: {
        amounts: [update_imprest_amount],
        initiator: [employee_annual_salary],
    },
    on_row_remove: [update_imprest_amount],
}

export const imprest_form_20_c = {
    custom_validation: [validate_imprest],
    on_field_change: {
        amounts: [update_imprest_amount],
        initiator: [employee_annual_salary],
    },
    on_row_remove: [update_imprest_amount],
}

export const expense_retirement ={
    custom_validation: [],
    on_field_change: {
        petty_cash: [populate_form],
        imprest_a: [populate_form],
        imprest_b: [populate_form],
        imprest_c: [populate_form],
        unit_price_of_usage: [update_imprest_retirement_row],
        usage_length: [update_imprest_retirement_row],
        obtained_amount: [update_retired_and_bal_amount],
        retired_amount: [update_retired_and_bal_amount],
    },
    on_row_remove: [update_imprest_amount],
}

export const cash_repayment = {
    on_field_change: {
        repayment_type :[provide_model],
        medical_recovery :[update_with_doc_data],
        long_term_sponsorship :[update_with_doc_data],
        professional_membership_subscription :[update_with_doc_data],
        personal_loan_application :[update_with_doc_data],
        house_loan_application :[update_with_doc_data],
        advance_application :[update_with_doc_data],
    }
}

export const application_for_a_personal_loan ={
    on_field_change: {
        employee_no :[populate_personal_loan],
    }
}

export const personal_loan_application ={
    on_field_change: {
        employee_no :[populate_personal_loan],
    }
}

export const pay_for_temps_or_seasonal_employee = {
    on_load: [load_temp_employees],
    on_field_change: {
        days :[calc_rate_and_amount],
    }
}