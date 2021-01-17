from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import Choice, Question


def index(request):
    five_most_recent = Question.objects.order_by("-pub_date")[:5]
    five_most_recent = five_most_recent[::-1]
    context_dict = {"five_most_recent": five_most_recent}
    return render(request, "polls/index.html", context=context_dict)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {"question": question, "error_message": "You did not make a choice."},
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
    return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})