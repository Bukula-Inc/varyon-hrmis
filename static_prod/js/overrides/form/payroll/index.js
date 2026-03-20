// Index JS
import {
    calculate_payroll,
    on_payroll_load,
    on_end_time_field_change,
    // on_payroll_row_removed,
    // on_payroll_new_employee_row_added,
    get_salary_components_payroll,
    advance_leave_validations,
} from "./core.js";

export const payroll_processor = {
    on_load: [on_payroll_load],
    on_field_change: {
        // employee: [on_payroll_new_employee_row_added],
        company: [calculate_payroll],
        currency: [calculate_payroll],
        convertion_rate: [calculate_payroll],
        from_date: [on_payroll_load],
        to_date: [on_payroll_load],

    },
    // on_row_remove: [on_payroll_row_removed]
}

export const overtime = {
    on_field_change: {
        end_time: [on_end_time_field_change],
    },
}

export const employee_grade = {
    on_load: [get_salary_components_payroll]
}

export const advance_application = {
    on_field_change: {
        amount: [advance_leave_validations]
    },
}