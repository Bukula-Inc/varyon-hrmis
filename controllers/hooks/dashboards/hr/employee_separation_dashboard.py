import pandas as pd
import numpy as np
from controllers.utils import Utils
from controllers.utils.dates import Dates
from datetime import datetime, date
import calendar

utils =Utils()
dates =Dates()
pp =utils.pretty_print
throw =utils.throw



def employee_separation_dashboard(dbms, object):
    return_data =utils.from_dict_to_object({})
    emp_under_disciplinary = []
    emp_settlement = []
    separation_trends = utils.from_dict_to_object({})
    recent_separation_applications = []
    fetch_disciplinary =None
    fetch_separation =None
    fetch_disciplinary =None
    fetch_final_statement =None
    try:
        fetch_disciplinary =dbms.get_list("Employee_Disciplinary", fetch_linked_fields=True, fetch_linked_tables=True)
        fetch_separation =dbms.get_list("Employee_Seperation", fetch_linked_fields=True, fetch_linked_tables=True)
        fetch_final_statement =dbms.get_list("Final_Statement", fetch_linked_fields=True, fetch_linked_tables=True)
        # fetch_separation =dbms.get_list("employee_separation", filters= {"__range"}, fetch_linked_fields=True, fetch_linked_tables=True)
        # fetch_disciplinary =dbms.get_list("Employee_Disciplinary", fetch_linked_fields=True, fetch_linked_tables=True)
        # fetch_disciplinary =dbms.get_list("Employee_Disciplinary", fetch_linked_fields=True, fetch_linked_tables=True)
        # fetch_disciplinary =dbms.get_list("Employee_Disciplinary", fetch_linked_fields=True, fetch_linked_tables=True)
    except Exception as e:
        pp(f"An Error Occured: {e}")

    if fetch_disciplinary.status ==utils.ok:
        for disciplinary in fetch_disciplinary.data.rows:
            emp =disciplinary.linked_fields.subject
            emp_under_disciplinary.append(utils.from_dict_to_object({
                "image": "",
                "emp_name": emp.full_name,
                "action_taken": emp.status,
            }))
        return_data.emp_under_disciplinary =emp_under_disciplinary

    # SETTLEMENT RATINGS    

    if fetch_final_statement.status ==utils.ok:

        # Step 1: Convert the object into a DataFrame
        final_statement_df = utils.to_data_frame(fetch_final_statement.data.rows)

        # Step 2: Convert columns to numeric before using fillna
        final_statement_df['total_payable'] = pd.to_numeric(final_statement_df['total_payable'], errors='coerce').fillna(0)
        final_statement_df['total_asset'] = pd.to_numeric(final_statement_df['total_asset'], errors='coerce').fillna(0)
        final_statement_df['leave_days'] = pd.to_numeric(final_statement_df['leave_days'], errors='coerce').fillna(0)
        final_statement_df['redundancy'] = pd.to_numeric(final_statement_df['redundancy'], errors='coerce').fillna(0)
        final_statement_df['gratuity'] = pd.to_numeric(final_statement_df['gratuity'], errors='coerce').fillna(0)

        # Step 3: Summing the relevant columns
        totals = final_statement_df[['total_payable', 'total_asset', 'leave_days', 'redundancy', 'gratuity']].sum()

        # Step 4: Convert 'created_on' to datetime and calculate the rate of records over time
        final_statement_df['created_on'] = pd.to_datetime(final_statement_df['created_on'])

        # Calculate time difference from the earliest record (if you have multiple records, this makes sense)
        time_span = (final_statement_df['created_on'].max() - final_statement_df['created_on'].min()).days if len(final_statement_df) > 1 else 1  # Avoid division by zero

        # Calculate rate of records per day
        rate_of_records = len(final_statement_df) / time_span

        # Step 5: Prepare the final result as a dictionary
        final_dict = {
            "total_payable": totals['total_payable'],
            "total_asset": totals['total_asset'],
            "leave_days": totals['leave_days'],
            "redundancy": totals['redundancy'],
            "gratuity": totals['gratuity'],
            "rate_of_records_per_day": rate_of_records
        }

        final_dict_vals =utils.from_dict_to_object(final_dict)

        emp_settlement.append(utils.from_dict_to_object({
            "rate": final_dict_vals.rate_of_records_per_day or 00,
            "amount_pending": final_dict_vals.total_payable or 00,
            "amount_con": final_dict_vals.redundancy or 00,
            "overall_rate": final_dict_vals.rate_of_records_per_day *5 or 0.00,
            "leave_value_paid": final_dict_vals.leave_days or 00,
            "gratuity_value_paid": final_dict_vals.gratuity or 00,
        }))
        
        return_data.emp_settlement =emp_settlement[0]


    # DEPARTMENTAL MUTLI LINE GRAPH
    if fetch_separation.status ==utils.ok:
        separation_df =utils.to_data_frame(fetch_separation.data.rows)

        departmental =utils.group(fetch_separation.data.rows, "department")
        male =0
        female =0
        gender =utils.from_dict_to_object({
            "labels": ["male", "female"],
            "value": [],
        })

        for separation in fetch_separation.data.rows:
            # GENDER
            if separation.linked_fields.employee.gender =="Female":
                female +=1
            else:
                male +=1
 
        gender.value.append(male)
        gender.value.append(female)
        separation_trends.gender =gender

        return_data.separation_trends =separation_trends

        # SEPARATION

        separation_df["created_on"] = pd.to_datetime(separation_df["created_on"])

        # Define date range
        today = pd.Timestamp.today()
        three_months_ago = today - pd.DateOffset(months=3)

        # Filter using Pandas (vectorized operation, no explicit loop)
        filtered_df = separation_df[(separation_df["created_on"] >= three_months_ago) & (separation_df["created_on"] <= today)]

        # Convert back to list of dictionaries if needed
        filtered_data = filtered_df.to_dict(orient="records")
        for recent_separation in filtered_data:
            recent_separation_applications.append(utils.from_dict_to_object({
                "name": recent_separation["employee_name"],
                "status": recent_separation["status"],
                "date_of_application": recent_separation["created_on"],
            }))
        return_data.recent_separations =recent_separation_applications  

    # MONTHLY DISTRIBUTION
    mon_sep_data =utils.from_dict_to_object({
        "lebals":[],
        "values": []
    })

    mon_values_source =utils.from_dict_to_object({})
    month_names = [calendar.month_name[m] for m in range(1,datetime.now().month)]
    today = datetime.today()

    # Define start of the year (January 1st of current year)
    start_of_year = date(today.year, 1, 1)

    # Define end date (Last day of current month)
    # end_of_range = date(today.year, today.month, )
    end_of_range = date(today.year, 4, 1)

    current_month = datetime.now().month

    # last_day_of_work
    filtered_data = [
        item for item in fetch_separation.data.rows
        if start_of_year <= item.last_day_of_work <= end_of_range
    ]
    
    if len(filtered_data) >0:
        separation_types_list =utils.group(filtered_data, "separation_type")

