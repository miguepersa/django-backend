from django.shortcuts import render

def index(request):
    context = {
        'logo' : "templates/mailer/kurioslogo.png",
        'user' : f"{request.user.first_name} {request.user.last_name}",
        'token' : "asdasd"
    }
    return render(request, "mailer/user_reset_password.html")