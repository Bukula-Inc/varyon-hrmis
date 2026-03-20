import pandas as pd
from collections import defaultdict
from controllers.utils import Utils
from controllers.utils.dates import Dates


utils = Utils ()
dates = Dates ()
tdf = utils.to_data_frame
class Report_Analytics:
    def __init__(self, dbms, object=None, privilege=None) -> None:
        self.dbms = dbms
        self.object = object

    def summarize_stock_entries(self, stock_entries):
        df = tdf (stock_entries)
        required_columns = {"warehouse", "item_name", "in_qty", "out_qty", "current_qty"}
        if not required_columns.issubset(df.columns):
            raise ValueError(f"Missing required columns. Expected: {required_columns}")
        grouped = df.groupby(["warehouse", "item_name"]).agg(
            in_qty=("in_qty", "sum"),
            out_qty=("out_qty", "sum"),
            current_qty=("current_qty", "sum")
        ).reset_index()

        summary = defaultdict(lambda: defaultdict(lambda: {"in_qty": 0, "out_qty": 0, "current_qty": 0}))
        for _, row in grouped.iterrows():
            warehouse = row["warehouse"]
            item_name = row["item_name"]
            summary[warehouse][item_name]["in_qty"] = row["in_qty"]
            summary[warehouse][item_name]["out_qty"] = row["out_qty"]
            summary[warehouse][item_name]["current_qty"] = row["current_qty"]

        return summary


    def groupby_date_range (self, data, start_date, end_date):
        df = tdf (data)
        df['posting_date'] = pd.to_datetime(df['posting_date'])
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        less_than_start = df[df['posting_date'] < start_date].to_dict(orient='records')
        between_start_and_end = df[(df['posting_date'] >= start_date) &
                                (df['posting_date'] <= end_date)].to_dict(orient='records')
        only_start_date = df[(df['posting_date'] >= start_date)]
        return less_than_start, between_start_and_end, only_start_date

    def fnd_date_closing (self, entries, start_date):
        st = self.groupby_date_range (entries, start_date=start_date, end_date=dates.today ())
        val = 0.00
        blc = 0.00
        if st[0]:
            stc = self.stock_balance (st[0])
            for item in stc:
                val += float (item.get ("stock_value", 0))
                blc += float (item.get ("stock_balance", 0))
        return blc, val

    def stock_balance (self, entries):
        df = tdf (entries)
        grouped = df.groupby('item_name').agg({
            'item_code': 'first',
            'warehouse': 'first',
            'out_qty': 'sum',
            'in_qty': 'sum',
            'out_value': 'sum',
            'current_qty': 'sum',
            'current_value': 'sum',
            'incoming_value': 'sum',
        }).reset_index()

        grouped.rename(columns={
            'item_code': 'item_code',
            'warehouse': 'warehouse',
            'in_qty': 'in_qty',
            'out_qty': 'sold_qty',
            'out_value': 'sold_value',
            'current_qty': 'stock_balance',
            'current_value': 'stock_value',
            'incoming_value': 'in_value',
        }, inplace=True)

        result = grouped.to_dict(orient='records')
        return result

    def stock_turnover (self, entries):
        df = tdf (entries)
        grouped = df.groupby('item_name').agg({
            'item_code': 'first',
            'in_qty': 'sum',
            'incoming_value': 'sum',
            'out_qty': 'sum',
            'out_value': 'sum',
            'current_qty': 'sum',
            'current_value': 'sum',
        }).reset_index()

        grouped.rename(columns={
            'item_code': 'item_code',
            'in_qty': 'in_qty',
            'incoming_value': 'in_value',
            'out_qty': 'out_qty',
            'out_value': 'out_value',
            'current_qty': 'current_qty',
            'current_value': 'current_value',
        }, inplace=True)

        result = grouped.to_dict(orient='records')
        return result

    def stock_summary (self, entries):
        df = tdf (entries)
        grouped = df.groupby('item_name').agg({
            'item_code': 'first',
            'out_qty': 'sum',
            'out_value': 'sum',
            'current_qty': 'sum',
            'current_value': 'sum',
        }).reset_index()

        grouped.rename(columns={
            'item_code': 'item_code',
            'out_qty': 'sold_qty',
            'out_value': 'sold_value',
            'current_qty': 'available_quantity',
            'current_value': 'total_value',
        }, inplace=True)

        result = grouped.to_dict(orient='records')
        return result

    def stock_movement (self, entires):
        df = tdf (entires)
        numeric_columns = ['in_qty', 'out_qty', 'out_value', 'current_qty', 'current_value', 'remaining_qty', 'incoming_value', 'remaining_value']
        for column in numeric_columns:
            df[column] = pd.to_numeric(df[column], errors='coerce')
        grouped = df.groupby (['item_name', 'reference_type', 'reference', 'transaction_type']).agg ({
            'item_code': 'first',
            'in_qty': 'sum',
            'out_qty': 'sum',
            'out_value': 'sum',
            'current_qty': 'sum',
            'current_value': 'sum',
            'remaining_qty': 'sum',
            'incoming_value': 'sum',
            'remaining_value': 'sum',
        }).reset_index()

        result = grouped.to_dict(orient='records')
        return result
