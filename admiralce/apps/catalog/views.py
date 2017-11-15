from django.shortcuts import render, get_object_or_404
from .models import Course, Provider

from django.views import generic


class CourseListView(generic.ListView):
    model = Course

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CourseListView, self).get_context_data(**kwargs)
        # Get the blog from id and add it to the context
        context['provider_list'] = Provider.objects.all()
        return context


class CourseDetailView(generic.DetailView):
    model = Course


def view_sitter(request, slug):
    sitter = get_object_or_404(Course, url=slug)
    context = {
        'sitter': sitter
    }
    return render(request, "sitter_profile.html", context)
