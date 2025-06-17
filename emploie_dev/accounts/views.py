from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.core.mail import send_mail, EmailMessage
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from emploie_dev import settings
from .tokens import generateToken
from .forms import RegisterForm

# Page d'accueil
def home(request):
    return render(request, 'home.html')


# Inscription
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpwd = request.POST.get('confirm_password')
        if not all([username, email, password, confirmpwd]):
            messages.error(request, "Tous les champs sont obligatoires.")
            return redirect('register')
        if User.objects.filter(username=username).exists():
            messages.error(request, "Nom d'utilisateur déjà pris.")
            return redirect('register')
        if User.objects.filter(email=email).exists():
            messages.error(request, "Cet email possède déjà un compte.")
            return redirect('register')
        if len(username) > 10 or len(username) < 5:
            messages.error(request, "Le nom d'utilisateur doit comporter entre 5 et 10 caractères.")
            return redirect('register')
        if not username.isalnum():
            messages.error(request, "Le nom d'utilisateur doit être alphanumérique.")
            return redirect('register')
        if password != confirmpwd:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return redirect('register')
          # Création de l'utilisateur
        my_user = User.objects.create_user(username=username, email=email, password=password)
        my_user.is_active = False
        my_user.save()
        messages.success(request, "Compte créé. Un email de confirmation vous a été envoyé.")
          # Envoi de l’email de bienvenue
        subject = "Bienvenue sur EmploieDev"
        message = f"Bienvenue {my_user.username}, merci de vous être inscrit. Veuillez confirmer votre adresse email."
        send_mail(subject, message, settings.EMAIL_HOST_USER, [my_user.email], fail_silently=False)
          # Envoi de l’email de confirmation avec lien d’activation
        current_site = get_current_site(request)
        email_subject = "Confirmation de votre compte - EmploieDev"
        messageConfirm = render_to_string("emailConfirmation.html", {
            'name': my_user.username,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(my_user.pk)),
            'token': generateToken.make_token(my_user)
        })
        email = EmailMessage(
            email_subject,
            messageConfirm,
            settings.EMAIL_HOST_USER,
            [my_user.email]
        )
        email.send(fail_silently=False)
        return redirect('login')
    return render(request, 'accounts/register.html')


# Connexion
def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            my_user = User.objects.get(email=email)
            username = my_user.username
        except User.DoesNotExist:
            messages.error(request, "Utilisateur introuvable.")
            return redirect('login')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                auth_login(request, user)
                messages.success(request, f"Bienvenue {user.username} !")
                return redirect('home')
            else:
                messages.error(request, "Veuillez d'abord confirmer votre email.")
                return redirect('login')
        else:
            messages.error(request, "Email ou mot de passe incorrect.")
            return redirect('login')

    return render(request, 'accounts/login.html')

# Vue de confirmation de déconnexion
def confirm_logout(request):
    return render(request, 'accounts/confirm_logout.html')

# Déconnexion
def logout(request):
    auth_logout(request)
    messages.success(request, "Vous êtes maintenant déconnecter.")
    return redirect('home')


# Activation du compte par lien email
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        my_user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        my_user = None

    if my_user is not None and generateToken.check_token(my_user, token):
        my_user.is_active = True
        my_user.save()
        messages.success(request, "Votre compte a été activé avec succès. Connectez-vous maintenant.")
        return redirect('login')
    else:
        messages.error(request, "Échec de l'activation. Lien invalide ou expiré.")
        return redirect('home')
