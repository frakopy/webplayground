from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from .models import Message, Thread
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect


# Display a thread list
@method_decorator(login_required, name='dispatch')
class ThreadList(TemplateView):
    template_name = 'messenger/thread_list.html'


# Display a thread of conversation
@method_decorator(login_required, name="dispatch")
class ThreadDetail(DetailView):
    model = Thread
    template_name = 'messenger/thread_detail.html'

    def get_object(self):
        # It will return a instance from Thread model using the pk passed as an argument in the path of the url
        obj = super().get_object()
        if self.request.user not in obj.users.all():
            raise Http404("Profile user do not exist")
        return obj


# Create and add a new message to an existing thread
def add_message(request, pk):
    json_response = {'created': False}
    if request.user.is_authenticated:
        content = request.GET.get('content', None)
        if content:
            thread = get_object_or_404(Thread, pk=pk)
            message = Message.objects.create(user=request.user, content=content)
            thread.messages.add(message)
            json_response['created'] = True
            if len(thread.messages.all()) == 1:
                json_response['first'] = True
    else:
        raise Http404("User is not authenticated")

    return JsonResponse(json_response)


# Create a new thread in order to send message to an other user
@login_required
def start_converstation(request, username):
    user_me = request.user
    user_dest = get_object_or_404(User, username=username)
    thread = Thread.objects.find_or_create(user_me, user_dest)
    return redirect(reverse_lazy('messenger:detail', args=[thread.pk]))
