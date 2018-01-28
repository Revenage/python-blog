from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.shortcuts import redirect

from django.http import HttpResponse, HttpRequest, JsonResponse

import requests
import json

# def dosome (resp):
#     # result = json.loads(resp)
#     return resp

# def post_list(request):
#     # get the response from the URL
#     test_url = 'http://ip.jsontest.com/?callback=showMyIP'
#     response = requests.get(test_url)
#     result = dosome(response)
#     return HttpResponse(result)

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('created_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

# Create your views here.
