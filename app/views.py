from django.shortcuts import render, redirect
from django.views.generic import View
from .models import Post
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class IndexView(View):
    def get(self, request, *args, **kwargs):
        # Postモデルからデータを取得
        # orderobyで(id順に)並び替え
        post_data = Post.objects.order_by('-id')
        # 指定したテンプレートにデータを流す
        return render(request, 'app/index.html', {
            'post_data': post_data
        })


# 詳細用のView
class PostDetailView(View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        return render(request, 'app/post_detail.html', {
            'post_data': post_data
        })


# 投稿用のView
# LoginRequiredMixinを継承することでログインが必須となる
class CreatePostView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # 新しいPostFotmインスタンスを生成
        form = PostForm(request.POST or None)
        return render(request, 'app/post_form.html', {
            'form': form
        })

    # ボタンを押したときにcallされる
    def post(self, request, *args, **kwargs):
        # 新しいPostFotmインスタンスを生成
        form = PostForm(request.POST or None)

        # 正しい入力なら実行
        if form.is_valid():
            # 新しいPostインスタンスを生成
            post_data = Post()
            # post_data.authorにログインユーザーを代入
            post_data.author = request.user
            # form.cleaned_dataでフォームの内容を取得できる
            post_data.title = form.cleaned_data['title']
            post_data.content = form.cleaned_data['content']
            if request.FILES:
                post_data.image = request.FILES.get('image')
            # save()でデータベースに保存
            post_data.save()
            # 詳細画面にリダイレクトする
            return redirect('post_detail', post_data.id)

        # フォームに誤りがあった場合はフォームに戻る
        return render(request, 'app/post_form.html', {
            'form': form
        })


# 編集用のView
class PostEditView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        form = PostForm(
            request.POST or None,
            initial={
                'title': post_data.title,
                'content': post_data.content,
                'image': post_data.image
            }
        )
        return render(request, 'app/post_form.html', {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        # 新しいPostFotmインスタンスを生成
        form = PostForm(request.POST or None)

        # 正しい入力なら実行
        if form.is_valid():
            # 新しいPostインスタンスを生成
            post_data = Post.objects.get(id=self.kwargs['pk'])
            # post_data.authorにログインユーザーを代入
            post_data.author = request.user
            # form.cleaned_dataでフォームの内容を取得できる
            post_data.title = form.cleaned_data['title']
            post_data.content = form.cleaned_data['content']
            if request.FILES:
                post_data.image = request.FILES.get('image')
            # print(post_data.image)
            # save()でデータベースに保存
            post_data.save()
            # 詳細画面にリダイレクトする
            return redirect('post_detail', post_data.id)

        # フォームに誤りがあった場合はフォームに戻る
        return render(request, 'app/post_form.html', {
            'form': form
        })


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        return render(request, 'app/post_delete.html', {
            'post_data': post_data
        })

    def post(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        post_data.delete()
        return redirect('index')
