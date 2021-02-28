from collections import namedtuple
from datetime import datetime
from pprint import pprint
from string import printable

from bs4 import BeautifulSoup

import requests


Email = namedtuple('Email', 'sender recipient timestamp subject content')


class NotFound(Exception):
    pass


def get_email(*, email_id):
    """
    GETS EMAILS BY EMAIL ID FROM WIKILEAKS
    :param email_id: Email Id
    :return: Email namedtuple containing sender, recipient, timestamp, subject, content
    """

    url = f'https://wikileaks.org/clinton-emails/emailid/{email_id}'

    res: requests.Response = requests.get(url)

    soup = BeautifulSoup(res.content, features='html.parser')

    if soup.find(class_='text-danger well h4'):
        raise NotFound(f'Email with id "{email_id}" not found. Check url {url}') from None

    header = soup.find(id='header')
    content = soup.find(class_='email-content')

    sender, recipient, timestamp, subject = [item.strip('\t').split(':', 1)[1].strip()
                     for item in header.text.strip('\t').strip('\n').split('\n') if item != '']

    content = ''.join(*[filter(lambda x: x in printable and x != '\t', content.text)])
    content = '\n'.join([' '.join(line.split()) for line in content.split('\n') if line])

    record = Email(
        sender,
        recipient,
        datetime.strptime(timestamp, '%Y-%m-%d %H:%M'),
        subject,
        content
    )

    return record


if __name__ == '__main__':
    email = get_email(email_id=2)

    print('sender: \t', email.sender)
    print('recipient:\t', email.recipient)
    print('timestamp:\t', email.timestamp)
    print('subject:\t', email.subject)
    print()
    print(email.content)
