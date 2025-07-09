from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record

# Create your views here.

def home(request):
    records = Record.objects.all()  # fixed typo: 'object' -> 'objects'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate User
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login was successful")
            return redirect('home')
        else:
            messages.error(request, "There was an error logging in. Try again.")
            return redirect('home')
    else:
        return render(request, 'home.html', {'records': records})

def logout_user(request):
    logout(request)
    messages.success(request, "Successful Logout!")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "User Successfully Registered!")
            return redirect('home')
        else:
            # If the form is invalid, show the form with errors
            return render(request, 'register.html', {'form': form})
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})

def customer_record(request, pk):
    if request.user.is_authenticated:
        # Look up record
        customer_record = Record.objects.get(id=pk)  # fixed: Record.object -> record.objects
        return render(request, 'record.html', {'customer_record': customer_record})
    else:
        messages.success(request, "Login to view record")
        return redirect('home')
      
def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "record deleted")
        return redirect('home')
    else:
     messages.success(request, "login to delete record")
     return redirect('home')
 
def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            form = AddRecordForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Record Added")
                return redirect('home')
        else:
            form = AddRecordForm()

        return render(request, 'add_record.html', {'form': form})
    else:
        messages.error(request, "You must be logged in to add a record")
        return redirect('home')

def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record Updated!")  # use success for successful update
            return redirect('home')
        
        return render(request, 'update_record.html', {'form': form})  # properly aligned
    else:
        messages.error(request, "You must be logged in to update a record")
        return redirect('home')
