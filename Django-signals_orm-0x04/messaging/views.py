from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect, render

@login_required
def delete_user(request):
    if request.method == "POST":
        user = request.user
        logout(request)
        user.delete()  # Ensure the user is deleted
        return redirect('home')  # Replace 'home' with your homepage URL name
    return