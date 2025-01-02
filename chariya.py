import requests  # Install using `pip install requests`
from BlaApi import Client  # Assuming this is your custom library for the school app
from html2text import html2text as h2t  # Install using `pip install html2text`
from markdownify import markdownify  # Install using `pip install markdownify`

# Discord webhook URL (replace with yours)
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
  # Login to the school app
  c = Client(username=username, password=password)

  # Get current date or replace with a specific date (optional)
  date = c.get_current_date()
  # date = 'Fri, 04/08/2023'  # Replace with specific date

  student_id = c.students[0].get('student_id')
  print(f"Attempting to get homework/classwork for: {c.students[0].get('student_name')}")

  # Retrieve homework/classwork data
  diary_data = filter_diary(date=date, been_read=True)  # Adjust filter parameters if needed

  # Format and send data to Discord
  formatted_data = format_diary(diary_data)
  for message in formatted_data:
    send_to_discord(message)

if __name__ == "__main__":
  main()
