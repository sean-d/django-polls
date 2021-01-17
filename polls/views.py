from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "five_most_recent"

    def get_queryset(self):
        thing = Question.objects.order_by("-pub_date")[:5]
        return thing[::-1]


class DetailsView(generic.DetailView):
    model = Question
    template_name = "polls/details.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/details.html",
            {"question": question, "error_message": "You did not make a choice."},
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
    return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"
