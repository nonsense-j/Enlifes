from django.db import models
from django.contrib.auth.models import User


class Diary(models.Model):
    '''
        日记表
    '''
    cid = models.AutoField(primary_key=True, verbose_name="序号")
    title = models.CharField(max_length=20, blank=False, verbose_name="标题")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="时间")
    detail = models.TextField(verbose_name="内容")
    cdisry = models.ForeignKey(User, to_field="username", related_name="Diary", on_delete=models.SET_NULL, blank=True,
                               null=True, verbose_name="作者")

    class Meta:
        verbose_name = "日记本"
        verbose_name_plural = verbose_name
        db_table = "my_diary"

    def __str__(self):
        return "title = {} , time = {} ,detail = {} ,who = {}".format(self.title, self.create_time, self.detail,
                                                                      self.cdisry)
