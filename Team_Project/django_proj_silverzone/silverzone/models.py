from django.db import models
from django.contrib.auth.models import User


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Main(TimestampedModel):
    pass


class Qna(TimestampedModel):
    title = models.CharField(max_length=100, verbose_name="제목")
    writer = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="글 작성자")
    email = models.CharField(max_length=100, verbose_name="이메일")
    image = models.ImageField(verbose_name="첨부 이미지")
    content = models.TextField(verbose_name="내용")

    def __str__(self) -> str:
        return self.writer


class Review(TimestampedModel):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="리뷰 작성자")
    question = models.ForeignKey(
        Qna, on_delete=models.CASCADE, verbose_name="질문")
    message = models.TextField(verbose_name="건의내용")

    def __str__(self) -> str:
        return self.author
