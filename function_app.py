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
    email_client = EmailClient.from_connection_string(connection_string)

    logging.info(os.getenv('RECEIVER_EMAIL'))

