from django.shortcuts import render, redirect, HttpResponse
from django.core.validators import RegexValidator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django import forms
from app01 import models
from app01.static.utils.pagination import Pagination
import random
from datetime import datetime


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


def user_list(request):
    user_set = models.UserInfo.objects.all()

    return render(request, 'user_list.html', {"user_set": user_set})


def user_add(request):
    if request.method == "GET":
        context = {
            'gender_choice': models.UserInfo.gender_choice,
            'depart_list': models.Department.objects.all()
        }
        return render(request, 'user_add.html', context)
    name = request.POST.get('name')
    password = request.POST.get('password')
    age = request.POST.get('age')
    account = request.POST.get('account')
    create_time = request.POST.get('create_time')
    gender = request.POST.get('gender')
    depart = request.POST.get('depart')

    models.UserInfo.objects.create(name=name, password=password, age=age, account=account, create_time=create_time,
                                   gender=gender, depart_id=depart)
    return redirect("/user/list/")


class UserModelForm(forms.ModelForm):

    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "age", "account", "create_time", "gender", "depart"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


def user_model_form_add(request):
    if request.method == "GET":
        form = UserModelForm()
        return render(request, 'user_model_form_add.html', {"form": form})

    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/user/list/")
    return render(request, 'user_model_form_add.html', {"form": form})


def user_edit(request, nid):
    if request.method == "GET":
        row_obj = models.UserInfo.objects.filter(id=nid).first()
        form = UserModelForm(instance=row_obj)
        return render(request, 'user_edit.html', {"form": form})

    row_obj = models.UserInfo.objects.filter(id=nid).first()
    form = UserModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    return render(request, 'user_edit.html', {"form": form})


def user_delete(request, nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')


def num_list(request):
    data_dict = {}
    value = request.GET.get('q', "")
    if value:
        data_dict["mobile__contains"] = value

    num_set = models.PrettyNum.objects.filter(**data_dict).order_by("-level")
    return render(request, 'num_list.html', {"num_list": num_set, "search_data": value})


class NumModelForm(forms.ModelForm):
    mobile = forms.CharField(
        label="?????????",
        validators=[RegexValidator(r'^1\d{10}$', '?????????????????????')]
    )

    class Meta:
        model = models.PrettyNum
        # fields = ["mobile", "price", "level", "status"]
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    # def clean_mobile(self):
    #     txt_mobile = self.cleaned_data["mobile"]
    #
    #     if len(txt_mobile) != 11:
    #         raise ValidationError("????????????")
    #     return txt_mobile
    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]

        exists = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("??????????????????")
        return txt_mobile


def num_add(request):
    if request.method == "GET":
        form = NumModelForm()
        return render(request, 'num_add.html', {"form": form})
    form = NumModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/num/list/')
    return render(request, 'num_add.html', {"form": form})


class NumModelEditForm(forms.ModelForm):
    mobile = forms.CharField(
        label="?????????",
        # disabled=True,
        validators=[RegexValidator(r'^1\d{10}$', '?????????????????????')],
    )

    class Meta:
        model = models.PrettyNum
        fields = ["mobile", "price", "level", "status"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]

        exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("??????????????????")
        return txt_mobile


def num_edit(request, nid):
    row_obj = models.PrettyNum.objects.filter(id=nid).first()
    if request.method == "GET":
        form = NumModelEditForm(instance=row_obj)
        return render(request, 'num_edit.html', {"form": form})
    form = NumModelEditForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect("/num/list/")
    return render(request, 'num_edit.html', {"form": form})


def num_delete(request, nid):
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect('/num/list/')


class LoginForm(forms.Form):
    username = forms.CharField(
        label="?????????",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=True
    )
    password = forms.CharField(
        label="?????????",
        widget=forms.PasswordInput(attrs={"class": "form-control"}, render_value=True),
        required=True
    )


def admin_login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {"form": form})
    form = LoginForm(data=request.POST)
    if form.is_valid():
        admin_obj = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_obj:
            form.add_error("password", "????????????????????????")
            return render(request, 'login.html', {'form': form})
        request.session["info"] = {"id": admin_obj.id, "name": admin_obj.username}
        return redirect('/depart/list/')
    return render(request, 'login.html', {'form': form})


def logout(request):

    request.session.clear()

    return redirect('/account/login/')


class OrderForm(forms.ModelForm):
    class Meta:
        model = models.Order
        exclude = ['oid', 'admin']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


def order_list(request):
    queryset = models.Order.objects.all().order_by('-id')
    page_obj = Pagination(request, queryset)
    form = OrderForm()

    context = {
        'form': form,
        'queryset': page_obj.page_queryset,
        'page_string': page_obj.html()
    }
    return render(request, "order_list.html", context)


@csrf_exempt
def order_add(request):
    form = OrderForm(data=request.POST)
    if form.is_valid():
        form.instance.oid = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999))
        form.instance.admin_id = request.session["info"]["id"]
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, "error": form.errors})


def order_delete(request):
    uid = request.GET.get("uid")
    exists = models.Order.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({"status": False, "error": "???????????????"})
    models.Order.objects.filter(id=uid).delete()
    return JsonResponse({"status": True})


def order_detail(request):
    uid = request.GET.get("uid")
    row_dict = models.Order.objects.filter(id=uid).values("title", "price", "status").first()
    if not row_dict:
        return JsonResponse({"status": False, "error": "??????????????????"})
    result = {
        "status": True,
        "data": row_dict
    }
    return JsonResponse(result)


@csrf_exempt
def order_edit(request):
    uid = request.GET.get("uid")
    row_obj = models.Order.objects.filter(id=uid).first()
    if not row_obj:
        return JsonResponse({"status": False, "msg": "???????????????, ??????????????????"})
    form = OrderForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, "error": form.errors})


@csrf_exempt
def upload_list(request):
    if request.method == "GET":
        return render(request, "upload_list.html")
    file_obj = request.FILES.get("avatar")
    f = open(file_obj.name, mode="wb")

    for chunk in file_obj.chunks():
        f.write(chunk)
    f.close()
    return HttpResponse("---")
