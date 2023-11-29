import azure.functions as func
from check_for_internships import check_internship_availability, download_html
import logging
import os
from azure.communication.email import EmailClient

app = func.FunctionApp()

@app.function_name(name="check_for_internship_offers")
@app.schedule(schedule="0 0 8,20 * * *",
              arg_name="mytimer",
              run_on_startup=True)
def function(mytimer: func.TimerRequest) -> None:
    logging.info("Starting function ...")

    url = 'https://www.lifeatspotify.com/jobs?j=internship'
    html = download_html(url)
    result = check_internship_availability(html)
    logging.info(result)

    email_state = "internal" # internal or external

    if result["match"] == True:
        if result["number_of_positions"] > 0:
            subject = f"{result['number_of_positions']} Internship Offers available"
            plainText = f"There are {result['number_of_positions']} offers available."
            email_state = "external"
        else:
            subject = "No Internship Offers available"
            plainText = "Currently, there are no internship offers available. But your code works fine."
            email_state = "internal"
    else:
        subject = "Couldn't find information on internships, please check the website for any changes. "
        plainText = subject
        email_state = "internal"

    connection_string = os.getenv('COMMUNICATION_CONNECTION_STRING')
    email_client = EmailClient.from_connection_string(connection_string)

    recipients = os.getenv('MAILING_LIST').split(",") if email_state == "external" else os.getenv('INTERNAL_MAILING_LIST').split(",")
    # Send to each email in MAILING_LIST
    for receiver_email in recipients:
        message = {
            "content": {
                "subject": subject,
                "plainText": plainText,
                "html": f"<html><h1>{plainText}</h1></html>"
            },
            "recipients": {
                "to": [
                    {"address": f"{receiver_email}", "displayName": "Spotify Internship Checker Bot"}
                ]
            },
            "senderAddress": f"{os.getenv('SENDER_EMAIL')}"
        }

        email_client.begin_send(message)
