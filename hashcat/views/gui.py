from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator

# Create your views here.
from django.template import loader
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from hashcat.models import CrackingTask, Hash

@require_http_methods(["GET"])
def new(request):
	template = "hashcat/new.html"
	context = {}
	return render(request, template, context)
	HttpResponse(template.render(context, request))

@require_http_methods(["GET"])
def status(request, crackTaskId):
        template = "hashcat/status.html"
        crackingTask = get_object_or_404(CrackingTask, pk=crackTaskId)
        context = {"crackingTask": crackingTask}
        return render(request, template, context)

@require_http_methods(["GET"])
def home(request):
	template = "hashcat/home.html"

	crackingTask_list = CrackingTask.objects.all().order_by('-id')
	paginator = Paginator(crackingTask_list, 10)
	page = request.GET.get('p')
	crackingTasks = paginator.get_page(page)
	context = { 'crackingTasks' : crackingTasks }
	return render(request, template, context)
