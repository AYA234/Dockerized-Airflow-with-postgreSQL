
import pandas as pd
import time

# Function to periodically extract data and write to CSV
def extract_and_write_to_csv():

    df = pd.read_csv("winemag-data-130k-v2.csv")
    extracted_data = df.head(10)
    timestamp = int(time.time())
    csv_filename = f"extracted_data_{timestamp}.csv"

    # Write the extracted data to a CSV file in the shared volume
    extracted_data.to_csv(f"/shared_volume/{csv_filename}", index=False)

    print(f"Data extracted and written to /shared_volume/{csv_filename}")

interval_seconds = 3600  

while True:
    extract_and_write_to_csv()
    time.sleep(3)
