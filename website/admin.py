from django.contrib import admin
from .models import Appointment, Doctor
from django.utils import timezone
from .models import ConsultationRequest
from .models import ContactMessage


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "status", "created")
    list_filter = ("status",)
    ordering = ("-created",)


class ConsultationRequestAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "status", "created")
    list_filter = ("status",)
    


class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'speciality', 'status', 'busy_until')
    list_filter = ('status',)


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("name", "doctor", "date", "schedule", "created")

    # --- показуємо тільки вільних лікарів ---
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "doctor":
            kwargs["queryset"] = Doctor.objects.filter(
                status="Available"
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # --- автоматично ставимо Busy + час ---
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if obj.doctor:
            obj.doctor.status = "Busy"
            now = timezone.now()

            if obj.schedule == "9 AM to 10 AM":
                obj.doctor.busy_until = now.replace(hour=10, minute=0, second=0)

            elif obj.schedule == "11 AM to 12 PM":
                obj.doctor.busy_until = now.replace(hour=12, minute=0, second=0)

            elif obj.schedule == "2 PM to 4 PM":
                obj.doctor.busy_until = now.replace(hour=16, minute=0, second=0)

            elif obj.schedule == "8 PM to 10 PM":
                obj.doctor.busy_until = now.replace(hour=22, minute=0, second=0)

            obj.doctor.save()

admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(ConsultationRequest, ConsultationRequestAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)


