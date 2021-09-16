from django.shortcuts import render, redirect, resolve_url
from django.http.request import HttpRequest
from django.contrib.auth.decorators import login_required
from silverzone.models import Main, Qna, Review
from silverzone.forms import QnaForm, ReviewForm

# 지도 시각화를 위한 라이브러리
import pandas as pd
from folium import plugins
from folium.plugins import MousePosition
import folium
import requests
import geocoder

from django.http import JsonResponse
from django.contrib.auth.models import User

# main_page
# import geojson
g = geocoder.ip('me')
# 현재 내위치 # Create your views here.


def main_page(request):
    df= pd.read_csv('data\전국노인보호구역표준데이터_수정.csv', encoding='euc-kr')
    df_dabal= pd.read_csv('data\보행노인사고 다발지역 전지역.csv')
    df_daejeon=pd.read_csv('data\대전광역시_전통시장 현황_20190301.csv', encoding='cp949')

    map = folium.Map(location=[36.111945112955745, 127.5026647656849], zoom_start=7,
                     width='100%', height='100%',)
    for n in df.index:
        folium.Circle([df['위도'][n], df['경도'][n]], radius=300,
                      popup=str(df.iloc[n][['대상시설명']]),
                      color='#3186cc', fill_color='#3186cc').add_to(map)

    for n in df_dabal.index:
        folium.Circle([df_dabal['위도'][n], df_dabal['경도'][n]], radius=10,
                      popup=str(df_dabal.iloc[n][['장소설명']]),
                      color='brown', fill_color='brown').add_to(map)

    for n in df_daejeon.index:
        folium.Circle([df_daejeon['위도'][n], df_daejeon['경도'][n]],
                      popup=str(df_daejeon.iloc[n][['시장명']]),
                      radius=60,
                      color = 'green', fill_color='green').add_to(map)

    plugins.LocateControl().add_to(map)  # 사용자 현재위치 반환
    plugins.Geocoder().add_to(map)  # 마커 위치 표시
    MousePosition().add_to(map)

    maps = map._repr_html_()  # 지도를 템플릿에 삽입하기위해 iframe이 있는 문자열로 반환 (folium)

    return render(request, "silverzone/main_page.html", {'map': maps})


def qna_list(request: HttpRequest):
    qs = Qna.objects.all().select_related("writer")

    # QueryDict
    # QueryString 인자 : 모든 요청에 존재할 수 있어요.
    query = request.GET.get("query", "")
    if query:
        qs = qs.filter(name__icontains=query)
    # request.POST  # POST에만 존재
    # request.FILES

    return render(request, "silverzone/qna_list.html", {
        "qna_list": qs,
    })


@login_required
def qna_post(request: HttpRequest):
    if request.method == "POST":
        form = QnaForm(request.POST, request.FILES)
        if form.is_valid():
            # commit=False를 지정하면, post.save() 가 호출되지 않은
            # post 인스턴스 반환
            qna = form.save(commit=False)  # 방금 저장한 모델 객체를 반환
            # post  # 아직 post.save()가 호출되지 않은 상태.
            # post.ip = request.META["REMOTE_ADDR"]
            qna.writer = request.user
            qna.save()
            # return redirect("/journal/" + str(1) + "/")
            return redirect(f"/silverzone/main/qnas/")
    else:
        form = QnaForm()

    return render(request, "silverzone/qna_form.html", {"form": form, },)


@login_required
def qna_edit(request: HttpRequest, pk):
    qna = Qna.objects.get(pk=pk)

    if request.method == "POST":
        form = QnaForm(request.POST, request.FILES, instance=qna)
        if form.is_valid():
            form.save()
            # post = form.save(commit=False)  # 방금 저장한 모델 객체를 반환
            # post.ip = request.META["REMOTE_ADDR"]
            # post.save()
            return redirect("/silverzone/main/qnas/")
    else:
        form = QnaForm(instance=qna)

    return render(request, "silverzone/qna_form.html", {"form": form, },)



@login_required
def qna_content(request, pk):
    qna = Qna.objects.get(pk=pk)
    review_list = Review.objects.filter(question_id= pk)
    return render(request, "silverzone/qna_content.html", {
        "qna": qna ,"review_list":review_list},)

def review_list(request, qna_pk):
    # movie = Movie.objects.get(pk=movie_pk)
    # review_list = movie.review_set.all()

    review_list = Review.objects.filter(qna__pk=qna_pk)

    # python plain objects로 변환
    # JSON으로 변환하는 파이썬 기본 라이브러리인 json.dumps를 통해서 이뤄집니다.
    #  파이썬 기본 타입에 대해서만 변환 룰을 제공해줍니다.
    #  추가 타입에 대해서는? 커스텀 Rule을 지정할 수 있습니다. => json.dumps에 cls 인자를 통해 가능
    response_data = [
        {
            "message": review.message,
            "edit_url": resolve_url("review_edit", qna_pk, review.pk),
            "delete_url": resolve_url("review_delete", qna_pk, review.pk),
            "author": {
                "username": review.author.username,
            },
        }
        for review in review_list]
    return JsonResponse(response_data, safe=False, json_dumps_params={'ensure_ascii': False})

