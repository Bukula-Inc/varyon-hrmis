import {
    on_contract_change,
    func,
    get_emp_name,
    leave_days,
    leave_date_validate,
    on_employee_grade_change,
    on_create_user,
    employee_date_validate,
    interview_time_validation,
    interview_schedule_time_validation,
    validateTime,
    on_leave_policy_leave_type_changed,
    on_interview_schedule_change,
    on_field_change_bonus_type,
    on_final_statement,
    recalculate_expense_total,
    on_load_emp_load,
    on_bonus_percentage,
    get_emp_by_policy,
    years_checker,
    get_leave_type,
    on_from_date_plan,
    leave_hours,
    get_job_opening,
    commutated_leave_days,
    on_exit_interview_questionnair,
    get_tasks,
    price_distribution,
    limit_payment_duration,
    company_skill_levy,
    interview_rating_by_staff,
    appraise_your_self,
    rate_behavior,
    rate_performance_obj,
    interview_rating_validation,
    training_program_duration,
    prepopulated_behavioral_imperatives,
    seperation_notice_period,
    update_total,
    policy_type,
} from "./core.js";


export const self_appraisal = {
    on_load: [prepopulated_behavioral_imperatives],
    on_field_change: {
        employee_id: [appraise_your_self],
        rating_po: [rate_performance_obj],
        rating_b: [rate_behavior],
    }
}

export const training_program = {
    on_load:[training_program_duration],
    on_field_change: {
        amount: [recalculate_expense_total],
        start_date: [training_program_duration],
        end_date: [training_program_duration],
    }
}
export const interview_rating = {
    on_field_change: {
        interview: [interview_rating_by_staff],
        rating: [interview_rating_validation],
    }
}
export const exit_interview = {
    on_field_change: {
        designation: [on_exit_interview_questionnair]
    }
}

export const leave_commutation = {
    on_field_change: {
        commutated_days: [commutated_leave_days]
    }
}

export const bonus_planing = {
    on_field_change: {
        bonus_type: [on_field_change_bonus_type]
    }
}

export const staffing_plan = {
    on_field_change: {
        vacancies: [func],
        estimated_cost: [func],
    }
}

export const employee = {
    on_load: [on_load_emp_load],
    on_field_change: {
        first_name: [get_emp_name],
        middle_name: [get_emp_name],
        last_name: [get_emp_name],
        employee_grade: [on_employee_grade_change],
        main_role: [on_create_user],
        date_of_joining: [years_checker]
    },
    custom_validation: [employee_date_validate],
}

export const leave_application = {
    on_field_change:{
        to_date: [leave_days],
        to_time: [leave_hours],
    },
    custom_validation: [leave_date_validate],
}

export const leave_allocation = {
    on_field_change:{
        main_policy: [get_emp_by_policy],
    }
}



export const training_event = {
    custom_validation: [validateTime],
}
export const staff_interview_evaluator = {
    on_field_change: {
        interview: [interview_rating_by_staff],
        designation: [interview_rating_by_staff]
    }
}
export const interview = {
    custom_validation: [interview_time_validation],
    on_field_change: {
        short_listed_applicant: [on_interview_schedule_change],
        designation: [interview_rating_by_staff]
    },
}

export const interview_schedule = {
    custom_validation: [interview_schedule_time_validation],
}

export const leave_policy = {
    on_field_change:{
        policy_for: [policy_type],
    }
}


export const final_statement = {
    on_field_change: {
        employee_id: [on_final_statement],
    }
}

export const employee_promotion = {
    on_field_change: {
        employee_grade: [on_employee_grade_change]
    }
}


export const gratuity = {
    on_field_change: {
        expiry_contract_date: [on_contract_change],
    },
}

export const bonus = {
    on_field_change: {
        is_percentage: [on_bonus_percentage]
    }
}

export const leave_plan = {
    on_field_change: {
        to_date: [on_from_date_plan],
        // planner: [get_tasks],
    }
}

export const skill_levy ={
    on_load: [company_skill_levy],
}

export const job_application = {
    on_field_change: {
        job_opening: [get_job_opening]
    }
}

export const case_outcome = {
    on_field_change: {
        job_opening: [get_job_opening]
    }
}

export const welfare = {
    on_field_change: {
        welfare_type: [price_distribution, limit_payment_duration],
        welfare_expense: [price_distribution],
        pay_length_unit: [limit_payment_duration],
        payment_length: [limit_payment_duration],
    }
}

export const employee_separation = {
    on_field_change: {
        resignation_date: [seperation_notice_period],
        last_day_of_work: [seperation_notice_period],
    }
}

export const sitting_allowance_claim = {
    on_field_change: {
        amount: [update_total]
    }
}
