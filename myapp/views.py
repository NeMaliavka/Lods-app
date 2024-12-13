import logging
from django.http import HttpResponse
import yagmail
import smtplib
from email.mime.text import MIMEText

logger = logging.getLogger('my_logger')

def my_view(request):
    logger.debug('Это отладочное сообщение')
    logger.info('Это информационное сообщение')
    logger.warning('Это предупреждение')
    logger.error('Это сообщение об ошибке', exc_info=True)
    logger.critical('Это критическое сообщение', exc_info=True)
    return HttpResponse("Hello, world!")


def send_test_email():
    msg = MIMEText('Это тестовое сообщение.')
    msg['Subject'] = 'Тест'
    msg['From'] = 'alisa.xorok@gmail.com'
    msg['To'] = 'alisa.krushinina@mail.ru'

    try:
        with yagmail.SMTP('smtp.yandex.ru', 465) as server:
            server.login('alisa.xorok@gmail.com', 'SecretPassword')
            server.sendmail(msg['From'], [msg['To']], msg.as_string())
            print("Тестовое сообщение отправлено успешно.")
    except Exception as e:
        print(f"Ошибка при отправке тестового сообщения: {e}")

send_test_email()
