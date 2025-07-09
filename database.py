import mysql.connector
from booking import transforming
import pymysql
import pandas as pd

conn =  pymysql.connect( 
    host="localhost",
    user="root",
    password="1234",
    database="database"
)

#membuat table
cursor = conn.cursor()
create_table = """
CREATE TABLE IF NOT EXISTS booking_apartment(
    apartment_id varchar(10),
    room_id varchar(10),
    user_id varchar(10),
    start_date date,
    end_date date
);
"""

create_table_hasil = """
CREATE TABLE IF NOT EXISTS occupancy_apartment(
    apartment_id varchar(10),
    month char(2),
    occupancy_rate float(10,5)
);
"""

cursor.execute(create_table)
cursor.execute(create_table_hasil)
conn.commit()

data_awal, final_occupancy_rate = transforming()

# print("database", data_awal)
insert_data_awal = "INSERT INTO booking_apartment(apartment_id,room_id,user_id,start_date,end_date) VALUES(%s,%s,%s,%s,%s);"
insert_final_occupancy = "INSERT INTO occupancy_apartment(apartment_id,month,occupancy_rate) VALUES(%s,%s,%s);"

for _, r in data_awal.iterrows():
    cursor.execute(insert_data_awal, (
        r['apartment_id'], r['room_id'], r['user_id'], r['start_date'], r['end_date']
    ))

for _, r in final_occupancy_rate.iterrows():
    
    cursor.execute(insert_final_occupancy, (
        r['apartment_id'], str(int(r['month'])), r['occupancy_rate']
    ))

conn.commit()