import requests
import smtplib
from bs4 import BeautifulSoup
from email.message import EmailMessage
from time import sleep
import os

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
    url = f"https://www.upwork.com/ab/jobs/search?q={search_keyword}&sort=relevance"
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

        sleep(180)  # Check every 3 min

if __name__ == "__main__":
    main()
