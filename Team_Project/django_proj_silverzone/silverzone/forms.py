from django import forms
from silverzone.models import Qna, Review


class QnaForm(forms.ModelForm):
    class Meta:
        model = Qna
        # 유저로부터 입력받을 필드들의 이름을 나열
        fields = ["title", "email", "content", "image"]


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["message"]
