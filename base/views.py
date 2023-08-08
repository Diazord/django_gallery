from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, Http404

from .models import ImageModel
from .forms import ImageForm

from django.contrib.auth.decorators import login_required
import os

from django.forms.models import model_to_dict


def home(request):
    images = ImageModel.objects.all().order_by('-created_at')
    context = {'images': images}
    return render(request, 'base/home.html', context)

# ! TODO: file extension checking


@login_required(login_url='login')
def addImage(request):
    if request.method == "POST":
        # making sure to create user folder when he try to post image
        if not os.path.exists(f'./media/images/user_{request.user.id}'):
            os.mkdir(f'./media/images/user_{request.user.id}')

        form = ImageForm(request.POST, request.FILES)
        ImageModel.objects.create(
            host=request.user,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            image=request.FILES.get('image'),
        )
        return redirect('home')
    else:
        form = ImageForm()
    context = {'form': form}
    return render(request, 'base/add_image.html', context)


def viewImage(request, unique_name):
    image = get_object_or_404(ImageModel, unique_name=unique_name)
    context = {'image': image}
    return render(request, 'base/view_image.html', context)


def editImage(request, unique_name):
    image = get_object_or_404(ImageModel, unique_name=unique_name)
    form = ImageForm(instance=image)

    if request.user != image.host:
        return HttpResponse("You're not allowed here !")

    # updating image info
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            form.save()
            if 'image' in form.changed_data:
                image.unique_name = form.cleaned_data['image']
            return redirect('view-image', image.unique_name)

    context = {'form': form}
    return render(request, 'base/edit_image.html', context)


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
