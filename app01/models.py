from django.db import models


# Create your models here.
class Department(models.Model):
    title = models.CharField(verbose_name="标题", max_length=32)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    name = models.CharField(verbose_name="姓名", max_length=16)
    password = models.CharField(verbose_name="密码", max_length=32)
    age = models.IntegerField(verbose_name="年龄")
    account = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2, default=0)
    create_time = models.DateField(verbose_name="入职时间")

    depart = models.ForeignKey(verbose_name="部门", to="Department", to_field="id", on_delete=models.CASCADE)

    gender_choice = (
        (1, '男'),
        (2, '女')
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choice)


class PrettyNum(models.Model):
    mobile = models.CharField(verbose_name="手机号", max_length=11)
    price = models.IntegerField(verbose_name="价格", default=0)
    level_choice = (
        (1, "1级"),
        (2, "2级"),
        (3, "3级"),
        (4, "4级"),
    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choice, default=1)
    status_choices = (
        (1, "已占用"),
        (2, "未占用")
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=2)



