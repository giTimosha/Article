from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView

from webapp.forms import ArticleForm, CommentForm
from webapp.models import Article, Comment


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Article.objects.all()
        return context


class ArticleView(TemplateView):
    template_name = 'article.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article_pk = kwargs.get('pk')
        context['article'] = get_object_or_404(Article, pk=article_pk)
        return context


class ArticleCreateView(View):
    def get(self, request, *args, **kwargs):
        form = ArticleForm()
        return render(request, 'create.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            article = Article.objects.create(
                title=form.cleaned_data['title'],
                author=form.cleaned_data['author'],
                text=form.cleaned_data['text'],
                category=form.cleaned_data['category']
            )
            return redirect('article_view', pk=article.pk)
        else:
            return render(request, 'create.html', context={'form': form})


class ArticleUpdateView(View):
    def get(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs.get('pk'))
        form = ArticleForm(data={
            'title': article.title,
            'author': article.author,
            'text': article.text,
            'category': article.category_id
        })
        return render(request, 'update.html', context={'form': form, 'article': article})

    def post(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs.get('pk'))
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            article.title = form.cleaned_data['title']
            article.author = form.cleaned_data['author']
            article.text = form.cleaned_data['text']
            article.category = form.cleaned_data['category']
            article.save()
            return redirect('article_view', pk=article.pk)
        else:
            return render(request, 'update.html', context={'form': form, 'article': article})


class ArticleDeleteView(View):
    def get(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs.get('pk'))
        return render(request, 'delete.html', context={'article': article})

    def post(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs.get('pk'))
        article.delete()
        return redirect('index')


class CommentView(TemplateView):
    template_name = 'comment_view.html'

    def get_context_data(self, **kwargs):
        article = super().get_context_data(**kwargs)
        article['comments'] = Comment.objects.all().order_by('-created_at') #сортировка надеюсь что правельная
        return article


class CommentCreateView(View):
    def get(self, request, *args, **kwargs):
        form = CommentForm()
        return render(request, 'comment_create_view.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = CommentForm(data=request.POST)
        if form.is_valid():
            Comment.objects.create(
                article=form.cleaned_data['article'], author=form.cleaned_data['author'], text=form.cleaned_data['text']
            )
            return redirect('comment_view')

        else:
            return render(request, 'comment_create_view.html', context={'form': form})


class CommentUpdateView(View):
    def get(self, request, *args, **kwargs):
        article = get_object_or_404(Comment, pk=kwargs['pk'])
        form = CommentForm(data={
            'article': article.article,
            'author': article.author,
            'text': article.text
        })
        return render(request, 'comment_update_view.html', context={'form': form, 'comment': article})

    def post(self, request, *args, **kwargs):
        article = get_object_or_404(Comment, pk=kwargs['pk'])
        form = CommentForm(data=request.POST)
        if form.is_valid():
            article.article = form.cleaned_data['article']
            article.author = form.cleaned_data['author']
            article.text = form.cleaned_data['text']
            article.save()
            return redirect('comment_view')
        else:
            return render(request, 'comment_update_view.html', context={'form': form, 'comment': article})


class CommentDeleteView(View):
    def get(self, request, *args, **kwargs):
        article = get_object_or_404(Comment, pk=kwargs['pk'])
        return render(request, 'comment_delete_view.html', context={'comment': article})

    def post(self, request, *args, **kwargs):
        article = get_object_or_404(Comment, pk=kwargs['pk'])
        article.delete()
        return redirect('comment_view')