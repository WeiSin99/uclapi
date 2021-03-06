from __future__ import absolute_import

import os
import keen
import requests

from celery import shared_task


@shared_task
def test_task(param):
    return 'The test task executed with argument "%s" ' % param


@shared_task
def keen_add_event_task(title, data):
    try:
        keen.add_event(title, data)
    except keen.exceptions.InvalidProjectIdError as e:
        return 'Keen failed for the event titled ' + \
                title + ' because the Keen project ID is " + \
                " invalid. The API said: ' + e.message
    except keen.exceptions.KeenApiError as e:
        return 'Keen failed for the event titled ' + \
                title + ' because of an API error: ' + e.message
    except keen.exceptions.InvalidEnvironmentError as e:
        return 'Keen failed for the event titled ' + \
                title + ' because of an invalid Environment: ' + \
                e.message
    except keen.exceptions.BaseKeenClientError as e:
        return 'Keen failed for the event titled ' + \
                title + ' because of some other Keen error: ' + e.message
    except Exception:
        return 'Keen failed for event titled ' + \
                title + 'Please check your internet connection.'

    return 'Keen added a new event titled ' + title


@shared_task
def add_user_to_mailing_list_task(email, name):
    add_user_to_mailing_list(email, name)


def add_user_to_mailing_list(email, name):
    data = {
        "email_address": email,
        "status": "subscribed",
        "merge_fields": {
            "EMAIL": email,
            "FNAME": name
        }
    }

    headers = {
        "Authorization": "apikey {}".format(
            os.environ["MAILCHIMP_API_KEY"])
    }

    requests.post(
        os.environ["MAILCHIMP_ENDPOINT"], json=data, headers=headers)
