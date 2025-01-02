import requests
from BlaApi import Client
from html2text import html2text as h2t
from markdownify import markdownify
from time import sleep

import requests
from BlaApi import Client
from html2text import html2text as h2t
from markdownify import markdownify
from time import sleep

# Discord webhook URL 
webhook_url = "https://discord.com/api/webhooks/1318358536261992530/XlT3IzvrVthRB5jqYsZxSVQfPBzEV9M93LWp3D_kQqe7CzNgM-Yj8uGwLUOTue7x7sGQ" 

# School app login credentials
username = '03452101562'
password = 'wajeeh6813'


def send_to_discord(message):
    """Sends a message to the Discord channel using the provided webhook URL."""
    data = {"content": message}
    headers = {"Content-Type": "application/json"}
    response = requests.post(webhook_url, headers=headers, json=data)
    if response.status_code == 200:
        print("Message sent to Discord successfully!")
    else:
        print(f"Error sending message to Discord: {response.status_code}")

def format_diary(diary_data):
    """Formats the homework/classwork details in a Discord-friendly way."""
    # ... (Your existing format_diary function) ...

def main():
    c = Client(username=username, password=password)
    student_id = c.students[0].get('student_id')
    print(f"Monitoring homework/classwork for: {c.students[0].get('student_name')}")

    previous_diaries = []  # Store previously sent diary IDs

    while True:
        try:
            date = c.get_current_date()
            diaries = c.search_by_student(student_id=student_id)
            diaries = c.search_by_date(date=date, passthru=diaries) 

            new_diaries = []
            for diary in diaries:
                if diary['notificationId'] not in previous_diaries:
                    new_diaries.append(diary)
                    previous_diaries.append(diary['notificationId'])

            if new_diaries:
                formatted_data = format_diary(new_diaries)
                for message in formatted_data:
                    send_to_discord(message)

        except Exception as e:
            print(f"An error occurred: {e}")

        sleep(60)  # Wait for 60 seconds before checking for new diaries

if __name__ == "__main__":
    main()
