from django.shortcuts import render,redirect
from django.http import JsonResponse
from image_manipulations.models import Image_gallery,Tags
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from PIL import Image

def tags_creation(request):
    tag_name = request.POST.get("tag")
    tag_obj = Tags.objects.get_or_create(name=tag_name)[0]
    tags = Tags.objects.all()
    return redirect("/image_upload/")

    
def image_upload(request):
    if request.method == "POST":
        image = request.FILES.getlist("Image")
        if None in image:
            return JsonResponse({'error': 'please upload image!!'})

        for i in range(len(image)):
            tags = request.POST.getlist(f"tag{i}")
            for tag in tags:
                img_obj = Image_gallery(image = image[i])
                img_name = f"image/{img_obj.image}".replace(" ","_")

                filtered_img = Image_gallery.objects.filter(image=img_name)
                tag_obj  = Tags.objects.get_or_create(name=tag)[0]

                if filtered_img:
                    filtered_img[0].tags.add(tag_obj)
                    filtered_img[0].save()
                else:
                    img_obj.save()
                    img_obj.tags.add(tag_obj)
                    img_obj.save()
        return redirect("/list_image/")
    tags = Tags.objects.all()
    return render(request,"image_upload.html",{"tag":tags})


def image_list(request,tag_name=None):
    if tag_name:
        img_obj_list = Image_gallery.objects.filter(tags__name=tag_name)
    else:
        img_obj_list = Image_gallery.objects.all()

    page = request.GET.get('page', 1)

    paginator = Paginator(img_obj_list, 8)
    try:
        img_obj = paginator.page(page)
    except PageNotAnInteger:
        img_obj = paginator.page(1)
    except EmptyPage:
        img_obj = paginator.page(paginator.num_pages)
    tags = Tags.objects.all()
    return render(request,"image_list.html",{'img_obj':img_obj,'tags':tags})

def image_details(request,id):
    try:
        img = Image_gallery.objects.get(id=id)
    except:
        img = Image_gallery.objects.all()[0]
    return render(request,"image_details.html",{"img":img})


def rotate_img(request):
    rt_degr = request.GET.get("degree", None)
    img_id = request.GET.get("rt_id", None)
    img_path = request.GET.get("rt_img", None)
    img = Image_gallery.objects.get(id=img_id).image
    img_file_name = ("").join(img_path.split("/")[3])
    im = Image.open(img)
    img_rt_90 = im.rotate(int(rt_degr))
    img_rt_90.save(f"media/image/{img_file_name}")
    return JsonResponse({'message': 'Success'})






