import csv
import mysql.connector
from mysql.connector import Error

def drop_table(conn,query_drop):
    # this function will drop the table
    c=conn.cursor()
    try:
        c.execute(query_drop)
        print("Table dropped successfully")
    
    except Error as e:
        print("Error occurred when dropping data",e)

# Connect to the MySQL database
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='project_redbus'
)

# Create a cursor object
cursor = conn.cursor()

#drop tabel do it only once
drop_table(conn,"drop table if exists bus_data")

# Create the SQL table if it doesn't exist
create_table_query = '''
CREATE TABLE IF NOT EXISTS bus_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bus_no INT,
    bus_name VARCHAR(100),
    bus_type VARCHAR(100),
    departing_time TIME,
    duration VARCHAR(100),
    reaching_time TIME,
    star_rating FLOAT,
    price DECIMAL(10,0),
    seat_available INT
);
'''
cursor.execute(create_table_query)

# Prepare the insert query
insert_data_query = """insert into bus_data (bus_no,bus_name,bus_type,departing_time,duration,reaching_time,star_rating,price,seat_available) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)
on duplicate key update bus_no = values(bus_no), bus_name = values(bus_name), bus_type = values(bus_type), departing_time = values(departing_time), duration = values(duration),
reaching_time = values(reaching_time), star_rating = values(star_rating), price = values(price), seat_available = values(seat_available)
"""


# Read the CSV file and insert data into the table
with open('D:\\python\\VsCodePythonWorkplace\\bus_data10.csv', mode='r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip the header row
    i=0
    for row in csv_reader:
        print(i)
        i+=1
        # Convert the row data to the correct types
        bus_no = int(row[0])
        bus_name = row[1]
        bus_type = row[2]
        departing_time = row[3]
        duration = row[4]
        reaching_time = row[5]
        star_rating = 3.0 if row[6]=="" else float(row[6])
        price = float(row[7])
        seat_availability = int(row[8])

        # Insert the row into the table
        cursor.execute(insert_data_query, (
            bus_no, bus_name, bus_type, departing_time, duration, reaching_time, star_rating, price, seat_availability
        ))

# Commit the transaction
conn.commit()

# Close the connection
conn.close()
