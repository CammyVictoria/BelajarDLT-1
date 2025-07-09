# Apartment occupancy rate calculator
Aplikasi untuk menghitung occupancy rate masing-masing apartemen per-bulan dan menyimpan datanya ke dalam 
database MySQL.

[Fitur](##Fitur)
[Instalasi](##Instalasi)
[Cara Kerja Aplikasi](#cara-kerja-aplikasi)
[Changers](#changes)

## Fitur
- Menghitung Occupancy Rate perbulan
- Mencatat data ke MySQL

## Instalasi
1. Pastikan Python sudah terinstall

2. Pastikan MySQL sudah terinstall

3. Lakukan intalasi library berikut di Python:
- pandas
- datetime
- MonthEnd
- pymysql

4. Lakukan cloning git repository dengan
```bash
git clone https://github.com/CammyVictoria/BelajarDLT
```
## Cara Kerja Aplikasi
### Step 1 - load data dari csv menggunakan pandas
pada step ini, data dari booking apartment.csv diload ke python menggunakan library pandas
```python
data_awal = pd.read_csv(r"booking apartment.csv") 
``` 

### Step 2 - pastikan kolom start_date dan end_date sudah menjadi bentuk datetime
hal ini dilakukan agar data lebih mudah diolah
```python
data_awal['start_date'] = pd.to_datetime(data_awal['start_date'])
data_awal['end_date'] = pd.to_datetime(data_awal['end_date'])
```

### Step 3 - pisahkan pemesanan yang bersifat overlapping pada setiap bulan 
contoh: kalau ada 1 row pemesanan dengan
start_date 20 Juni dan end_date 10 Juli, maka dipisah menjadi 2 rows:
rows 1: start_date = 20 Juni, end_date = 30 Juni
rows 2: start_date = 1 Juli, end_date= 10 Juli
```python
def split_rows_by_month(data_awal):
        expanded_rows = []

        for _, row in data_awal.iterrows():
            start = row['start_date']
            end = row['end_date']
            current_start = start

            while current_start <= end:
    ...
```

### Step 4 - hitung perbedaan start_date dan end_date untuk mengetahui berapa hari hotel dibooking
Mengetahui berapa lama hotel ditempati (dalam hitungan hari)
```python
data['day_booked'] = (data['end_date'] - data['start_date']).dt.days + 1
```

### Step 5 - hitung jumlah total unit apartment dibooking setiap bulannya dan bagi dengan 30 (jumlah hari perbulan)
Dilakukan untuk mengetahui occupancy rate setiap unit
```python
grouped = data.groupby(['apartment_id', 'room_id', 'month'])['day_booked'].sum().reset_index()

grouped['occupancy_rate'] = grouped['day_booked']/30
```

### Step 6 - hitung occupancy rate dengan mencari mean dari kolom occupancy_rate untuk setiap apartment di bulan tertentu
Mencari tahu rata-rata occupancy rate setiap hotel perbulan
```python
final_occupancy_rate = grouped.groupby(['apartment_id','month'])['occupancy_rate'].mean()reset_index()
```
### Step 7 - Menghubungkan koneksi ke database
set up koneksi ke database dengan konfigurasi berikut:
```python
conn =  pymysql.connect( 
    host="localhost",
    user="root",
    password="password",
    database="database"
)
```
konfigurasi tersebut dapat diubah sesuai dengan kebutuhan

### Step 8 - Membuat tabel booking_apartment dan occupancy_appartment
Jalankan query SQL untuk membuat tabel tersebut, berikut contoh dari code untuk membuat tabel booking_apartment
```python
create_table = """
CREATE TABLE IF NOT EXISTS booking_apartment(
    apartment_id varchar(10),
    room_id varchar(10),
    user_id varchar(10),
    start_date date,
    end_date date
);
"""
cursor.execute(create_table)
```
### Step 9 - Melakukan eksekusi input data ke dalam tabel database
Memasukkan data awal dan data yang telah diolah ke dalam database MySQL
```python
insert_data_awal = "INSERT INTO booking_apartment(apartment_id,room_id,user_id,start_date,end_date) VALUES(%s,%s,%s,%s,%s);"
for _, r in data_awal.iterrows():
    cursor.execute(insert_data_awal, (
        r['apartment_id'], r['room_id'], r['user_id'], r['start_date'], r['end_date']
    ))
```
## Changes
### Version 1
1. algoritma transformasi data di database.py diubah menjadi fungsi transforming()
2. Membuat variabel baru untuk data awal agar data awal dapat disimpan di dalam database
ke dalam tabel
2. Menghubungkan dengan server mysql menggunakan library pymysql
3. Membuat tabel booking_apartment untuk menyimpan data awal
4. Membuat tabel occupancy_apartment untuk menyimpan hasil perhitungan occupancy rate