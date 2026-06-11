from django.contrib.auth.models import User, Group
from website.models import Doctor
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.conf import settings
from django import forms
import resend


# ============================================================
# РОЛЬОВА СИСТЕМА - Helper функції
# ============================================================

def get_user_role(user):
    """Повертає роль користувача у вигляді рядка."""
    if not user.is_authenticated:
        return 'anonymous'
    if user.is_superuser:
        return 'superuser'
    if user.groups.filter(name='HeadDoctor').exists():
        return 'head_doctor'
    if user.groups.filter(name='Receptionist').exists():
        return 'receptionist'
    if user.groups.filter(name='Doctors').exists():
        return 'doctor'
    return 'patient'


def is_staff_user(user):
    """Перевірка чи має юзер доступ до staff_dashboard."""
    if not user.is_authenticated:
        return False
    if user.is_superuser or user.is_staff:
        return True
    return user.groups.filter(
        name__in=['Doctors', 'Receptionist', 'HeadDoctor']
    ).exists()


# ============================================================
# ФОРМИ
# ============================================================

class PatientRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True, label="Ім'я")
    last_name = forms.CharField(max_length=50, required=True, label="Прізвище")
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput,
        help_text="Мінімум 8 символів, не лише цифри."
    )
    password2 = forms.CharField(
        label="Підтвердження пароля",
        widget=forms.PasswordInput,
        help_text=""
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Паролі не співпадають")
        from django.contrib.auth.password_validation import validate_password
        validate_password(password2)
        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Користувач з таким email вже існує")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.is_active = False
        if commit:
            user.save()
            patients_group, _ = Group.objects.get_or_create(name='Patients')
            user.groups.add(patients_group)
        return user


# ============================================================
# EMAIL VERIFICATION
# ============================================================

def send_verification_email(request, user):
    from django.utils.html import strip_tags
    resend.api_key = settings.RESEND_API_KEY

    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    verify_url = f"https://dentist-production-0f00.up.railway.app/accounts/verify-email/{uid}/{token}/"

    subject = "🦷 Підтвердження email — Стоматологія Dento"
    html_message = render_to_string('accounts/verification_email.html', {
        'user': user,
        'verify_url': verify_url,
    })
    plain_message = strip_tags(html_message)

    resend.Emails.send({
    "from": "onboarding@resend.dev",
    "to": [user.email],
    "subject": subject,
    "html": html_message,
})
print("RESEND RESPONSE:", response)

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = PatientRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            try:
                send_verification_email(request, user)
                messages.success(request,
                    f"Реєстрація успішна! Ми надіслали лист на {user.email}. "
                    "Перейдіть за посиланням у листі, щоб підтвердити свій email.")
            except Exception:
                messages.error(request,
                    "Реєстрація відбулась, але не вдалось надіслати email. Зв'яжіться з підтримкою.")
            return redirect('login')
    else:
        form = PatientRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Email успішно підтверджено! Тепер ви можете увійти.")
        return redirect('login')
    else:
        messages.error(request, "Посилання недійсне або застаріло.")
        return redirect('login')


def resend_verification(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        try:
            user = User.objects.get(email=email, is_active=False)
            send_verification_email(request, user)
            messages.success(request, f"Лист повторно надіслано на {email}")
        except User.DoesNotExist:
            messages.error(request, "Не знайдено непідтверджений акаунт з таким email")
        except Exception:
            messages.error(request, "Не вдалось надіслати лист")
        return redirect('login')
    return render(request, 'accounts/resend_verification.html')


# ============================================================
# LOGIN / LOGOUT
# ============================================================

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"З поверненням, {user.first_name or user.username}!")
            if is_staff_user(user):
                return redirect('staff_dashboard')
            return redirect('dashboard')
        else:
            username = request.POST.get('username', '')
            try:
                u = User.objects.get(username=username)
                if not u.is_active:
                    messages.error(request, "unverified")
                else:
                    messages.error(request, "Невірний логін або пароль")
            except User.DoesNotExist:
                messages.error(request, "Невірний логін або пароль")
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "Ви вийшли з системи")
    return redirect('home')


# ============================================================
# DASHBOARDS - різні за роллю
# ============================================================

@login_required
def dashboard(request):
    """Пацієнтський кабінет."""
    from website.models import Appointment
    my_appointments = Appointment.objects.filter(email=request.user.email).order_by('-date')
    return render(request, 'accounts/dashboard.html', {
        'appointments': my_appointments,
    })


@login_required
@user_passes_test(is_staff_user, login_url='/accounts/login/')
def staff_dashboard(request):
    """
    Дашборд для персоналу клініки.
    Показує різний шаблон залежно від ролі користувача.
    """
    from website.models import Appointment, ContactMessage, ConsultationRequest

    role = get_user_role(request.user)

    # ============ ГОЛОВНИЙ ЛІКАР або SUPERUSER ============
    if role in ('head_doctor', 'superuser'):
        appointments = Appointment.objects.all().order_by('-date')
        consultations = ConsultationRequest.objects.all().order_by('-id')
        messages_list = ContactMessage.objects.all().order_by('-id')

        stats = {
            'total_appointments': appointments.count(),
            'total_consultations': consultations.count(),
            'total_messages': messages_list.count(),
            'total_doctors': Doctor.objects.count(),
        }

        return render(request, 'accounts/dashboard_head_doctor.html', {
            'appointments': appointments[:30],
            'consultations': consultations[:20],
            'messages_list': messages_list[:20],
            'stats': stats,
            'role_name': 'Головний лікар',
        })

    # ============ Адміністратор ============
    elif role == 'receptionist':
        return render(request, 'accounts/dashboard_receptionist.html', {
            'appointments': Appointment.objects.all().order_by('-date')[:50],
            'consultations': ConsultationRequest.objects.all().order_by('-id')[:30],
            'messages_list': ContactMessage.objects.all().order_by('-id')[:30],
            'role_name': 'Адміністратор клініки',
        })

    # ============ ЛІКАР ============
    elif role == 'doctor':
        return render(request, 'accounts/dashboard_doctor.html', {
            'appointments': Appointment.objects.all().order_by('-date')[:50],
            'role_name': 'Лікар',
        })

    # ============ Без ролі — на пацієнтський кабінет ============
    else:
        return redirect('dashboard')
