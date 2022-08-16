from django.db import models


# Create your models here.
class Department(models.Model):
    title = models.CharField(verbose_name="标题", max_length=32)


class UserInfo(models.Model):
    name = models.CharField(verbose_name="姓名", max_length=16)
    password = models.CharField(verbose_name="密码", max_length=32)
    age = models.IntegerField(verbose_name="年龄")
    account = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2, default=0)
    create_time = models.DateTimeField(verbose_name="入职时间")

    depart = models.ForeignKey(to="Department", to_field="id", on_delete=models.CASCADE)

    gender_choice = (
        (1, '男'),
        (2, '女')
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choice)
