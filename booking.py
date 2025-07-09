import pandas as pd
from datetime import datetime
from pandas.tseries.offsets import MonthEnd

data = pd.read_csv(r"booking apartment.csv")

#ganti data type supaya perbedaan hari bisa diitung
data['start_date'] = pd.to_datetime(data['start_date'])
data['end_date'] = pd.to_datetime(data['end_date'])

def split_rows_by_month(data):
    expanded_rows = []

    for _, row in data.iterrows():
        start = row['start_date']
        end = row['end_date']
        current_start = start

        while current_start <= end:
            # Get end of the current month or actual end date
            current_end = min(end, current_start + MonthEnd(0))
            expanded_rows.append({
                'apartment_id': row['apartment_id'],
                'room_id': row['room_id'],
                'user_id': row['user_id'],
                'start_date': current_start,
                'end_date': current_end
            })
            current_start = current_end + pd.Timedelta(days=1)

    return pd.DataFrame(expanded_rows)

data = split_rows_by_month(data)

data['month'] = data['start_date'].dt.month
print(data)
# data_type = data.dtypes
# print(data_type)

#cari tau berapa hari dia dibooking
data['day_booked'] = (data['end_date'] - data['start_date']).dt.days + 1
print("hai",data)
grouped = data.groupby(['apartment_id', 'room_id', 'month'])['day_booked'].sum().reset_index()

grouped['occupancy_rate'] = grouped['day_booked']/30
print("grouped",grouped.sort_values(['month','apartment_id','room_id']))
final_occupancy_rate = grouped.groupby(['apartment_id','month'])['occupancy_rate'].mean().reset_index()
print(final_occupancy_rate)