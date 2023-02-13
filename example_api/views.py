from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, Http404 # JsonResponse and HttpResponseRedirect may be used in other APIs
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import ExampleModel
import json

# GET testing
@require_http_methods(['GET'])
def index(request):
    return HttpResponse("Successfully connected to the backend.")

# POST testing
@require_http_methods(['POST'])
@csrf_exempt
def post_demo(request):
    try:
        data_username = json.loads(request.body).get("username")
    except:
        raise Http404("Unknown Error")
    # Data Type: String
    if isinstance(data_username, str) == False:
        raise Http404("Illegal Data Type")
    # String Length: 1 - 50
    if len(data_username) <= 0 or len(data_username) > 50:
        raise Http404("Illegal Length")
    # No duplication
    try:
        user = ExampleModel.objects.get(username = data_username)
        return HttpResponse("Sorry, the username '%s' has already been registered." % user.username)
    except ExampleModel.DoesNotExist:
        # Write the data to the database
        data_time_created = timezone.now()
        new_user = ExampleModel.objects.create(username = data_username, time_created = data_time_created)
        return HttpResponse("Welcome, %s! You have created an account at %s." % (new_user.username, new_user.time_created))
