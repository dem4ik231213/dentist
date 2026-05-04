from django.shortcuts import render
from .models import Appointment
from django.shortcuts import render, redirect
from .models import Appointment, ConsultationRequest
from .models import ContactMessage
from django.contrib import messages


#from django.core.mail import send_mail


def home(request):
    return render(request, 'home.html', {})

def free_consultation(request):
    if request.method == "POST":
        name = request.POST.get("name") or request.POST.get("message-name")
        email = request.POST.get("email") or request.POST.get("message-email")
        phone = request.POST.get("phone", "")
        message = request.POST.get("message", "")


        ConsultationRequest.objects.create(
            name=name,
           email=email,
            phone=phone,
            message=message
        )

        return redirect("home")   

    return redirect("home")

def blog1(request):
    return render(request, 'blog-details1.html')

def blog2(request):
    return render(request, 'blog-details2.html')

def blog3(request):
    return render(request, 'blog-details3.html')



def contact(request):
    if request.method == "POST":
        name = request.POST.get("message-name")
        email = request.POST.get("message-email")
        message_text = request.POST.get("message")

        ContactMessage.objects.create(
            name=name,
            email=email,
            message=message_text
        )

        messages.success(request, "Your message has been sent successfully!")
        return redirect("contact")

    return render(request, "contact.html")

        #send_mail(
    #		message_name,
    #		message,
    #		message_email,
    #		['your@email.com'],
    #		)



def about(request):
    return render(request, 'about.html', {})


def pricing(request):
    return render(request, 'pricing.html', {})


def service(request):
    return render(request, 'service.html', {})


def appointment(request):
    if request.method == "POST"  and 'your-name' in request.POST:
        your_name = request.POST['your-name']
        your_phone = request.POST['your-phone']
        your_email = request.POST['your-email']
        your_address = request.POST['your-address']
        your_schedule = request.POST['your-schedule']
        your_date = request.POST['your-date']
        your_message = request.POST['your-message']
  
  #  ЗБЕРЕЖЕННЯ В БАЗУ ДАНИХ
        Appointment.objects.create(
            name=your_name,
            phone=your_phone,
            email=your_email,
            address=your_address,
            schedule=your_schedule,
            date=your_date,
            message=your_message
        )

        
        # send an email
        #appointment = "Name: " + your_name + " Phone: " + your_phone + " Email: " + your_email + " Address: "\
        #	+ your_address + " Schedule: " + your_schedule + " Day: " + your_date + " Message: " + your_message

        #send_mail(
        #	'Appointment Request',
        #	appointment,
        #	your_email,
        #	['drHowardM@gmail.com'],
        #	)
        
        return render(request, 'appointment.html', {
            'your_name': your_name,
            'your_phone': your_phone,
            'your_email': your_email,
            'your_address': your_address,
            'your_schedule': your_schedule,
            'your_date': your_date,
            'your_message': your_message
            })

    else:
        return render(request, 'home.html', {})