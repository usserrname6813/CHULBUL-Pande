import requests
from BlaApi import Client
from html2text import html2text as h2t
from markdownify import markdownify
from time import sleep
from flask import Flask
from threading import Thread

# Discord webhook URL
webhook_url = "https://discord.com/api/webhooks/1318358536261992530/XlT3IzvrVthRB5jqYsZxSVQfPBzEV9M93LWp3D_kQqe7CzNgM-Yj8uGwLUOTue7x7sGQ"

# School app login credentials
username = '03452101562'
password = 'wajeeh6813'

app = Flask('')

@app.route('/')
def home():
    return "The bot is running!"

def keep_alive():
    """Starts a thread to run a Flask server."""
    t = Thread(target=lambda: app.run(host='0.0.0.0', port=8080))
    t.start()

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
    output = []
    for d in diary_data:
        details = markdownify(d.get('details'))
        details = details.replace('**', '*')
        details = details.replace('\\', '')
        details = details.replace('   ', ' ')
        details = details.replace('_', '')

        subject = f"Subject: {d.get('subject')}" if d.get('subject') else "Notice"

        attachment_link = "https://beaconlightacademy.edu.pk/app/uploaded/" if d.get('attachmentId') else ""
        attachments = f"Attachments: {attachment_link}{d['attachmentId']}" if d.get('attachmentId') else ""

        message = f"{subject}\n{details}\n{attachments}"
        output.append(message)
    return output

def main():
    c = Client(username=username, password=password)
    student_id = c.students[0].get('student_id')
    print(f"Monitoring homework/classwork for: {c.students[0].get('student_name')}")

    previous_diaries = []  # Store previously sent diary IDs

    while True:
        try:
            date = c.get_current_date()
            diaries = c.search_by_student(student_id=student_id)
            diaries = c.search_by_date(date, passthru=diaries) 

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
    keep_alive()  # Start the web server
    main()
