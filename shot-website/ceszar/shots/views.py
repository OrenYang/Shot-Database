from django.shortcuts import render
from .models import Shot, Gas
from django.views import generic
from .FilterSet import ShotFilter


def home(request):
    return render(request,
                  "shots/home.html",
                  context={}
                  )

class ShotDetailView(generic.DetailView):
    model = Shot

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shot = self.object

        # Get the filter from the query parameters
        shot_filter = ShotFilter(self.request.GET, queryset=Shot.objects.all())
        filtered_qs = list(dict.fromkeys(shot_filter.qs))  # Convert to list for easier index manipulation

        shot_index = filtered_qs.index(shot)
        previous_shot = filtered_qs[shot_index - 1] if shot_index > 0 else filtered_qs[-1]
        next_shot = filtered_qs[shot_index + 1] if shot_index < len(filtered_qs) - 1 else filtered_qs[0]

        context['previous_shot'] = previous_shot
        context['next_shot'] = next_shot
        context['filter'] = shot_filter

        # Preserve filter parameters in URLs
        context['previous_url'] = f"{previous_shot.get_absolute_url()}?{self.request.GET.urlencode()}"
        context['next_url'] = f"{next_shot.get_absolute_url()}?{self.request.GET.urlencode()}"

        return context


class ShotSummary(generic.DetailView):
    model = Shot
    template_name = 'shots/summary_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shot = self.object

        # Get the filter from the query parameters
        shot_filter = ShotFilter(self.request.GET, queryset=Shot.objects.all())
        filtered_qs = list(dict.fromkeys(shot_filter.qs))  # Convert to list for easier index manipulation

        shot_index = filtered_qs.index(shot)
        previous_shot = filtered_qs[shot_index - 1] if shot_index > 0 else filtered_qs[-1]
        next_shot = filtered_qs[shot_index + 1] if shot_index < len(filtered_qs) - 1 else filtered_qs[0]

        context['previous_shot'] = previous_shot
        context['next_shot'] = next_shot
        context['filter'] = shot_filter

        # Preserve filter parameters in URLs
        context['previous_url'] = f"{previous_shot.get_summary_url()}?{self.request.GET.urlencode()}"
        context['next_url'] = f"{next_shot.get_summary_url()}?{self.request.GET.urlencode()}"

        return context


def shot_list(request):
    f = ShotFilter(request.GET, queryset=Shot.objects.all())
    return render(request, 'shots/filtered_list.html', {'filter': f})
