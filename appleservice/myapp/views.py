from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.conf import settings
from django.core.exceptions import ValidationError
from .models import *
from .forms import ServiceFormSet
from time import sleep
from functools import wraps
from datetime import datetime
# Create your views here.

def worker_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.session.get('worker'):
            return view_func(request, *args, **kwargs)
        return redirect('Home')
    return _wrapped_view

def login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.session.get('user_id'):
            return view_func(request, *args, **kwargs)
        return redirect('Login')
    return _wrapped_view

def not_logged_in(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.session.get('user_id'):
            return view_func(request, *args, **kwargs)
        return redirect('Home')
    return _wrapped_view

def home(request):
    locations = Lokacja.objects.all()
    return render(request, "home.html", {'locations': locations})

@not_logged_in
def login_panel(request):
    message = ""
    if request.method == 'POST':
        is_worker = request.POST.get('is_worker') == 'worker'
        database = Klient
        if is_worker: 
            database = Pracownik
        user = None
        
        try:
            user = database.objects.get(email=request.POST.get('email'))
        except database.DoesNotExist:
            user = None

        if is_worker and not user.zatwierdzony: user = None

        if user and check_password(request.POST.get('password'), user.haslo):
            request.session['user_id'] = user.id
            request.session['email'] = user.email
            request.session['worker'] = is_worker
            if is_worker: request.session['location'] = user.lokacja.nazwa_lokacji
            request.session.set_expiry(60 * 60 * 24 * 30 * (request.POST.get('remember_me') == 'remember_me')) # 60 seconds * 60 minutes * 24 hours * 30 days * (1 or 0) = 30 dniowy token (albo nie)
            return redirect('Home')
        else:
            message = "Błędny adres e-mail lub hasło!"

    return render(request, 'login.html', {'message': message})

def append_id(last_id):
    # zero pad 7 digits
    return f"{last_id[0]}{(int(last_id[1:]) + 1):07d}"

@not_logged_in
def register_panel(request):
    locations = Lokacja.objects.all()
    message = ""
    if request.method == 'POST':
        is_worker = request.POST.get('is_worker') == 'worker'
        database = Klient
        if is_worker: 
            database = Pracownik

        if database.objects.filter(email = request.POST.get('email')).exists():
            message = "Ten adres e-mail jest już zarejestrowany!"
        else:
            next_id = append_id(database.objects.order_by('-id').first().id)

            new_user = database(
                id = next_id,
                email = request.POST.get('email'),
                haslo = make_password(request.POST.get('password')),
                imie = request.POST.get('firstName'),
                nazwisko = request.POST.get('lastName'),
                telefon = request.POST.get('phone'),
            )

            if is_worker and request.POST.get('location') == "Wybierz lokację...": message = 'Wybierz właściwą lokakację!'
            else: 
                if is_worker: new_user.lokacja = Lokacja.objects.get(nazwa_lokacji = request.POST.get('location'))
                new_user.save()
                messages.info(request, "Pomyślnie utworzono konto!")
                sleep(1)
                return redirect("Login")
        
    return render(request, "register.html", {'message': message, 'locations': locations,})

@login_required
def settings_panel(request):
    message = ""
    database = Klient
    if request.session.get('worker'):
        database = Pracownik

    user = database.objects.get(id = request.session.get('user_id'))

    if request.method == 'POST':
        if request.POST.get('email') != user.email and database.objects.filter(email = request.POST.get('email')).exists():
            message = "Ten adres e-mail jest już zarejestrowany!"
        elif check_password(request.POST.get('old_password'), user.haslo):
            user.email = request.POST.get('email')
            request.session['email'] = user.email
            user.telefon = request.POST.get('phone')
            if request.POST.get('new_password'): user.haslo = make_password(request.POST.get('new_password'))
            user.save()
            return redirect("Home")
        else:
            message = "Błędne hasło!"


    return render(request, "settings.html", {'message': message, 'user': user})

@worker_required
def dashboard_panel(request):
    return redirect('Zlecenia')

def combine_datetime(data, godzina):
    return datetime.strptime(f"{data} {godzina}", "%d.%m.%Y %H:%M")

def visit_panel(request):
    locations = Lokacja.objects.all()
    message = ""

    if request.method == 'POST':
        
        try: 
            termin = combine_datetime(request.POST.get("data"), request.POST.get("godzina"))
            validate_time(termin)
        except ValueError: message = "Zły format daty."
        except ValidationError as error: message = error.message
        else:
            zlecenie = Zlecenie(
            id_zlecenia = "zl" + datetime.now().strftime("%Y%m%d%H%M%S%f"),
            id_klienta = Klient.objects.get(id = request.session.get('user_id')),
            id_lokacji = Lokacja.objects.get(nazwa_lokacji = request.POST.get('lokacja')),
            model = request.POST.get('model'),
            notes = request.POST.get('notes'),
            pakiet_diagnostyczny = request.POST.get("diagnoza") == "diagnoza",
            termin_zlecenia = termin
            )
            zlecenie.save()
            return redirect("Home")
    return render(request, "visit.html", {'message': message, 'locations': locations})

@worker_required
def zlecenia_panel(request):
    zlecenia = Zlecenie.objects.all()
    zlecenia_titles = ["ID Zlecenia", "Termin wizyty", "Klient", "ID Pracownika", "Status", "Termin realizacji"]
    return render(request, "dashboard/zlecenia.html", 
                  {'zlecenia': zlecenia, 
                   'zlecenia_titles': zlecenia_titles})

@worker_required
def faktury_panel(request):
    zlecenia = Zlecenie.objects.all()
    zlecenia_titles = ["ID Zlecenia", "ID Klienta", "ID Pracownika", "Termin realizacji"]
    return render(request, "dashboard/faktury.html", 
                {'zlecenia': zlecenia, 
                   'zlecenia_titles': zlecenia_titles})

@worker_required
def magazyn_panel(request):
    zlecenia = Zlecenie.objects.all()
    zlecenia_titles = ["ID Zlecenia", "ID Klienta", "ID Pracownika", "Status", "Termin wizyty", "Termin realizacji"]
    return render(request, "dashboard/magazyn.html", 
                  {'zlecenia': zlecenia, 
                   'zlecenia_titles': zlecenia_titles})

@worker_required
def zlecenia_view(request, zl_id_zlecenia):
    status_choices = Zlecenie.Status.choices
    zlecenie = Zlecenie.objects.get(id_zlecenia = zl_id_zlecenia)

    if request.method == 'POST':
        actions = ['take', 'finish', 'archive', 'renew', 'SAVE', 'DELETE']
        action = request.POST.get('action')
        formset = ServiceFormSet(request.POST, instance=zlecenie)

        if action not in actions: return HttpResponseForbidden("Invalid action.")
        if action != actions[4]: formset = ServiceFormSet(instance = zlecenie)
        if action == actions[0]:
            zlecenie.id_pracownika = Pracownik.objects.get(id = request.session['user_id'])
            zlecenie.status_zlecenia = 1
            zlecenie.save()
        elif action == actions[1]:
            zlecenie.status_zlecenia = 2
            zlecenie.save()
        elif action == actions[2]:
            zlecenie.termin_realizacji = datetime.now()
            zlecenie.status_zlecenia = 3
            zlecenie.save()
        elif action == actions[3]:
            zlecenie.status_zlecenia = 1
            zlecenie.save()
        elif action == actions[4]:
            sleep(.5)
            zlecenie.model = request.POST.get('_model')
            zlecenie.nr_seryjny = request.POST.get('_serial_nr')
            zlecenie.diagonza = request.POST.get('_diagnoza')
            zlecenie.notes = request.POST.get('_notes')

            if formset.is_valid():
                for form in formset:
                    data = form.cleaned_data
                    if data and not data.get('service') and not data.get('price'):
                        data['DELETE'] = True
                formset.save()
                zlecenie.save()
            zlecenie.save()
        elif action == actions[5]:
            zlecenie.delete()
            return redirect('Zlecenia')
        return redirect('Zlecenia_view', zl_id_zlecenia=zlecenie.id_zlecenia)
    else:
        formset = ServiceFormSet(instance = zlecenie)

    return render(request, "dashboard/zlecenia_view.html", {'zlecenie': zlecenie, 'status_choices': status_choices, 'formset': formset})

@worker_required
def faktury_view(request, zl_id_zlecenia):
    zlecenie = Zlecenie.objects.get(id_zlecenia = zl_id_zlecenia)
    klient = zlecenie.id_klienta
    formset = ServiceFormSet(instance = zlecenie)
    if request.method == 'POST': 
        for field in Klient._meta.get_fields():
            val = request.POST.get(field.name)
            if val is not None: setattr(klient, field.name, val)
        klient.save()
        return redirect('Faktury_view', zl_id_zlecenia=zlecenie.id_zlecenia)
    return render(request, "dashboard/faktury_view.html", {'zlecenie': zlecenie, 'formset': formset})

def logout_view(request):
    request.session.flush()
    return redirect('Home')