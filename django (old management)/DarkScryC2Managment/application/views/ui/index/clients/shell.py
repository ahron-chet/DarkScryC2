from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from models import ChatMessage

@login_required
def post_message(request):
    if request.method == 'POST':
        msg_text = request.POST.get('message')
        if msg_text:
            ChatMessage.objects.create(
                user=request.user,
                role='user',
                message=msg_text,
                client_name='Machine1'  # or whichever
            )
    # Then return a template or redirect somewhere
    return redirect('view_chat')

def view_chat(request):
    # Pull all messages (or filter by machine)
    messages = ChatMessage.objects.all().order_by('timestamp')
    return render(request, 'chat/view_chat.html', {'messages': messages})