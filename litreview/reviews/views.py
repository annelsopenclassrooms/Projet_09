from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required

from django.shortcuts import redirect, render, get_object_or_404
from . import forms
from .models import Ticket
from .models import Review
from .models import UserFollows
from .forms import TicketForm
from .forms import ReviewForm


from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def ticket_post(request):
    form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            # set the uploader to the user before saving the model
            ticket.user = request.user
            # now we can save
            ticket.save()
            return redirect('flux')
    return render(request, 'reviews/ticket-post.html', context={'form': form})


@login_required
def ticket_delete(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)  # Vérifie que l'utilisateur est bien le propriétaire
    if request.method == "POST":
        ticket.delete()
        return redirect('flux')  # Redirige vers la page d'accueil après suppression

    return render(request, 'reviews/ticket-delete.html', {'ticket': ticket})


@login_required
def ticket_edit(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)  # Vérifie que c'est son ticket
    if request.method == "POST":
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('flux')  # Redirige après modification
    else:
        form = TicketForm(instance=ticket)

    return render(request, 'reviews/ticket-edit.html', {'form': form, 'ticket': ticket})



@login_required
def flux(request):
    user = request.user

    # Récupérer les utilisateurs suivis
    followed_users = UserFollows.objects.filter(user=user).values_list('followed_user', flat=True)

    # Récupérer les billets de l'utilisateur connecté et des utilisateurs suivis
    tickets = Ticket.objects.filter(user__in=list(followed_users) + [user])
    for ticket in tickets:
        ticket.type = "ticket"

    # Récupérer les avis de l'utilisateur connecté et des utilisateurs suivis
    reviews = Review.objects.filter(user__in=list(followed_users) + [user])
    for review in reviews:
        review.type = "review"

    # Récupérer les avis en réponse aux billets de l'utilisateur connecté
    reviews_on_my_tickets = Review.objects.filter(ticket__user=user).exclude(user=user)
    for review in reviews_on_my_tickets:
        review.type = "review"

    # Fusionner tous les objets et trier par date décroissante
    all_posts = sorted(
        list(tickets) + list(reviews) + list(reviews_on_my_tickets),
        key=lambda post: post.time_created,
        reverse=True
    )

    context = {
        "all_posts": all_posts
    }
    return render(request, "reviews/flux.html", context)


@login_required
def subscribe(request):
    user_follows = UserFollows.objects.filter(user=request.user)  # Utilisateurs que je suis
    followers = UserFollows.objects.filter(followed_user=request.user)  # Utilisateurs qui me suivent
    search_results = None  # Initialisation des résultats de recherche

    if request.method == "POST":
        if "search_user" in request.POST:  # Si la requête vient de la recherche
            query = request.POST.get("search_query", "").strip()
            if query:
                search_results = User.objects.filter(username__icontains=query).exclude(id=request.user.id)
                if not search_results.exists():
                    messages.error(request, "Aucun utilisateur trouvé.")

        elif "follow_user" in request.POST:  # Si la requête vient du bouton "Suivre"
            user_id = request.POST.get("user_id")
            followed_user = get_object_or_404(User, id=user_id)

            if UserFollows.objects.filter(user=request.user, followed_user=followed_user).exists():
                messages.warning(request, f"Vous suivez déjà {followed_user.username}.")
            else:
                UserFollows.objects.create(user=request.user, followed_user=followed_user)
                messages.success(request, f"Vous suivez maintenant {followed_user.username}.")

            return redirect("subscribe")  # Rafraîchir la page après l'ajout

    context = {
        "user_follows": user_follows,
        "followers": followers,
        "search_results": search_results
    }
    return render(request, "reviews/subscribe.html", context)


@login_required
def unfollow_user(request, user_id):
    followed_user = get_object_or_404(User, id=user_id)
    user_follow = UserFollows.objects.filter(user=request.user, followed_user=followed_user)

    if user_follow.exists():
        user_follow.delete()
        messages.success(request, f"Vous ne suivez plus {followed_user}.")
    else:
        messages.error(request, "Vous ne suivez pas cet utilisateur.")

    #return redirect("user_follows_list")  


    return redirect('subscribe')


@login_required
def remove_follower(request, follower_id):
    # Récupérer l'entrée où l'utilisateur actuel est suivi par le follower
    follow_relationship = get_object_or_404(
        UserFollows, 
        followed_user=request.user,  # L'utilisateur actuel est celui qui est suivi
        user_id=follower_id          # Le follower est celui qui suit
    )
    
    # Supprimer l'entrée dans la table UserFollows
    follow_relationship.delete()
    
    # Rediriger l'utilisateur vers une page appropriée
    return redirect('subscribe')


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
            return redirect('flux')
    return render(request, 'reviews/review-post.html', context={'form': form})

@login_required
def review_delete(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)  # Vérifie que l'utilisateur est bien le propriétaire
    if request.method == "POST":
        review.delete()
        return redirect('flux')  # Redirige vers la page d'accueil après suppression

    return render(request, 'reviews/review-delete.html', {'review': review})

@login_required
def review_edit(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)  # Vérifie que c'est son ticket
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('flux')  # Redirige après modification
    else:
        form = ReviewForm(instance=review)

    return render(request, 'reviews/review-edit.html', {'form': form, 'review': review})


@login_required
def posts(request):
    # Récupérer les tickets de l'utilisateur connecté
    user_tickets = Ticket.objects.filter(user=request.user)

    # Récupérer les critiques de l'utilisateur connecté
    user_reviews = Review.objects.filter(user=request.user)

    # Combiner les tickets et les critiques dans une seule liste
    posts = []

    for ticket in user_tickets:
        posts.append({
            'type': 'ticket',
            'object': ticket,
            'time_created': ticket.time_created,
        })

    for review in user_reviews:
        posts.append({
            'type': 'review',
            'object': review,
            'time_created': review.time_created,
        })

    # Trier la liste par date de création (du plus récent au plus ancien)
    posts.sort(key=lambda x: x['time_created'], reverse=True)

    context = {
        'posts': posts,
    }

    return render(request, 'reviews/posts.html', context)


@login_required
def create_ticket_and_review(request):
    if request.method == 'POST':
        # Créer les instances des formulaires avec les données POST et FILES
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)

        if ticket_form.is_valid() and review_form.is_valid():
            # Sauvegarder le ticket
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            # Sauvegarder la critique associée au ticket
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()

            return redirect('flux')  # Rediriger vers la page d'accueil après création
    else:
        # Afficher les formulaires vides pour une requête GET
        ticket_form = TicketForm()
        review_form = ReviewForm()

    # Passer les deux formulaires au template
    context = {
        'ticket_form': ticket_form,
        'review_form': review_form,
    }
    return render(request, 'reviews/create_ticket_and_review.html', context)