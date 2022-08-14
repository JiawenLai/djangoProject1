from django.shortcuts import render, redirect
from app01 import models


# Create your views here.
def depart_list(request):

    queryset = models.Department.objects.all()

    return render(request, 'department_list.html', {"queryset": queryset})


def depart_add(request):
    if request.method == "GET":
        return render(request, 'department_add.html')

    title = request.POST.get("title")
    models.Department.objects.create(title=title)
    return redirect("/depart/list/")


def depart_delete(request):
    nid = request.GET.get("nid")
    models.Department.objects.filter(id=nid).delete()
    return redirect("/depart/list/")


def depart_edit(request, nid):
    if request.method == "GET":
        row_obj = models.Department.objects.filter(id=nid).first()
        return render(request, 'department_edit.html', {"row_obj": row_obj})

    title = request.POST.get("title")
    models.Department.objects.filter(id=nid).update(title=title)
    return redirect("/depart/list/")


