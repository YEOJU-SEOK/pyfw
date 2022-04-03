from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from djangogram.users.models import User as user_model

from . import models, serializers
from .forms import CreatePostForm
# Create your views here.

# db에서 포스트만 추출
    # post시리얼라이저 호출
    # return render(request, 'posts/main.html')

def index(request):
    if request.method == "GET":
        user = get_object_or_404(user_model, pk=request.user.id)
        following = user.following.all()
        posts = models.Post.objects.filter(Q(author__in=following) | Q(author=user))

        serializer = serializers.PostSerializer(posts, many=True)

        return render(request, 'posts/main.html', {'posts': serializer.data})
    #로그인을 한 포스트 + 팔로잉을 한 유저의 포스트가 같이 나

def post_create(request):
    # 사용자가 페이지를 요청하는 get
    if request.method == "GET":
        form = CreatePostForm()
        return render(request, 'posts/post_create.html', {"form": form})
    elif request.method == "POST":

        # 로그인한 유저의 경우
        if request.user.is_authenticated:
            user = get_object_or_404(user_model, pk=request.user.id)
            # # 파일데이터의 경우 files, 일반 데이터의 경우 post
            # image = request.FILES['image']
            # caption = request.POST['caption']
            #
            # new_post = models.Post.objects.create(author=user, image=image, caption=caption)
            # new_post.save()
            form = CreatePostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = user
                post.save()
            else:
                print(form.errors)

            return render(request, 'posts/main.html')
        else:
            return render(request, 'users/main.html')

