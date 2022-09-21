from django.contrib.auth import logout
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage

from .algorithm import dataExtraction, defineTime, timeIndex, searchingFree, searchingBusy
from .models import faculty_details

# Create your views here.
def login(request):
    return render(request, 'main/login.html', {})

@login_required(login_url='/login')
def home(request):
    numbers = range(8, 18)
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    depts = ["Computer Science and Engineering", "Electrical and Communications Engineering", "Mechanical Engineering", "Civil Engineering", "Biotechnology Engineering", "Chemical Engineering"]
    dayIndex = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4}
    context = {'numbers': numbers, 'days': days, 'depts': depts}

    if request.method == 'POST':
        # reqDept = request.POST['department']
        reqDayIndex = dayIndex[request.POST['requested_day']]
        if 'day_sort' in request.POST.keys():
            if request.POST['day_sort'] == 'morning':
                reqTime = timeIndex([i for i in range(8, 14)])
                timeTemp = timeIndex([i for i in range(8, 14)])
            elif request.POST['day_sort'] == 'evening':
                reqTime = timeIndex([i for i in range(13, 17)])
                timeTemp = timeIndex([i for i in range(13, 17)])
            else:
                reqTime = timeIndex([i for i in range(8, 17)])
                timeTemp = timeIndex([i for i in range(8, 17)])
        else:
            reqTime = timeIndex(defineTime(request.POST))
            timeTemp = defineTime(request.POST)

        querySet = faculty_details.objects.all()
        context['day'] = request.POST['requested_day']
        context['time'] = f'{timeTemp[0]}:00 - {timeTemp[-1]}:50'

        if request.POST['use_case'] == 'free':
            context['eligibleEmps'] = searchingFree(querySet, reqDayIndex, reqTime)
            context['status'] = 'Faculty who are free'
        else:
            context['eligibleEmps'] = searchingBusy(querySet, reqDayIndex, reqTime)
            context['status'] = 'Faculty who are busy'
    
    return render(request, 'main/home.html', context)

@login_required(login_url='/login')
def fileInput(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        path = "media/"+ str(uploaded_file.name)
        dataExtraction(path)
        # fs.delete(name)
        fs.delete(uploaded_file.name)
        return HttpResponseRedirect('/')

    return render(request, 'main/fileInput.html', {})