@login_required
def review_new(request, qna_pk):
    qna = Qna.objects.get(pk=qna_pk)

    if request.method == "POST":
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review: Review = form.save(commit=False)
            # 현재 로그인 유저를 author 필드에 지정
            review.author = request.user
            review.question = qna
            review.save()
            # return redirect(f"/movist/movies/{movie_pk}/")
            # return redirect("movie_detail", movie_pk)  # URL Reverse

            # return redirect(movie.get_absolute_url())
            # redirect는 인자로 받은 객체에서 get_absolute_url 속성을 지원하면
            # get_absolute_url() 을 호출하여 그 반환값을 사용합니다.
            return redirect(f"/silverzone/main/qnas/{qna_pk}")

            # return redirect("movie_detail", pk=movie_pk)  # URL Reverse
    else:  # GET
        form = ReviewForm()

    return render(request, "silverzone/review_form.html", {
        "form": form,
    })


@login_required
def review_edit(request, qna_pk, pk):
    review = Review.objects.get(pk=pk)

    if request.method == "POST":
        form = ReviewForm(request.POST, request.FILES, instance=review)
        if form.is_valid():
            review: Review = form.save()
            # return redirect(f"/movist/movies/{movie_pk}/")
            # return redirect("movie_detail", movie_pk)  # URL Reverse
            return redirect(f"/silverzone/main/qnas/{qna_pk}")
    else:  # GET
        form = ReviewForm(instance=review)

    return render(request, "silverzone/review_form.html", {
        "form": form,
    })


# GET 방식으로 요청을 받았을 때에는, 절대 삭제하지마세요.
@login_required
def review_delete(request, qna_pk, pk):
    review = Review.objects.get(pk=pk)
    if request.method == "POST":
        review.delete()
        # return redirect(f"/movist/movies/{movie_pk}/")
        # return redirect("movie_detail", movie_pk)
        return redirect(f"/silverzone/main/qnas/{qna_pk}")
    return render(request, "silverzone/review_confirm_delete.html")

# SAISS 소개


def purpose(request):
    return render(request, "silverzone/purpose.html")

# 노인사고 통계분석


def analysis(request):
    return render(request, "silverzone/analysis.html")

# 노인보호구역 순위


def rank(request):
    return render(request, "silverzone/rank.html")

# 노인보호구역 추천 지도


def recommend(request):
    market_df = pd.read_csv("data\보행노인사고_다발지역_전통시장포함300m완료_0909_v08.csv",encoding="cp949",index_col=0)

    from sklearn import cluster
    
    # 분석에 사용할 속성을 선택
    columns_list = [6,8,12,14]
    X = market_df.iloc[:, columns_list]
    
    from sklearn import preprocessing

    X = preprocessing.StandardScaler().fit(X).transform(X)

    dbm = cluster.DBSCAN(eps=2, min_samples=5)
    dbm.fit(X)

    # 예측 (군집)
    cluster_label = dbm.labels_
    # 예측 결과를 데이터프레임에 추가
    market_df['Cluster'] = cluster_label

    grouped_cols = [0, 1,5] + columns_list
    grouped = market_df.groupby('Cluster')
    
    colors = {-1:'black', 0:'yellow', 1:'red', 2:'green', 3:'blue', 4:'blue', 5:'navy', 6:'purple', 7:'gray', 8:'gray', 9:'gray', 10:'gray', 11:'gray',12:'gray' ,13:'gray',15:'gray'}
    cluster_map = folium.Map(location=[36.35812161961745, 127.40060959359286],zoom_start=12, width='100%', height='100%')
    
    for name, lat, lng, clus, acc, dead in zip(market_df.장소설명, market_df.위도, market_df.경도, market_df.Cluster, market_df.사고건수, market_df.사망자수):  
        folium.CircleMarker([lat, lng],
        radius=10,                   # 원의 반지름
        color=colors[clus],         # 원의 둘레 색상
        fill=True,
        fill_color=colors[clus],    # 원을 채우는 색
        fill_opacity=0.5,           # 투명도    
        popup=name,tooltip=[acc,dead]
        ).add_to(cluster_map)
    cluster_map

    plugins.LocateControl().add_to(cluster_map)  # 사용자 현재위치 반환
    plugins.Geocoder().add_to(cluster_map)  # 마커 위치 표시
    MousePosition().add_to(cluster_map)

    cluster_maps = cluster_map._repr_html_()  # 지도를 템플릿에 삽입하기위해 iframe이 있는 문자열로 반환 (folium)

    return render(request, "silverzone/recommend.html", {'cluster_map': cluster_maps})
