import requests
import time
import datetime
import csv
import os

API_KEY = '[insert API key here]'
home = '123+N+Apple+Ln,Your+City,State'
work = '1200+S+Washington+Dr,+Another+City,+State'
headers = {
    'Referer': 'https://yourreffererwebsite.com/'
}
# Define CSV file paths
csv_file_to_work = 'commute_times_to_work.csv'
csv_file_to_home = 'commute_times_to_home.csv'

def get_travel_time(from_home: bool):
    if from_home:
        url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={home}&destinations={work}&departure_time=now&key={API_KEY}"
    else: 
        url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={work}&destinations={home}&departure_time=now&key={API_KEY}"
        
    response = requests.get(url, headers=headers).json()
    
    if response['status'] == 'OK':
        travel_time = response['rows'][0]['elements'][0]['duration_in_traffic']['text']  # get travel time in seconds
        return travel_time
    else:
        return None

def log_to_csv(file_path, date, time, duration):
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, time, duration])

def main():
    print("Starting...")
    # Check if the CSV files exist, if not, create them and write the headers
    for csv_file in [csv_file_to_work, csv_file_to_home]:
        if not os.path.exists(csv_file):
            with open(csv_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Date', 'Time', 'Duration'])

    start_time = datetime.datetime.now()
    interval = 5 * 60  # 5 minutes in seconds

    while True:
        current_time = datetime.datetime.now()
        
        # Get travel time from home to work
        travel_time_to_work = get_travel_time(from_home=True)
        if travel_time_to_work is not None:
            log_to_csv(csv_file_to_work, current_time.date(), current_time.time(), travel_time_to_work)
            print(f"To Work - At {current_time.strftime('%H:%M:%S')}, travel time is {travel_time_to_work}.")
        
        # Get travel time from work to home
        travel_time_to_home = get_travel_time(from_home=False)
        if travel_time_to_home is not None:
            log_to_csv(csv_file_to_home, current_time.date(), current_time.time(), travel_time_to_home)
            print(f"To Home - At {current_time.strftime('%H:%M:%S')}, travel time is {travel_time_to_home}.")
        
        time.sleep(interval - ((datetime.datetime.now() - start_time).total_seconds() % interval))

if __name__ == "__main__":
    main()
