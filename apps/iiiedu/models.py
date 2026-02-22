from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Branch(models.Model):
    """校區"""
    unit = models.CharField(max_length=255, verbose_name="單位")
    city = models.CharField(max_length=255, verbose_name="城市")
    addr = models.CharField(max_length=255, verbose_name="地址")
    md5_address = models.CharField(max_length=255)

    def __str__(self):
        return "%s %s %s" % (self.unit, self.city, self.addr)


class Tag(models.Model):
    """標籤"""
    name = models.CharField(max_length=255, verbose_name="標籤名")
    cate = models.ForeignKey("Cate", verbose_name="類別", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Cate(models.Model):
    """類別"""
    name = models.CharField(max_length=255, verbose_name="類別名")

    def __str__(self):
        return self.name


class Leng(models.Model):
    """語言"""
    name = models.CharField(max_length=255, verbose_name="語言")

    def __str__(self):
        return self.name


class Course(models.Model):
    """課程表"""
    branch = models.ForeignKey("Branch", verbose_name="分校", on_delete=models.CASCADE)
    Tag = models.ForeignKey("Tag", verbose_name="標籤", on_delete=models.CASCADE)
    series = models.ManyToManyField("Series", blank=True, verbose_name="領域")
    leng = models.ManyToManyField("Leng", blank=True, verbose_name="語言")

    class_id = models.CharField(max_length=255, verbose_name="課程代碼")
    name = models.CharField(max_length=255, verbose_name="課程")
    mongo_id = models.CharField(max_length=255)
    summary = models.TextField(verbose_name="內容")
    Price_Ownpay = models.IntegerField(verbose_name="價格")

    Training_Hours = models.IntegerField(verbose_name="時數")
    Training_StartDate = models.DateTimeField(verbose_name="訓練開始日期")
    Training_EndDate = models.DateTimeField(verbose_name="訓練結束日期")

    link = models.URLField()

    def __str__(self):
        return self.name


class Role(models.Model):
    """角色表 關聯權限"""
    name = models.CharField(max_length=32, unique=True)
    menus = models.ManyToManyField("Menu")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "角色"


class UserProfile(models.Model):
    """帳號表"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # from django.contrib.auth.models import User
    # User為Django自帶的user表 當模板使用

    name = models.CharField(max_length=32)
    roles = models.ManyToManyField("Role", blank=True)

    def __str__(self):
        return self.name


class Favorite(models.Model):
    """課程收藏"""
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    # user = models.ForeignKey('UserProfile')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "收藏"


class Reply(models.Model):
    """課程留言"""
    content = models.TextField()
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    # user = models.ForeignKey('UserProfile')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "留言"


class Menu(models.Model):
    """菜單"""
    name = models.CharField(max_length=32)
    url_name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Theme(models.Model):
    """主題"""
    name = models.CharField(max_length=256)
    en = models.CharField(max_length=256, null=True)

    def __str__(self):
        return self.name


class Series(models.Model):
    """系列或領域"""
    name = models.CharField(max_length=256)
    en = models.CharField(max_length=256, blank=True, default='')
    theme = models.ManyToManyField("Theme", blank=True)

    def __str__(self):
        return self.name
