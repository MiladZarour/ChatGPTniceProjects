import requests
import smtplib
from bs4 import BeautifulSoup
from email.message import EmailMessage
from time import sleep
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration
email_address = os.environ["EMAIL_ADDRESS"]
email_password = os.environ["EMAIL_PASSWORD"]
receiver_email = os.environ["RECEIVER_EMAIL"]
search_keyword = "python"

def send_email(job_title, job_link):
    msg = EmailMessage()
    msg.set_content(f"New job on Upwork:\n\n{job_title}\n{job_link}")

    msg["Subject"] = f"New Upwork Job: {job_title}"
    msg["From"] = email_address
    msg["To"] = receiver_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(email_address, email_password)
        server.send_message(msg)

def get_new_jobs():
    url = "https://www.upwork.com/nx/jobs/search/?q=python&sort=recency&t=1&amount=100-499,500-999,1000-4999,5000-,30-&payment_verified=1"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []
    for job in soup.find_all("section", {"class": "job-tile"}):
        title = job.find("a", {"class": "job-title"}).text
        link = "https://www.upwork.com" + job.find("a", {"class": "job-title"})["href"]
        jobs.append((title, link))

    return jobs

def main():
    sent_jobs = set()

    while True:
        print("Checking for new jobs...")
        new_jobs = get_new_jobs()

        for title, link in new_jobs:
            if link not in sent_jobs:
                print(f"Found new job: {title}")
                send_email(title, link)
                sent_jobs.add(link)

        sleep(3)  # Check every 3 minutes

def main():
    sent_jobs = set()
    interval = 180  # Check every 3 minutes

    while True:
        print("Checking for new jobs...")
        new_jobs = get_new_jobs()

        for title, link in new_jobs:
            if link not in sent_jobs:
                print(f"Found new job: {title}")
                send_email(title, link)
                sent_jobs.add(link)

        # Send an email even if there's no new job
        if not new_jobs:
            send_email("No new jobs found", "There are no new jobs matching your search criteria.")

        for remaining_time in range(interval, 0, -1):
            print(f"Next check in {remaining_time} seconds...", end='\r')
            sleep(1)
        print("\n")

if __name__ == "__main__":
    main()
