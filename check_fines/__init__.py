import os
from datetime import datetime, timezone
import logging

import azure.functions as func

from app_backend.email_sender import EmailSender
from app_backend.road_fines import get_road_fines


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.now(timezone.utc)

    if mytimer.past_due:
        logging.info('The timer is past due!')

    print("Hello from BG road Finester!")

    function_name = os.path.basename(os.path.dirname(__file__))

    email_service = EmailSender()
    road_fines_result = get_road_fines()

    if road_fines_result:
        email_service.send_email(body=road_fines_result)
    else:
        email_service.send_error_email(message=road_fines_result)

    logging.info(f'Python timer trigger function "{function_name}" ran at {utc_timestamp}')
