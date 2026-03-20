import {
    advance_leave_validations,
    on_end_time_field_change,
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
    appraise_your_self,
    rate_performance_obj,
    rate_behavior,
    prepopulated_behavioral_imperatives,
    commutated_leave_days,
    seperation_notice_period,
} from "../hr/core.js"

import {
    // recalculate_imprest_retirement,
    recalculate_imprest,
    validate_imprest,
    get_full_name,
    staff_survey_feedback,
    interview_rating_staff,
    recalculate_imprest_retirement_expenses,
    popluate_imprest_data,
} from "../staff/core.js"

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

export const staff_overtime = {
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
        employee_id: [appraise_your_self],
        rating_po: [rate_performance_obj],
        rating_b: [rate_behavior],
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


// export const staff_imprest = {
//     on_field_change: {
//         amount: []
//     }
// }


export const imprest = {
    custom_validation: [validate_imprest],
    on_field_change: {
        requested_amount: [recalculate_imprest],
        approved_amount: [recalculate_imprest],
        requested_currency: [recalculate_imprest],
        debit_account: [recalculate_imprest],
        credit_account: [recalculate_imprest],
        debit_account_currency: [recalculate_imprest],
        credit_account_currency: [recalculate_imprest],
        request_currency: [recalculate_imprest],
    },
}

// ORIGINAL
// export const imprest_retirement = {
//     // custom_validation: [validate_imprest],
//     on_field_change: {
//         amount: [recalculate_imprest_retirement],
//         debit_account: [recalculate_imprest_retirement],
//         credit_account: [recalculate_imprest_retirement],
//         debit_account_currency: [recalculate_imprest_retirement],
//         credit_account_currency: [recalculate_imprest_retirement],
//         imprest: [recalculate_imprest_retirement],
//         currency: [recalculate_imprest_retirement],
//     },
// }
export const imprest_retirement = {
    // custom_validation: [validate_imprest],
    on_field_change: {
        imprest: [popluate_imprest_data],
        usage_length: [recalculate_imprest_retirement_expenses],
        unit_price_of_usage: [recalculate_imprest_retirement_expenses],
        // total_spent: [recalculate_imprest_retirement_expenses]
    },
}

export const staff_advance = {
    on_load: [prepopulated_behavioral_imperatives],
    on_field_change: {
        employee_id: [appraise_your_self],
        rating_po: [rate_performance_obj],
        rating_b: [rate_behavior],
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

export const separation = {
    on_field_change: {
        resignation_date: [seperation_notice_period],
        last_day_of_work: [seperation_notice_period],
    }
}