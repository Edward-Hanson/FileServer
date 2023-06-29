from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views import View
from .models import FilesAdmin
import os
from django.db.models import Q
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

from .forms import EmailForm,UploadForm
from django.shortcuts import redirect
from django.contrib import messages

# Create your views here.
@login_required
def listfiles(request):
    files = FilesAdmin.objects.all()
    return render(request,'list.html',{'files':files})

@login_required
def detailfile(request,pk):
    file= get_object_or_404(FilesAdmin,pk=pk)
    return render(request,'detail.html',{'file':file})

@login_required
def download(request, file_id):
    file_obj = get_object_or_404(FilesAdmin, pk=file_id)
    file_obj.downloadcount += 1
    file_obj.save()
    return redirect(file_obj.adminupload.url)
    
@login_required   
def query_set(request):
    query = request.GET.get('q')
    if query is None:
        return
    results = FilesAdmin.objects.filter(Q(title__icontains=query)  | Q(description__icontains= query))
    return render(request,'search_results.html',{'results': results})

@staff_member_required
@login_required
def upload(request):
    if request.method=="POST":
        form= UploadForm(request.POST,request.FILES)
        if form.is_valid():
            file = form.save()
            messages.info(request,"Upload Success")
            return redirect('detail', pk=file.pk)
    else:
        form= UploadForm()
    return render(request,'upload.html',{'form':form})


@login_required 
def send_email(request, pk):
    user = request.user
    default_active_file = get_object_or_404(FilesAdmin, pk=pk)
    
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            recipient_email = form.cleaned_data['recipient_email']

            email = EmailMessage(
                subject='File Attachment',
                body='Please find the attached file',
                from_email=user.email,
                to=[recipient_email],
            )
            email.attach_file(default_active_file.adminupload.path)
            email.send()
            
            default_active_file.emailcount+=1
            default_active_file.save()

            messages.info(request, 'Email sent successfully!')
            return redirect('detail',pk=default_active_file.pk)
    else:
        form = EmailForm()

    context = {'form': form}
    return render(request, 'email_form.html', context)

