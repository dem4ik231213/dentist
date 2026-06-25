from django.db import models


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    speciality = models.CharField(max_length=120)

class Appointment(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    email = models.EmailField(db_index=True)
    address = models.CharField(max_length=200, blank=True)
    schedule = models.CharField(max_length=100)
    date = models.CharField(max_length=100, db_index=True)
    message = models.TextField(blank=True)

    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"{self.name} — {self.date}"


class ConsultationRequest(models.Model):

      STATUS_CHOICES = (
        ("new", "New"),
        ("in_progress", "In Progress"),
        ("contacted", "Contacted"),
        ("done", "Done"),
    )
      name = models.CharField(max_length=100, blank=True, null=True)
      email = models.EmailField(db_index=True)
      phone = models.CharField(max_length=50, blank=True)
      message = models.TextField(blank=True)
      created = models.DateTimeField(auto_now_add=True, db_index=True)

      status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="new",
        db_index=True  
     )

class ContactMessage(models.Model):

      STATUS_CHOICES = (
        ("new", "New"),
        ("in_progress", "In Progress"),
        ("done", "Done"),
    )
      name = models.CharField(max_length=100)
      email = models.EmailField(db_index=True)
      message = models.TextField()
      created = models.DateTimeField(auto_now_add=True, db_index=True)

      status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="new",
        db_index=True                                  
     )

      def __str__(self):
        return f"{self.name} — {self.email}"
