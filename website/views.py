from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import Appointment, ConsultationRequest, ContactMessage
#from django.core.mail import send_mail


def home(request):
    context = {}
    if request.user.is_authenticated:
        context['prefill'] = {
            'name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
            'email': request.user.email,
        }
    return render(request, 'home.html', context)


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
        messages.success(request, "Ваше повідомлення надіслано успішно!")
        return redirect("contact")
    return render(request, "contact.html")


def about(request):
    return render(request, 'about.html', {})


def pricing(request):
    return render(request, 'pricing.html', {})


def service(request):
    return render(request, 'service.html', {})


def appointment(request):
    if request.method == "POST" and 'your-name' in request.POST:
        your_name = request.POST['your-name']
        your_phone = request.POST['your-phone']
        your_email = request.POST['your-email']
        your_address = request.POST['your-address']
        your_schedule = request.POST['your-schedule']
        your_date = request.POST['your-date']
        your_message = request.POST['your-message']

        appointment = Appointment.objects.create(
            name=your_name,
            phone=your_phone,
            email=your_email,
            address=your_address,
            schedule=your_schedule,
            date=your_date,
            message=your_message
        )

        # СПОВІЩЕННЯ В TELEGRAM
        try:
            from website.telegram_notify import notify_admin_new_appointment
            notify_admin_new_appointment(appointment)
        except Exception as e:
            print(f"Помилка відправки Telegram: {e}")
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
        context = {}
        if request.user.is_authenticated:
            context['prefill'] = {
                'name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
                'email': request.user.email,
            }
        return render(request, 'home.html', context)


def sitemap_xml(request):
    xml = render_to_string("sitemap.xml")
    return HttpResponse(xml, content_type="application/xml")