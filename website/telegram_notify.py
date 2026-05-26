import os
import logging
import requests

logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_ADMIN_CHAT_ID = os.getenv('TELEGRAM_ADMIN_CHAT_ID')


def send_telegram_message(text, chat_id=None):
    """Універсальна функція відправки повідомлення в Telegram."""
    if not TELEGRAM_BOT_TOKEN:
        logger.warning("TELEGRAM_BOT_TOKEN не налаштований — сповіщення не надіслано")
        return False

    target_chat = chat_id or TELEGRAM_ADMIN_CHAT_ID
    if not target_chat:
        logger.warning("Не вказано chat_id для відправки")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        response = requests.post(
            url,
            data={
                'chat_id': target_chat,
                'text': text,
                'parse_mode': 'HTML',
                'disable_web_page_preview': True,
            },
            timeout=10
        )
        if response.status_code == 200:
            return True
        logger.error(f"Telegram API error: {response.status_code} - {response.text}")
        return False
    except Exception as e:
        logger.error(f"Помилка відправки в Telegram: {e}")
        return False


def notify_admin_new_appointment(appointment):
    """Сповіщення адміну про новий запис на прийом."""
    doctor_name = appointment.doctor.name if appointment.doctor else "Не обрано"
    
    text = (
        f"🆕 <b>Новий запис на прийом!</b>\n\n"
        f"👤 <b>Пацієнт:</b> {appointment.name}\n"
        f"📞 <b>Телефон:</b> {appointment.phone}\n"
        f"📧 <b>Email:</b> {appointment.email}\n"
        f"📅 <b>Дата:</b> {appointment.date}\n"
        f"🕐 <b>Час:</b> {appointment.schedule}\n"
        f"🦷 <b>Лікар:</b> {doctor_name}\n"
    )
    
    if appointment.address:
        text += f"📍 <b>Адреса:</b> {appointment.address}\n"
    
    if appointment.message:
        text += f"💬 <b>Повідомлення:</b> {appointment.message}\n"
    
    text += f"\n🌐 Сайт: dentist-production-0f00.up.railway.app"
    
    return send_telegram_message(text)


def notify_admin_consultation_request(consultation):
    """Сповіщення про запит на консультацію."""
    text = (
        f"💬 <b>Новий запит на консультацію!</b>\n\n"
        f"👤 <b>Ім'я:</b> {consultation.name or 'Не вказано'}\n"
        f"📧 <b>Email:</b> {consultation.email}\n"
        f"📞 <b>Телефон:</b> {consultation.phone or 'Не вказано'}\n"
        f"💬 <b>Повідомлення:</b> {consultation.message}\n"
    )
    return send_telegram_message(text)


def notify_admin_contact_message(contact):
    """Сповіщення про повідомлення з форми контактів."""
    text = (
        f"📨 <b>Нове повідомлення з форми контактів!</b>\n\n"
        f"👤 <b>Ім'я:</b> {contact.name}\n"
        f"📧 <b>Email:</b> {contact.email}\n"
        f"💬 <b>Повідомлення:</b> {contact.message}\n"
    )
    return send_telegram_message(text)
