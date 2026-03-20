import pandas as pd
from datetime import datetime
from controllers.utils import Utils
from .utils import natural_list_dicts

utils = Utils () 

class Stock_Analytics:
    def __init__(self, dbms, object=None, privilege=None) -> None:
        self.dbms = dbms
        self.object = object

    def analyze_stock_valuation (self, entries):
        df = utils.to_data_frame (entries)
        df['posting_date'] = pd.to_datetime(df['posting_date'])
        df['year_month'] = df['posting_date'].dt.to_period('M').astype(str)
        df['year_month'] = df['posting_date'].dt.strftime('%B %Y')

        grouped = df.groupby(['year_month', 'warehouse', 'item_name']).apply(lambda x: x.to_dict(orient='records'))
        result = {}
        for (year_month, warehouse, item_name), records in grouped.items():
            if year_month not in result:
                result[year_month] = {}
            if warehouse not in result[year_month]:
                result[year_month][warehouse] = {}
            result[year_month][warehouse][item_name] = records

        return result

    def to_numeric (self, data):
        data['incoming_rate'] = pd.to_numeric(data['incoming_rate'])
        data['incoming_value'] = pd.to_numeric(data['incoming_value'])
        data['in_qty'] = pd.to_numeric(data['in_qty'])
        data['out_value'] = pd.to_numeric(data['out_value'])
        data['out_qty'] = pd.to_numeric(data['out_qty'])
        data['current_value'] = pd.to_numeric(data['current_value'])
        data['current_qty'] = pd.to_numeric(data['current_qty'])
        data['remaining_qty'] = pd.to_numeric(data['remaining_qty'])
        data['remaining_value'] = pd.to_numeric(data['remaining_value'])
        return data
    
    def split_dict (self, data_frame) -> dict:
        restocking_df = data_frame[data_frame['status'].isin(['Purchased', 'Depleting', 'Transfer In'])]
        sold_df = data_frame[data_frame['status'].isin(['Sold', 'Transferred'])]   
        return {
            "restocking_df": restocking_df,
            "sold_df": sold_df
        }
    
    def aggregate_by (self, by:str, data_frame):
        return data_frame.groupby (by).agg (
            incoming_value = ('incoming_value', 'sum'),
            in_qty = ('in_qty', 'sum'),
            current_value = ('current_value', 'sum'),
            current_qty = ('current_qty', 'sum'),
            out_value = ('out_value', 'sum'),
            out_qty = ('out_qty', 'sum'),
            remaining_value = ('remaining_value', 'sum'),
            remaining_qty = ('remaining_qty', 'sum')
        )
    
    def item_trends (self, data):
        df = utils.to_data_frame(data)
        df['created_on'] = pd.to_datetime(df['created_on'])
        current_date = datetime.now()
        start_of_year = datetime(current_date.year, 1, 1)
        ytd_selling_df = df[(df['entry_type'] == 'Selling') & (df['created_on'] >= start_of_year)]
        sales_trends = ytd_selling_df.groupby(['item_code', 'item_name']).agg(
            total_sold=('out_qty', 'sum'),
            transactions_count=('id', 'count')
        ).reset_index()
        top_trending_items = sales_trends.sort_values(by='total_sold', ascending=False).head(6)
        return top_trending_items.to_dict(orient="records")

    def item (self, data: list, add_overall_totals: bool = False):
        return_dict = {}
        if data:
            data_frame = utils.to_data_frame (data)
            data_frame = self.to_numeric (data_frame)
            splitted_data_frames = self.split_dict (data_frame)
            grouped_restocking = self.aggregate_by("item_name", splitted_data_frames['restocking_df'])

            grouped_sold = self.aggregate_by("item_name", splitted_data_frames['sold_df'])
            
            sold_df = utils.to_data_frame (grouped_sold.to_dict (orient='index')).T
            restocking_df = utils.to_data_frame (grouped_restocking.to_dict (orient='index')).T

            merged_df = pd.merge (sold_df, restocking_df, left_index=True, right_index=True, suffixes=('_sold', '_restock'))
            
            return_dict['items'] = natural_list_dicts (merged_df.to_dict (orient='index'))
            if add_overall_totals:
                return_dict['overall_totals'] = {
                    "unit_cost": grouped_restocking['unit_price'],
                    "total_in_qty": grouped_restocking['in_qty'].sum (),
                    "total_incoming_value": grouped_restocking['incoming_value'].sum (),
                    "total_out_value": grouped_sold['out_value'].sum (),
                    "total_out_qty": grouped_sold['out_qty'].sum (),
                    "total_current_qty": grouped_restocking['in_qty'].sum () - grouped_sold['out_qty'].sum (),
                    "total_current_value": grouped_restocking['incoming_value'].sum () - grouped_sold['out_value'].sum (),
                }
        
        return utils.respond (utils.ok, return_dict)

    def analyze (self, data: list, groupby: str, add_overall_totals: bool = False):
        return_dict = {}
        if data:
            data_frame = utils.to_data_frame (data)
            data_frame = self.to_numeric (data_frame)
            splitted_data_frames = self.split_dict (data_frame)
            grouped_restocking = self.aggregate_by(groupby, splitted_data_frames['restocking_df'])
            grouped_sold = self.aggregate_by(groupby, splitted_data_frames['sold_df'])
            sold_df = utils.to_data_frame (grouped_sold.to_dict (orient='index')).T
            restocking_df = utils.to_data_frame (grouped_restocking.to_dict (orient='index')).T
            merged_df = pd.merge (sold_df, restocking_df, left_index=True, right_index=True, suffixes=('_sold', '_restock'))
            return_dict['items'] = natural_list_dicts (merged_df.to_dict (orient='index'))

            if add_overall_totals:
                return_dict['overall_totals'] = {
                    "total_in_qty": grouped_restocking['in_qty'].sum (),
                    "total_incoming_value": grouped_restocking['incoming_value'].sum (),
                    "total_out_value": grouped_sold['out_value'].sum (),
                    "total_out_qty": grouped_sold['out_qty'].sum (),
                    "total_current_qty": grouped_restocking['in_qty'].sum () - grouped_sold['out_qty'].sum (),
                    "total_current_value": grouped_restocking['incoming_value'].sum () - grouped_sold['out_value'].sum (),
                }
        return utils.respond (utils.ok, return_dict)

    def stock_aging (self, data):
        df = utils.to_data_frame (data)
        df['posting_date'] = pd.to_datetime(df['posting_date'])
        current_date = datetime.now()
        df['age_days'] = (current_date - df['posting_date']).dt.days
        average_age_by_item = df.groupby('item_name')['age_days'].mean().reset_index()
        average_age_by_item = average_age_by_item.to_dict (orient='records')
        df = utils.to_data_frame (average_age_by_item)
        df_sorted = df.sort_values(by='age_days', ascending=False)
        return df_sorted.head(9).to_dict (orient='records')


    def warehouse (self, data: list):
        data_frame = utils.to_data_frame  (data)
        data_frame = self.to_numeric (data_frame)
        splitted_data_frames = self.split_dict (data_frame) 

    def item_info (self, data):
        df = utils.to_data_frame (data=data)
        restock_df = df[df['entry_type'] == 'Restocking']
        sale_df = df[df['entry_type'] == 'Selling']

        sum_out_qty_sale = sale_df['out_qty'].sum()
        sum_in_qty_restock = restock_df['in_qty'].sum()
        sum_current_qty_restock = restock_df['current_qty'].sum()
        difference = sum_in_qty_restock - sum_out_qty_sale
        return utils.from_dict_to_object ({
            "out_qty": sum_out_qty_sale,
            "in_qty": sum_in_qty_restock,
            "available_qty": sum_current_qty_restock,
            "current_qty": difference
        })
        

    def aggregate_stock_data(self, stock_list):
        df = utils.to_data_frame (stock_list)
        grouped = df.groupby('item_name')
        sold_stock = {}
        restock = {}
        def is_sold(status):
            return status in ['Transferred', 'Sold']
        def is_restock(status):
            return status in ['Transfer In', 'Purchased', 'Depleting']
        
        for name, group in grouped:
            sold_stock[name] = group[group['status'].apply(is_sold)]
            restock[name] = group[group['status'].apply(is_restock)]
        def calculate_aggregates(data, type_of_calc):
            if type_of_calc == "sold":
                return {
                    'total_qty': data['out_qty'].sum(),
                    'total_value': data['out_value'].sum(),
                }
            else:
                return  {
                    'total_qty': data['remaining_qty'].sum(),
                    'total_value': data['remaining_value'].sum(),
                }
        
        sold_stock_aggregate = {name: calculate_aggregates(group, "sold") for name, group in sold_stock.items()}
        restock_aggregate = {name: calculate_aggregates(group, "restock") for name, group in restock.items()}
        current_stock = {}
        for name in sold_stock_aggregate.keys():
            current_qty = restock_aggregate[name]['total_qty'] - sold_stock_aggregate[name]['total_qty']
            current_value = restock_aggregate[name]['total_value'] - sold_stock_aggregate[name]['total_value']

            current_qty = max(current_qty, 0)
            current_value = max(current_value, 0)

            current_stock[name] = {
                'current_qty': current_qty,
                'current_value': current_value,
            }
        
        return utils.from_dict_to_object({
            'sold_stock': sold_stock_aggregate,
            'restock': restock_aggregate,
            'current_stock': current_stock,
        })

    def price_list (self, data):
        df = utils.to_data_frame (data)
        grouped = df.groupby (['warehouse', 'item_name'])
        grouped = grouped.agg({
            'item_code': 'first',
            'incoming_rate': 'first',
            'current_qty': 'sum',
        }).reset_index()
        result = grouped.to_dict(orient='records')
        return result
