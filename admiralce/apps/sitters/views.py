from django.shortcuts import render, get_object_or_404
from .models import Sitter


def view_sitter(request, slug):
    sitter = get_object_or_404(Sitter, url=slug)
    context = {
        'sitter': sitter
    }
    return render(request, "sitter_profile.html", context)
