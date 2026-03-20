export const payroll_processor = async () => {
    try{
        const payroll_processor = await import(`../../form/payroll/index.js`)
        if(payroll_processor){
            return { ...payroll_processor?.payroll_processor } || {}
        }
        return {}
    }
    catch{
        console.error(`Failed`)
        return {}
    }
}
export const calculate_payroll = async () => {
    try{
        const re_calc = await import(`../../form/payroll/core.js`)
        if(re_calc){
            return re_calc.calculate_payroll || null
        }
        return null
    }
    catch{
        console.error(`Failed`)
        return null
    }
}