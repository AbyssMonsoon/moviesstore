from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Petition
from .forms import PetitionForm
from django.urls import reverse

def index(request):
    petitions = Petition.objects.order_by('-created_at')
    return render(request, 'petitions/index.html', {'petitions': petitions})

def detail(request, pk):
    petition = get_object_or_404(Petition, pk=pk)
    user_voted = request.user.is_authenticated and petition.yes_votes.filter(pk=request.user.pk).exists()
    return render(request, 'petitions/detail.html', {'petition': petition, 'user_voted': user_voted})

@login_required
def new(request):
    if request.method == 'POST':
        form = PetitionForm(request.POST)
        if form.is_valid():
            petition = form.save(commit=False)
            petition.created_by = request.user
            petition.save()
            return redirect('petitions:detail', pk=petition.pk)
    else:
        form = PetitionForm()
    return render(request, 'petitions/create.html', {'form': form})

@login_required
def vote_yes(request, pk):
    petition = get_object_or_404(Petition, pk=pk)
    # only allow affirmative votes once per user
    if not petition.yes_votes.filter(pk=request.user.pk).exists():
        petition.yes_votes.add(request.user)
    # redirect back to detail
    return redirect('petitions:detail', pk=pk)
