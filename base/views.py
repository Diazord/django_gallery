from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, Http404

from django.contrib import messages

from .models import ImageModel
from .forms import ImageForm, MyUserCreationForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import os

# ! TODO: Get rid of unique_name variable


def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password is incorrect')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def registerUser(request):
    form = MyUserCreationForm()
    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Something went wrong during registration')
    return render(request, 'base/login_register.html', {'form': form})


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('home')


def home(request):
    images = ImageModel.objects.all()
    context = {'images': images}
    return render(request, 'base/home.html', context)

# ! TODO: file extension checking


@login_required(login_url='login')
def addImage(request):
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        ImageModel.objects.create(
            host=request.user,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            image=request.FILES.get('image'),
            image_flag=True,
        )
        return redirect('home')
    else:
        form = ImageForm()
    context = {'form': form}
    return render(request, 'base/add_image_page.html', context)


def viewImage(request, unique_name):
    image = get_object_or_404(ImageModel, unique_name=unique_name)
    context = {'image': image}
    return render(request, 'base/view_image_page.html', context)


def editImage(request, unique_name):
    image = get_object_or_404(ImageModel, unique_name=unique_name)
    form = ImageForm(instance=image)

    if request.user != image.host:
        return HttpResponse("You're not allowed here !")

    # updating image info
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            if 'image' in request.FILES:
                image.image_flag = True
                os.remove(
                    f'./media/images/user_{image.host.id}/{image.unique_name}')

            image.image = form.cleaned_data['image']
            image.title = form.cleaned_data['title']
            image.description = form.cleaned_data['description']
            image.save()

            return redirect('view-image', image.unique_name)

    context = {'form': form}
    return render(request, 'base/edit_image_page.html', context)


@login_required(login_url='login')
def deleteImage(request, unique_name):
    image = ImageModel.objects.get(unique_name=unique_name)

    if request.user != image.host:
        return redirect('home')
    else:
        if request.method == "POST":

            image.delete()
            return redirect('home')

    return render(request, 'base/delete_image.html', {'image': image})
