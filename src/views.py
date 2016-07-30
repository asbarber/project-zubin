from django.shortcuts import render
from django.http import HttpResponse

def index_get(request):
	return render(request, 'index_challenge1.html')

# Performs log in action
def index_post(request):
	key1 = request.POST['key1']

	if key1 == "713760":
		return render(request, 'index_challenge2.html')

	return HttpResponseRedirect('/')


	
def index(request):
	if request.method == 'GET':
		return login_get(request)
	
	if request.method == 'POST':
		return login_post(request)
