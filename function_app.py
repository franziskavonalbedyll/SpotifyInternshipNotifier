import azure.functions as func
from check_for_internships import check_internship_availability, download_html
import logging
import os
from azure.communication.email import EmailClient

app = func.FunctionApp()

@app.function_name(name="check_for_internship_offers")
@app.schedule(schedule="0 * * * * *",
              arg_name="mytimer",
              run_on_startup=True)
def function(mytimer: func.TimerRequest) -> None:
    url = 'https://www.lifeatspotify.com/jobs?j=internship'
    logging.info("Starting function ...")
    html = download_html(url)
    logging.info(check_internship_availability(html))

    connection_string = os.getenv('COMMUNICATION_CONNECTION_STRING')
    logging.info(connection_string)
    email_client = EmailClient.from_connection_string(connection_string)

    message = {
        "content": {
            "subject": "New Internship Alert",
            "plainText": "A new internship offer has been posted.",
            "html": "<html><h1>A new internship offer has been posted.</h1></html>"
        },
        "recipients": {
            "to": [
                {"address": f"{os.getenv('RECEIVER_EMAIL')}", "displayName": "Your Name"}
            ]
        },
        "senderAddress": f"{os.getenv('SENDER_EMAIL')}"
    }
    poller = email_client.begin_send(message)
    result = poller.result()
