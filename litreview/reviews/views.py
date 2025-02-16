from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required

from django.shortcuts import redirect, render
from . import forms
from . import models

@login_required

def home(request):
    tickets = models.Ticket.objects.all()
    return render(request, 'reviews/home.html', context={'tickets': tickets})




@login_required
def post_ticket(request):
    form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            # set the uploader to the user before saving the model
            ticket.user = request.user
            # now we can save
            ticket.save()
            return redirect('home')
    return render(request, 'reviews/post-ticket.html', context={'form': form})



def flux(request):
    pass

def posts(request):
    pass

def abonnements(request):
    pass

def logout_view(request):
    pass