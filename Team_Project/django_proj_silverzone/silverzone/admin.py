from django.contrib import admin
from silverzone.models import Main, Qna, Review
from django.utils.safestring import mark_safe


@admin.register(Main)
class MainAdmin(admin.ModelAdmin):
    pass


@admin.register(Qna)
class QnaAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'writer', 'email','image', 'created_at']

    # 적절히 썸네일처리해주면, 페이지가 좀 더 빨리 뜨고, 서버 부담도 줄어든다.

    def image(self, qna: Qna):
        html = f'<img src="{qna.image.url}" style="width: 100px;" />'
        return mark_safe(html)
    image.short_description = "이미지"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['pk', 'author','message', 'created_at']
