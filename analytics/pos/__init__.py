import pandas as pd # type: ignore
from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.utils.dict_to_object import Dict_To_Object

utils = Utils ()
dates = Dates ()
pp = utils.pretty_print
throw = utils.throw

class POS_Analysis:
    def __init__(self,dbms,object=None):
        self.dbms = dbms
        self.object = object

    def get_sales_data_metrics(self, data):
        if not isinstance(data, list) or len(data) == 0:
            return {}
        
        total_qty = 0
        for item in data:
            total_qty += int(item['total_qty'])

        df = utils.to_data_frame(data)
        
        df['base_total_discount_amount'] = df['base_total_discount_amount'].astype(float)
        df['base_total_taxes_amount'] = df['base_total_taxes_amount'].astype(float)
        df['base_tax_exclusive_total_amount'] = df['base_tax_exclusive_total_amount'].astype(float)
        df['base_inclusive_total_amount'] = df['base_inclusive_total_amount'].astype(float)

        data = {
            'total_sales': len(df),
            'total_quantity': total_qty,
            'total_discount_amount': df['base_total_discount_amount'].sum(),
            'total_tax_amount': df['base_total_taxes_amount'].sum(),
            'total_exclusive_amount': df['base_tax_exclusive_total_amount'].sum(),
            'total_inclusive_amount': df['base_inclusive_total_amount'].sum(),
        }
        return data

    def cashier_metrics(self,data):
        if not isinstance(data, list) or len(data) == 0:
            return {}
        
        df = utils.to_data_frame(data)
        total = len(df)
        sale_points = df['sale_point'].dropna().unique()
        sale_point_metrics = []
        for s in sale_points:
            sale_point_metrics.append({"sale_point": s, "total": len(df[df['sale_point'] == s])})

        return {
            "total": total,
            "sale_point_metrics": sale_point_metrics
        }
    
    def filtered_metrics(self, name, df):
        total_till_records = len(df)
        total_starting_float = df['starting_float'].sum()
        total_quantity_sold = df['total_quantity_sold'].sum()
        total_amount_sold = df['total_amount_sold'].sum()
        total_amount_sold_by_customer = df['total_amount_sold_by_customer'].sum()
        total_amount_sold_by_walkin = df['total_amount_sold_by_walkin'].sum()

        average_starting_float = df['starting_float'].mean(skipna=True)
        average_quantity_sold = df['total_quantity_sold'].mean(skipna=True)
        average_amount_sold = df['total_amount_sold'].mean(skipna=True)
        average_amount_sold_by_customer = df['total_amount_sold_by_customer'].mean(skipna=True)
        average_amount_sold_by_walkin = df['total_amount_sold_by_walkin'].mean(skipna=True)

        return {
            "name": name,
            "total_records": total_till_records,
            "total_starting_float": total_starting_float,
            "average_starting_float": average_starting_float,
            "total_amount_sold": total_amount_sold,
            "total_amount_sold_by_customer": total_amount_sold_by_customer,
            "total_amount_sold_by_walkin": total_amount_sold_by_walkin,
            "average_amount_sold_by_customer": average_amount_sold_by_customer,
            "average_amount_sold_by_walkin": average_amount_sold_by_walkin,
            "average_amount_sold": average_amount_sold,
            "total_quantity_sold": int(total_quantity_sold) if isinstance(total_quantity_sold, int) or isinstance(total_amount_sold, float) else 0,
            "average_quantity_sold": int(average_quantity_sold) if isinstance(average_quantity_sold, int) or isinstance(average_amount_sold, float) else 0,
        }
    
    def till_record_metrics(self, data: list = [], get_cashier_metrics: bool = True, get_sale_point_metrics: bool = True):
        if not isinstance(data, list) or len(data) == 0:
            return {}

        df = utils.to_data_frame(data)

        df['starting_float'] = df['starting_float'].fillna(0).astype(float)
        df['total_amount_sold'] = df['total_amount_sold'].fillna(0)

        df['total_quantity_sold'] = pd.to_numeric(df['total_quantity_sold'], errors='coerce').fillna(0).astype(int)

        df['sale_point'] = df['sale_point'].fillna('Unknown')
        df['cashier'] = df['cashier'].fillna('Unknown')

        total_till_records = len(df)
        total_starting_float = df['starting_float'].sum()
        total_quantity_sold = df['total_quantity_sold'].sum()
        total_amount_sold = df['total_amount_sold'].sum()
        total_amount_sold_by_customer = df['total_amount_sold_by_customer'].sum()
        total_amount_sold_by_walkin = df['total_amount_sold_by_walkin'].sum()

        average_starting_float = df['starting_float'].mean(skipna=True)
        average_quantity_sold = df['total_quantity_sold'].mean(skipna=True)
        average_amount_sold = df['total_amount_sold'].mean(skipna=True)
        average_amount_sold_by_customer = df['total_amount_sold_by_customer'].mean(skipna=True)
        average_amount_sold_by_walkin = df['total_amount_sold_by_walkin'].mean(skipna=True)

        total_sale_points = df['sale_point'].nunique()
        total_cashiers = df['cashier'].nunique()

        # till_metrics = []
        # till_list = []
        # if get_till_metrics == True:
        #     till_list = df['till'].unique()
        #     for t in till_list:
        #         till_metrics.append(self.filtered_metrics(t, df[df['till'] == t]))

        cashier_metrics = []
        cashier_list = []
        if get_cashier_metrics == True:
            cashier_list = df['cashier'].unique()
            for c in cashier_list:
                cashier_metrics.append(self.filtered_metrics(c, df[df['cashier'] == c]))

        sale_point_metrics = []
        sale_point_list = []
        if get_sale_point_metrics == True:
            sale_point_list = df['sale_point'].unique()
            for s in sale_point_list:
                sale_point_metrics.append(self.filtered_metrics(s, df[df['sale_point'] == s]))

        return {
            "total_records": total_till_records,
            "total_starting_float": total_starting_float,
            "average_starting_float": average_starting_float,
            "total_amount_sold": total_amount_sold,
            "total_amount_sold_by_customer": total_amount_sold_by_customer,
            "total_amount_sold_by_walkin": total_amount_sold_by_walkin,
            "average_amount_sold_by_customer": average_amount_sold_by_customer,
            "average_amount_sold_by_walkin": average_amount_sold_by_walkin,
            "average_amount_sold": average_amount_sold,
            "total_quantity_sold": int(total_quantity_sold) if isinstance(total_quantity_sold, int) or isinstance(total_amount_sold, float) else 0,
            "average_quantity_sold": int(average_quantity_sold) if isinstance(average_quantity_sold, int) or isinstance(average_amount_sold, float) else 0,
            "total_sale_points": total_sale_points,
            "sale_points": sale_point_list,
            "total_cashiers": total_cashiers,
            "cashiers": cashier_list,
            "cashier_metrics": cashier_metrics,
            "sale_point_metrics": sale_point_metrics,
            # "tills": till_list,
            # "till_metrics": till_metrics,
        }
    
    def get_payment_metrics(self, data):
        if not isinstance(data, list) or len(data) == 0:
            return {}
            
        df = utils.to_data_frame(data)

        cols = ['mobile_money', 'cash', 'card']
        for col in cols:
            if col not in df.columns:
                df[col] = 0
            df[col] = df[col].fillna(0).astype(float)

        metrics = {}
        for col in cols:
            metrics.update({col : df[col].sum()})
            metrics.update({f"average_{col}" : df[col].mean()})
        return metrics
    
    def closing_entries_metrics(self, data):
        if not isinstance(data, list) or len(data) == 0:
            return {}

        df = utils.to_data_frame(data)

        df['total_walkin_amount_sold'] = df['total_walkin_amount_sold'].fillna(0).astype(float)
        df['total_customer_amount_sold'] = df['total_customer_amount_sold'].fillna(0).astype(float)

        # df['total_qty_sold'] = pd.to_numeric(df['total_qty_sold'], errors='coerce').fillna(0).astype(int)

        total_closings = len(df)
        total_walkin_amount_sold = df['total_walkin_amount_sold'].sum()
        total_customer_amount_sold = df['total_customer_amount_sold'].sum()
        # total_qty_sold = df['total_qty_sold'].sum()

        return {
            "total_closings": total_closings,
            "total_walkin_amount_sold": total_walkin_amount_sold,
            "total_customer_amount_sold": total_customer_amount_sold,
            # "total_qty_sold": total_qty_sold,
        }
    
    def cash_logs_metrics(self, data):
        if not isinstance(data, list) or len(data) == 0:
            return {}
        
        df = utils.to_data_frame(data)

        total_logs = len(df)
        total_closed = len(df[df['closed_at'] != None])
        total_users = df['user'].nunique()
        total_sale_points = df['sale_point'].nunique()

        users = df['user'].unique()
        sale_points = df['sale_point'].unique()
        
        df['cash_on_hand'] = df['cash_on_hand'].fillna(0).astype(float)

        user_metrics = []
        sale_point_metrics = []

        for user in users:
            df_user = df[df['user'] == user]
            total_cash_on_hand = df_user['cash_on_hand'].sum()
            user_metrics.append({
                "user": user,
                "total_cash_on_hand": total_cash_on_hand
            })

        for sale_point in sale_points:
            df_sale_point = df[df['sale_point'] == sale_point]
            total_cash_on_hand = df_sale_point['cash_on_hand'].sum()
            sale_point_metrics.append({
                "sale_point": sale_point,
                "total_cash_on_hand": total_cash_on_hand
            })

        return {
            "total_logs": total_logs,
            "total_closed": total_closed,
            "total_users": total_users,
            "total_sale_points": total_sale_points,
            "user_metrics": user_metrics,
            "sale_point_metrics": sale_point_metrics
        }
    
    def get_item_metrics(self, items):
        df = utils.to_data_frame(items)

        cols = ['discount_amount', 'discounted_amount', 'exclusive', 'inclusive', 'tax_amount', 'xclusive', 'qty']
        totals = {}
        
        for col in df.columns:
            if col in cols:
                df[col] = df.get(col).fillna(0).astype(float)
                total = df.get(col).sum()
                totals.update({col: total})
        return totals

    def generate_aggregated_totals(self, data: list = [], key: str = None):
        if not isinstance(data, list) or len(data) == 0:
            return {}
        
        item_sales_data = []
        for sales_data in data:
            if 'line_items' in sales_data and isinstance(sales_data['line_items'], list) and sales_data['customer'] == key:
                item_sales_data.extend(sales_data['line_items'])

        line_items = []

        if len(item_sales_data) > 0:
            group_by_item_name = utils.group(item_sales_data, "item_name")
            for item_name, items in group_by_item_name.items():
                item_metric = self.get_item_metrics(items)
                item_metric['qty'] = int(item_metric['qty'])
                item_metric.update({"item_name": item_name, "item_code": item_name, "item_type": items[0].item_type})
                line_items.append(item_metric)

        cols = ["total_discount_amount", "total_outstanding_amount", "total_paid_amount", "total_taxes_amount", "total_qty", "sub_total_amount", "tax_exclusive_total_amount", "base_inclusive_total_amount", "base_sub_total_amount", "base_tax_exclusive_total_amount", "base_total_discount_amount", "base_total_outstanding_amount", "base_total_paid_amount", "base_total_taxes_amount","inclusive_total_amount"]

        df = utils.to_data_frame(data)
        df = df[df['customer'] == key]

        totals = {}

        for col in df.columns:
            if col in cols:
                df[col] = df.get(col).fillna(0).astype(float)
                total = df.get(col).sum()
                totals.update({col: total})

        totals.update({"line_items": line_items})
        return totals
    
    def aggregate_sales_entries(self, data):
        if not isinstance(data, list) or len(data) == 0:
            return {}
        
        aggregated_sales = {}
        for sales_log in data:
            for item, sales_data in sales_log.items():
                if item in aggregated_sales:
                    aggregated_sales[item]['quantity_sold'] += sales_data['quantity_sold']
                    aggregated_sales[item]['total_revenue'] += sales_data['quantity_sold'] * sales_data['unit_price']
                else:
                    aggregated_sales[item] = {
                        'unit_price': sales_data['unit_price'],
                        'quantity_sold': sales_data['quantity_sold'],
                        'total_revenue': sales_data['quantity_sold'] * sales_data['unit_price']
                    }

        return aggregated_sales