from django.shortcuts import get_object_or_404,render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Choice, Question
from django.urls import reverse
from django.views import generic
from django.utils import timezone
# Create your views here.
class IndexView(generic.ListView):
    template_name='polls/index.html'
    context_object_name='latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model=Question
    template_name='polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

#def index(request):
#    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    #template = loader.get_template('polls/index.html')
    #output = ', '.join([q.question_text for q in lastest_question_list])
#    context = {'latest_question_list': latest_question_list}
    #return HttpResponse(template.render(context,request))
#    return render(request, 'polls/index.html', context)
    #return HttpResponse("Hello my friend you are in poll application!" )#+ " " + output)
#def detail(request, question_id):
    #question = get_object_or_404(Question, pk=question_id)
    #return render(request, 'polls/detail.html', {'question': question})
                                                #dicts {'k1':k2}kazdy "klucz" ma swoja wartosc czyli klucz question ma wartosci question(zmienne z pytania QUestion)
                                                # oprocz stringow mozna uzyc innego typu np 'predkosc':[30,50]
#def results(request, question_id):
    #print(request)
    #response = "You're looking at the results of question %s"
    #return HttpResponse(request)
#    question = get_object_or_404(Question, pk=question_id)
    #return HttpResponse(response % question_id)
    #return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        #Redisplay the question voting form.
        return render(request, 'polls/detail.html',{
            'question': question,
            'error_message': "You didn't select a choice",
        })
    else:
        # statements # statements that will be executed if there is no exception
        # try catch else skladnia !
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after succesfully dealing
        # with POST data. This prevents data from being posted twice if a user hits the Back  button
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
