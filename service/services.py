import logging
import smtplib

from django.utils import timezone
from django.core.mail import send_mail
from django_apscheduler.jobstores import DjangoJobStore
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.models import DjangoJobExecution
from django.conf import settings as django_conf

from config import settings
from service.models import Mailing, MailingAttempt

logger = logging.getLogger(__name__)


def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


scheduler = BlockingScheduler(timezone=django_conf.TIME_ZONE)


def run_apscheduler():
    scheduler.add_jobstore(DjangoJobStore(), "default")

    scheduler.add_job(
        send_mailing,
        trigger=CronTrigger(minute="*/1"),  # Every 1 minute
        id="send_mailing",  # The `id` assigned to each job MUST be unique
        max_instances=1,
        replace_existing=True,
    )
    logger.info("Added job 'send_mailing'.")

    scheduler.add_job(
        delete_old_job_executions,
        trigger=CronTrigger(
            day_of_week="mon", hour="00", minute="00"
        ),  # Midnight on Monday, before start of the next work week.
        id="delete_old_job_executions",
        max_instances=1,
        replace_existing=True,
    )
    logger.info(
        "Added weekly job: 'delete_old_job_executions'."
    )

    try:
        logger.info("Starting scheduler...")
        scheduler.start()
    except KeyboardInterrupt:
        logger.info("Stopping scheduler...")
        scheduler.shutdown()
        logger.info("Scheduler shut down successfully!")


def send_mailing():
    current_datetime = timezone.now()
    logging.warning(f'текущее время: {current_datetime}')
    # создание объекта с применением фильтра
    mailings = Mailing.objects.filter(first_sent_at__lte=current_datetime, status__in=['Новая', 'Запущена'])

    mailing_attempts_to_create = []
    for mailing in mailings:
        if (current_datetime.minute == mailing.first_sent_at.minute) and (
                current_datetime.hour == mailing.first_sent_at.hour) and (
                (current_datetime - mailing.first_sent_at).days % mailing.frequency.days_until_next_mailing >= 0):
            if mailing.status == 'Новая':
                mailing.status = Mailing.StatusOfMailing.LAUNCHED
                mailing.save()
            try:
                server_response = send_mail(
                    subject=mailing.message_to_send.title,
                    message=mailing.message_to_send.body,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[client.email for client in mailing.client_list.all()],
                    fail_silently=False
                )
                mailing_attempts_to_create.append(MailingAttempt(last_attempt=current_datetime, is_success=True,
                                                                 server_answer=server_response,
                                                                 mailing=mailing))
            except smtplib.SMTPException as e:
                mailing_attempts_to_create.append(MailingAttempt(last_attempt=current_datetime, is_success=False,
                                                                 server_answer=e,
                                                                 mailing=mailing))

    MailingAttempt.objects.bulk_create(mailing_attempts_to_create)