# Convert the list of dictionaries to a pandas DataFrame
        separation_df = utils.to_data_frame(filtered_data)

        # Count the occurrences of each separation type in each department
        count_df = separation_df.groupby(['separation_type', 'department']).size().reset_index(name='count')

        # Pivot the table to get separation types as rows and departments as columns
        pivot_df = count_df.pivot(index='separation_type', columns='department', values='count').fillna(0)

        # Convert the pivoted DataFrame into the desired format
        departmental_result = {
            'values': [{'name': separation_type, 'data': pivot_df.loc[separation_type].tolist()} for separation_type in pivot_df.index],
            'labels': pivot_df.columns.tolist()
        }
        separation_trends.departmental =departmental_result

    # Convert the list of dictionaries to a pandas DataFrame
        monthly_separation_df = utils.to_data_frame(filtered_data)

        # Convert resignation_date to datetime and extract the month name
        monthly_separation_df['resignation_date'] = pd.to_datetime(monthly_separation_df['resignation_date'])
        monthly_separation_df['month'] = monthly_separation_df['resignation_date'].dt.strftime('%b')  # Get month name (Jan, Feb, etc.)

        # Count the occurrences of each separation type in each month
        count_df = monthly_separation_df.groupby(['separation_type', 'month']).size().reset_index(name='count')

        # Pivot the table to get separation types as rows and months as columns
        pivot_df = count_df.pivot(index='separation_type', columns='month', values='count').fillna(0)

    # Convert the pivoted DataFrame into the desired format
    # monthly_result = {
    #     'values': [{'name': separation_type, 'data': pivot_df.loc[separation_type].tolist()} for separation_type in pivot_df.index],
    #     'labels': pivot_df.columns.tolist()
    # }
    # separation_trends.monthly =monthly_result
    

    return utils.respond(utils.ok, return_data)