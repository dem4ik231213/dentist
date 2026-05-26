from django.contrib import admin
# Імпортуємо всі наші моделі бази даних
from .models import Appointment, Doctor
from .models import ConsultationRequest
from .models import ContactMessage


# === НАЛАШТУВАННЯ ТАБЛИЦІ ПОВІДОМЛЕНЬ З КОНТАКТНОЇ ФОРМИ ===
class ContactMessageAdmin(admin.ModelAdmin):
    # list_display - це колонки, які ми будемо бачити в загальній таблиці адмінки
    list_display = ("name", "email", "status", "created")
    # list_filter - додає бокову панель справа для фільтрації записів (наприклад, тільки "Нові")
    list_filter = ("status",)
    # ordering - сортування. Мінус ("-created") означає, що найновіші повідомлення будуть зверху
    ordering = ("-created",)


# === НАЛАШТУВАННЯ ТАБЛИЦІ ЗАЯВОК НА КОНСУЛЬТАЦІЮ ===
class ConsultationRequestAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "status", "created")
    list_filter = ("status",)


# === НАЛАШТУВАННЯ ТАБЛИЦІ ЛІКАРІВ ===
class DoctorAdmin(admin.ModelAdmin):
    # Залишили тільки найголовніше: ім'я та спеціальність (без зайвих дат і статусів)
    list_display = ('name', 'speciality')


# === НАЛАШТУВАННЯ ТАБЛИЦІ ЗАПИСІВ НА ПРИЙОМ ===
class AppointmentAdmin(admin.ModelAdmin):
    # Відображаємо ключову інформацію про пацієнта та час його прийому
    list_display = ("name", "doctor", "date", "schedule", "created")


# === РЕЄСТРАЦІЯ МОДЕЛЕЙ ===
# Цей блок каже Django: "Візьми модель бази даних і застосуй до неї мої налаштування вище, 
# щоб вона з'явилася на головній сторінці адмін-панелі"
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(ConsultationRequest, ConsultationRequestAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)