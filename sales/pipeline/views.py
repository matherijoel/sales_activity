from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, LoginForm, CreateRecordForm, UpdateRecordForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .models import Record
from django.contrib import messages

# - Homepage 
def home(request):
    return render(request, 'pipeline/index.html')

# - Register a user
def register(request):
    form = UserRegisterForm()
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['username']
            user.save()
            messages.success(request, "Account Created successfully!")
            return redirect("my-login")
    else:
        form = UserRegisterForm()
        context = {'form':form}
    return render(request, 'pipeline/register.html', context=context)

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'pipeline/profile.html', context=context)

# - Login a user
def my_login(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect("dashboard")
    context = {'form':form}
    return render(request, 'pipeline/my-login.html', context=context)

# - Dashboard
@login_required(login_url='my-login')
def dashboard(request):
    my_records = Record.objects.all()
    context = {'records': my_records}
    return render(request, 'pipeline/dashboard.html', context=context)

# - Create a record 
@login_required(login_url='my-login')
def create_record(request):
    if request.method == "POST":
        form = CreateRecordForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Record Created Successfully!")
            return redirect("dashboard")
    else:
        form = CreateRecordForm(user=request.user)
    context = {'form': form}
    return render(request, 'pipeline/create-record.html', context=context)

# - Update a record 
@login_required(login_url='my-login')
def update_record(request, pk):
    record = Record.objects.get(id=pk)
    form = UpdateRecordForm(instance=record)
    if request.method == 'POST':
        form = UpdateRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record Updated Successfully!")
            return redirect("dashboard")       
    context = {'form':form}
    return render(request, 'pipeline/update-record.html', context=context)

# - Read / View a singular record
@login_required(login_url='my-login')
def singular_record(request, pk):
    all_records = Record.objects.get(id=pk)
    context = {'record':all_records}
    return render(request, 'pipeline/view-record.html', context=context)

# - Delete a record
@login_required(login_url='my-login')
def delete_record(request, pk):
    record = Record.objects.get(id=pk)
    record.delete()
    messages.success(request, "You have just Deleted a Record!")
    return redirect("dashboard")

# - User logout
def user_logout(request):
    auth.logout(request)
    messages.success(request, "Logout success!")
    return redirect("my-login")
