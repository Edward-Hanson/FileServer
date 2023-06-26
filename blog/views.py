from django.shortcuts import render
from django.http import FileResponse,HttpResponse
from django.shortcuts import get_object_or_404
from django.views import View
from .models import FilesAdmin
import os
from django.db.models import Q
from django.core.mail import EmailMessage
from django.conf import settings
from .forms import EmailForm

# Create your views here.
def listfiles(request):
    files = FilesAdmin.objects.all()
    return render(request,'list.html',{'files':files})

def detailfile(request,pk):
    file= get_object_or_404(FilesAdmin,pk=pk)
    return render(request,'detail.html',{'file':file})


class Download(View):
    
    def get(self, request, file_id):
        file_obj = get_object_or_404(FilesAdmin, id=file_id)
        file_obj.downloadcount += 1
        file_obj.save()
        return file_obj.adminupload.url


def preview_file(request, file_id):
    file_obj = get_object_or_404(FilesAdmin, id=file_id)
    file_extension = os.path.splitext(file_obj.adminupload.name)[1].lower()

    if file_extension == '.pdf':
        return render(request, 'preview_pdf.html', {'file_url': file_obj.adminupload.url})
    elif file_extension in ['.jpg', '.jpeg', '.png', '.gif']:
        return render(request, 'preview_image.html', {'file_url': file_obj.adminupload.url})
    elif file_extension in ['.mp4', '.avi', '.mkv']:
        return render(request, 'preview_video.html', {'file_url': file_obj.adminupload.url})
    elif file_extension in ['.mp3', '.wav', '.ogg']:
        return render(request, 'preview_audio.html', {'file_url': file_obj.adminupload.url})
    else:
        return render(request, 'preview_unsupported.html')
    
    
def query_set(request):
    query = request.GET.get('q')
    results = FilesAdmin.objects.filter(Q(title__icontains=query)  | Q(description__icontains= query))
    return render(request,'search_results.html',{'results': results})


def send_email(request, pk):
    user = request.user
    default_active_file = get_object_or_404(FilesAdmin, pk=pk)
    
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            default_active_file.emailcount+=1
            default_active_file.save()
            recipient_email = form.cleaned_data['recipient_email']

            email = EmailMessage(
                subject='File Attachment',
                body='Please find the attached file.',
                from_email=user.email,
                to=[recipient_email],
            )

            file_path = os.path.relpath(default_active_file.adminupload.path, settings.MEDIA_ROOT)
            email.attach_file(default_active_file.adminupload.path)

            email.send()

            return HttpResponse('Email sent successfully!')
    else:
        form = EmailForm()

    context = {'form': form}
    return render(request, 'email_form.html', context)

