from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required

from django.shortcuts import redirect, render
from . import forms
from . import models

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Ticket
from .models import Review
from .forms import TicketForm
from .forms import ReviewForm


@login_required
def home(request):
    tickets = models.Ticket.objects.all()
    reviews = models.Review.objects.all()
    return render(request, 'reviews/home.html', context={'tickets': tickets, 'reviews':reviews})

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

@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)  # Vérifie que l'utilisateur est bien le propriétaire
    if request.method == "POST":
        ticket.delete()
        return redirect('home')  # Redirige vers la page d'accueil après suppression

    return render(request, 'reviews/delete-ticket.html', {'ticket': ticket})



@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)  # Vérifie que c'est son ticket
    if request.method == "POST":
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirige après modification
    else:
        form = TicketForm(instance=ticket)

    return render(request, 'reviews/edit-ticket.html', {'form': form, 'ticket': ticket})



def flux(request):
    pass

def posts(request):
    pass

def abonnements(request):
    pass

def logout_view(request):
    pass


@login_required
def review_post(request):
    ticket_id = request.GET.get('ticket_id')  # Récupère l'ID du ticket
    if ticket_id:
        ticket = get_object_or_404(Ticket, id=ticket_id)
    else:
        ticket = None
    form = forms.ReviewForm()
    if request.method == 'POST':
        form = forms.ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            # set the uploader to the user before saving the model
            review.user = request.user
            review.ticket = ticket
            # now we can save
            review.save()
            return redirect('home')
    return render(request, 'reviews/review-post.html', context={'form': form})

@login_required
def review_delete(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)  # Vérifie que l'utilisateur est bien le propriétaire
    if request.method == "POST":
        review.delete()
        return redirect('home')  # Redirige vers la page d'accueil après suppression

    return render(request, 'reviews/review-delete.html', {'review': review})






@login_required
def review_edit(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)  # Vérifie que c'est son ticket
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirige après modification
    else:
        form = ReviewForm(instance=review)

    return render(request, 'reviews/review-edit.html', {'form': form, 'review': review})
