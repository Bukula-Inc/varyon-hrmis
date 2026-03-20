import {
    advance_leave_validations,
    on_end_time_field_change,
    update_imprest_amount,
    employee_annual_salary,
    populate_form,
    update_imprest_retirement_row,
    update_retired_amount,
    update_retired_and_bal_amount,
    provide_model,
    update_with_doc_data,
    populate_personal_loan,
    get_ot_claim,
    calc_ot_amt
} from "../payroll/core.js";
import {
    leave_days,
    leave_date_validate,
    recalculate_expense_total,
    extend_self_appraisal_fields,
    extend_appraisal_fields,
    leave_hours,
    on_from_date_plan,
    interview_rating_by_staff,
    training_program_duration,
    populate_training_app,
    appraise_your_self_,
    self_rating_appraisal,
    prepopulated_behavioral_imperatives,
    commutated_leave_days,
    seperation_notice_period,
    price_distribution,
    limit_payment_duration,
    recruitment_budget,
    calculate_interview_ratings,
    on_exit_interview_questionnair,
    filled_sits_in_designation,
    job_variance,
    fetch_budget,
    pull_exit_interview_questions,
    fetch_accounts_from_hr_settings,
    calculate_acting_appointment_days
} from "../hr/core.js"

import {
    // recalculate_imprest_retirement,
    recalculate_imprest,
    validate_imprest,
    get_full_name,
    staff_survey_feedback,
    interview_rating_staff,
    witness_func,
} from "../staff/core.js"


export const medical_welfare = {
    on_field_change: {
        welfare_type: [price_distribution, limit_payment_duration],
        welfare_expense: [price_distribution],
        pay_length_unit: [limit_payment_duration],
        payment_length: [limit_payment_duration],
    }
}
export const staff_interview_evaluator = {
    on_field_change: {
        interview: [interview_rating_staff],
        designation: [interview_rating_by_staff]
    }
}
export const leave = {
    on_field_change:{
        to_date: [leave_days],
        to_time: [leave_hours],
    },
    custom_validation: [leave_date_validate],
}

export const overtime_claim = {
    on_field_change: {
        employee: [get_ot_claim],
        to_time: [calc_ot_amt],
    },
}
export const staff_overtime = {
    on_field_change: {
        end_time: [on_end_time_field_change],
    },
}

export const overtime = {
    on_field_change: {
        end_time: [on_end_time_field_change],
    },
}
export const staff_employee_welfare_feedback = {
    on_field_change: {
        survey: [staff_survey_feedback],
    },
}
// export const staff_appraisal = {
//     form_fields_extender: extend_self_appraisal_fields, 
    
//   }
export const staff_appraisal = {
    on_load: [prepopulated_behavioral_imperatives],
    on_field_change: {
        employee_id: [appraise_your_self_],
        rating_po: [self_rating_appraisal],
        rating_b: [self_rating_appraisal],
    }
}

export const staff_360_degree_appraisal = {
    form_fields_extender: extend_appraisal_fields, 
  }

export const training_program_application_form = {
    on_load:[training_program_duration],
    on_field_change: {
        amount: [recalculate_expense_total],
        start_date: [training_program_duration],
        end_date: [training_program_duration],
        name: [populate_training_app],
    }
}

export const staff_leave_plan = {
    on_field_change: {
        to_date: [on_from_date_plan],
    }
}

export const staff_advance = {
}


export const application_for_a_personal_loan = {
    on_field_change: {
        employee_no :[populate_personal_loan],
    }
}

export const requisition = {
    on_field_change: {
        item: [],
        qty: [],
        total_amount: [],
    },
    on_row_add: [],
}
export const staff_performance_agreement = {
    on_field_change: {
        first_name: [get_full_name],
        last_name: [get_full_name],
        middle_name: [get_full_name],
    },
}

export const staff_leave_commutation = {
    on_field_change: {
        commutated_days: [commutated_leave_days],
    }
}

export const staff_leave_commutation_memo = {
    on_field_change: {
        commutated_days: [commutated_leave_days],
    }
}

export const separation = {
    on_field_change: {
        resignation_date: [seperation_notice_period],
        last_day_of_work: [seperation_notice_period],
    }
}

export const witness = {
    on_load: [witness_func],
}

export const interview_rating = {
    on_field_change: {
        interview: [interview_rating_by_staff],
        behavioral_rating: [calculate_interview_ratings],
        technical_rating: [calculate_interview_ratings],
    }
}

export const exit_interview = {
    on_field_change: {
        designation: [on_exit_interview_questionnair]
    }
}

export const staff_requisition_form = {
    on_load: [fetch_budget],
    on_field_change: {
        employee_grade: [recruitment_budget],
        number_required: [recruitment_budget],
        staffing_job_title: [filled_sits_in_designation],
        approved_establishment : [job_variance],
        budget_needed: []

    }
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

export const retirement ={
    custom_validation: [],
    on_field_change: {
        petty_cash: [populate_form],
        imprest_a: [populate_form],
        imprest_b: [populate_form],
        imprest_c: [populate_form],
        unit_price_of_usage: [update_imprest_retirement_row],
        usage_length: [update_imprest_retirement_row],
        pc_retirement_amount: [update_retired_amount],
        imprest_obtained: [update_retired_and_bal_amount],
        retired_amount: [update_retired_and_bal_amount],
    },
    on_row_remove: [update_imprest_amount],
}

export const cash_repayment ={
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

export const exit_interview_questionnaire = {
    on_load: [pull_exit_interview_questions, ],
    on_field_change: {
        // designation: [pull_exit_interview_questions]
    }
}

export const graduate_development_enrollment_requisition = {
    on_load: [fetch_budget],
    on_field_change: {
        employee_grade: [recruitment_budget],
        number_required: [recruitment_budget]
    }
}

export const certificate_of_service ={
    on_load: [fetch_accounts_from_hr_settings],
    on_field_change: {
    },
    custom_validation: [],
}

export const certificate_of_service_seasonal_employment ={
    on_load: [fetch_accounts_from_hr_settings],
    on_field_change: {
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