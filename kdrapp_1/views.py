from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.contrib.auth import authenticate, login
from kdrapp_1.models import User_details, Task
from django.contrib.auth.models import User
from django.http import HttpResponse
from bs4 import BeautifulSoup
import requests
from django.conf import settings
from django.db.models import Q
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required



# index or homepage logic
@login_required
def content_1(request):
    template = loader.get_template('content_1.html')
    user_profile = get_object_or_404(User_details, username=request.user)

    context = {
        'user_profile': user_profile,
    }

    latest_news = []
    url = "https://www.baltictimes.com/news_latvia/"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        td_headline = None
        date = None
        title = None
        link = None
        # Headline extraction
        headlines = soup.find_all('h2', id='tbt-main-header')
        for headline in headlines:
            td_headline = headline.text.strip()

        # Date extraction
        news_day = soup.find_all("ul", class_="list-unstyled list-inline blog-info")
        news_day = soup.find("ul", class_="list-unstyled list-inline blog-info")
        date_element = news_day.find('li')
        date = date_element.get_text(strip=True)
        
        # Title and link extraction
        sou = soup.find('div', id="tbt-mobile-front")
        for h4, a in zip(sou.find_all('h4'), sou.find_all('a')):
            title = h4.text.strip()
            link = "https://www.baltictimes.com/" + a['href']

            # Append the extracted information to the latest_news list
            latest_news.append({'headline': td_headline, 'date': date, 'title': title, 'link': link})

    # Initialize user_tasks to an empty list
    user_tasks = []

    if request.method == 'GET':
        query = request.GET.get('query', '')
        # Perform the search in the database based on task_name, username, or date
        user_tasks = User_details.objects.filter(
            Q(task__task_name__icontains=query) |
            Q(task__description__icontains=query) |
            Q(username__username__icontains=query) |
            Q(start_date__icontains=query) |
            Q(end_date__icontains=query) |
            Q(contact_number__icontains=query) |
            Q(university_name__icontains=query)
        ).distinct()

    return render(request, 'content_1.html', {'request': request, 'user_tasks': user_tasks, 'query': query,
                                              'user_profile': user_profile, 'latest_news': latest_news})

#user login logic
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not (username and password):
            return render(request, 'login.html',
                          {'error_message': "Ohh oh! Need to fill in with your Friend's membership username and secret key."})
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            # Check if the user exists but the password is incorrect
            user_exists = User.objects.filter(username=username).exists()
            if user_exists:
                return render(request, 'login.html', {'error_message': 'Hi may be you entered wrong password. Think hard! Try Again!!'})
            else:
                return render(request, 'login.html', {'error_message': "Record says your are not yet member of Friend's club!!"})

    return render(request, 'login.html')


#profile photo logic
def user_photo(request, username):
    try:
        # Get the user details associated with the provided username
        user_details = User_details.objects.get(username__username=username)

        # Check if the user details have a photo
        if user_details.photo:
            # Return the user's profile photo
            return HttpResponse(user_details.photo.read(), content_type='image/jpeg')

    except User_details.DoesNotExist:
        pass  # Handle the case where the user details are not found

    # Return a default image or handle the case where the photo is not found
    default_photo_path = 'path/to/default/photo.jpg'
    default_absolute_path = settings.MEDIA_ROOT + default_photo_path

    with open(default_absolute_path, 'rb') as default_photo_file:
        return HttpResponse(default_photo_file.read(), content_type='image/jpeg')
    

#userprofile details logic    
@login_required
def profile(request):
    # Assuming you have a User_details instance for the currently logged-in user
    user_profile = get_object_or_404(User_details, username=request.user)

    context = {
        'user_profile': user_profile,
    }

    return render(request, 'profile.html', context)

from django.shortcuts import render, redirect, get_object_or_404
from .models import User_details, Task

#add task logic
def task_add_assign(request):
    # Fetch all users and tasks for dropdown options
    users = User.objects.all()
    tasks = Task.objects.all()

    if request.method == 'POST':
        if 'taskName' in request.POST and 'taskDescription' in request.POST:
            # Code to handle adding a new task
            task_name = request.POST['taskName']
            task_description = request.POST['taskDescription']
            new_task = Task.objects.create(task_name=task_name, description=task_description)
            new_task.save()
            # Redirect to the same page after adding task
            return redirect('task_add_assign')  

        elif 'assignUsername' in request.POST and 'assignTaskName' in request.POST and 'startDate' in request.POST and 'endDate' in request.POST:
            # Code to handle assigning task to a user
            assign_username = request.POST['assignUsername']
            assign_task_name = request.POST['assignTaskName']
            start_date = request.POST['startDate']
            end_date = request.POST['endDate']

            user_instance = User.objects.get(username=assign_username)
            task_instance = Task.objects.get(task_name=assign_task_name)

            user_profile = get_object_or_404(User_details, username=user_instance)
            user_profile.task = task_instance
            user_profile.start_date = start_date
            user_profile.end_date = end_date
            user_profile.save()

# Redirect to the same page after assigning task
            return redirect('task_add_assign')  

    context = {
        'users': users,
        'tasks': tasks,
    }
    return render(request, 'task_add_assign.html', context)


#logout user logic
def log_out(request):
    logout(request)
    # Redirect to the main page after logout
    return redirect('main')


def main(request):
    return render(request,'main.html')
def signup_newuser(request):
    return render(request,'signup_newuser.html')
def edit_task(request):
    return render(request,'edit_task.html')





