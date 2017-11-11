from django.shortcuts import render
from ..sitters.models import Sitter


# Show Search Results page
def index(request):
    context = {
        "search_results": Sitter.objects.all().order_by('-rank')
    }
    return render(request, "search.html", context)
