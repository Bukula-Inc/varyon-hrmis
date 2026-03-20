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
    on_interview_schedule_change,
    on_field_change_bonus_type,
    on_final_statement,
    recalculate_expense_total,
    on_load_emp_load,
    get_emp_by_policy,
    years_checker,
    on_from_date_plan,
    leave_hours,
    get_job_advertisement,
    commutated_leave_days,
    on_exit_interview_questionnair,
    price_distribution,
    limit_payment_duration,
    company_skill_levy,
    interview_rating_by_staff,
    appraise_your_self_,
    self_rating_appraisal,
    training_program_duration,
    prepopulated_behavioral_imperatives,
    seperation_notice_period,
    update_total,
    policy_type,
    get_bonus_employees,
    filled_sits_in_designation,
    calculate_interview_ratings,
    get_leave_schedule,
    leave_schedule_get_days,
    get_impact_on_budget,
    receiving_officer_for_clearance,
    recruitment_budget,
    pull_exit_interview_questions,
    job_variance,
    fetch_budget,
    interview_schedule_application_details,
    fetch_accounts_from_hr_settings,
    exit_interview_employee_details,
    calculate_acting_appointment_days,
    populate_certificate_of_service_for_temporal_employee
} from "./core.js";

export const leave_policy = {
    on_field_change:{
        policy_for: [policy_type],
    }
}

export const hr_budget = {
    on_field_change: {
        budget_line_expense: [get_impact_on_budget],
    },
}

export const leave_schedule = {
    on_field_change: {
        department: [get_leave_schedule],
        leave_type: [get_leave_schedule],
        to_date: [leave_schedule_get_days],
    },
}

export const appraise_your_self = {
    on_load: [prepopulated_behavioral_imperatives],
    on_field_change: {
        employee_id: [appraise_your_self_],
        rating_po: [self_rating_appraisal],
        rating_b: [self_rating_appraisal],
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
        behavioral_rating: [calculate_interview_ratings],
        technical_rating: [calculate_interview_ratings],
    }
}
export const exit_interview = {
    // on_laod: [pull_exit_interview_questions],
    on_field_change: {
        designation: [on_exit_interview_questionnair]
    }
}

export const leave_commutation = {
    on_field_change: {
        commutated_days: [commutated_leave_days]
    }
}

export const leave_commutation_memo = {
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
        leave_type: [leave_days],
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
    application: [interview_schedule_application_details],
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

export const bonus = {
    on_load: [get_bonus_employees],
}


export const gratuity = {
    on_field_change: {
        // expiry_contract_date: [on_contract_change],
        expiry_contract_date: [on_contract_change],
    },
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
        // job_advertisement: [get_job_advertisement]
    }
}

export const case_outcome = {
    on_field_change: {
        job_opening: [get_job_advertisement]
    }
}

export const recovery_of_medical_bills = {
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

export const sitting_allowance = {
    on_field_change: {
        amount: [update_total]
    }
}

export const graduate_development_enrollment_requisition = {
    on_load: [fetch_budget],
    on_field_change: {
        employee_grade: [recruitment_budget],
        number_required: [recruitment_budget]
    }
}

export const staff_requisition = {
    on_load: [fetch_budget],
    on_field_change: {
        employee_grade: [recruitment_budget],
        number_required: [recruitment_budget],
        staffing_job_title: [filled_sits_in_designation],
        approved_establishment : [job_variance],
        budget_needed: []

    }
}

export const separation_clearance_item = {
    on_field_change: {
        hand_in_status: [receiving_officer_for_clearance],
        // number_required: [recrutement_budget],
        // staffing_job_title: [filled_sits_in_designation]

    }
}

export const exit_interview_questionnaire = {
    on_load: [pull_exit_interview_questions, ],
    on_field_change: {
        employee_seperation: [exit_interview_employee_details],
    }
}

export const recruit_employee ={
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

export const certificate_of_service ={
    on_load: [fetch_accounts_from_hr_settings],
    on_field_change: {
    },
    custom_validation: [],
}

export const certificate_of_service_temporal_employee ={
    on_load: [fetch_accounts_from_hr_settings],
    on_field_change: {
        employee_seperation: [populate_certificate_of_service_for_temporal_employee],

    },
    custom_validation: [],
}

export const acting_appointment_memo ={
    on_field_change: {
        start_date: [calculate_acting_appointment_days],
        end_date: [calculate_acting_appointment_days],
    },
    custom_validation: [],
}

export const acting_appointment ={
    on_field_change: {
        start_date: [calculate_acting_appointment_days],
        end_date: [calculate_acting_appointment_days],
    },
    custom_validation: [],
}
