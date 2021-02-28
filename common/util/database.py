import os

from peewee import SqliteDatabase, Model, CharField, TextField, TimestampField, IntegrityError

from scraper import get_email, NotFound

DATABASE_PATH = os.path.join(os.path.abspath('../../'), 'hrc-insight.db')

DB = SqliteDatabase(DATABASE_PATH)


class Email(Model):
    sender = CharField()
    recipient = CharField()
    timestamp = TimestampField()
    subject = CharField()
    content = TextField()

    class Meta:
        database = DB


def create_schema(db: SqliteDatabase = DB, models=[Email]):
    db.connect()
    db.create_tables(models=models)


def load_data():
    curr_email = 1

    try:
        while True:
            try:
                email = get_email(email_id=curr_email)
            except NotFound:
                break

            try:
                Email(
                    sender=email.sender,
                    recipient=email.recipient,
                    timestamp=email.timestamp,
                    subject=email.subject,
                    content=email.content
                ).save()

                print(f'finished writing email {curr_email}')

                curr_email += 1

            except IntegrityError as err:
                print(email)
                raise
    except KeyboardInterrupt:
        print(f'Wrote {curr_email} rows. Exiting')
    finally:
        DB.close()


if __name__ == '__main__':
    create_schema()
    load_data()

