from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.text import slugify

from accounts.models import UserProfile
from movies.forms import CommentForm
from movies.models import Comment, Movie, Rating
from django.shortcuts import get_object_or_404


# Create your views here.
from .forms import MovieForm

def update_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == "POST":
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movie_review_page', slug=movie.slug, movie_id=movie.id)
    else:
        form = MovieForm(instance=movie)

    return render(request, 'update_movie.html', {'form': form, 'movie': movie})

def index(request):
    movies = Movie.objects.all()
    return render(request, 'index.html', {
        'movies':movies
    }) 

# Add a movie
def add_movie(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        owner =request.user
        try:
            image = request.FILES['image']
        except MultiValueDictKeyError:
            image = None
        producer = request.POST.get('producer')
        year = request.POST.get('year')
        category = request.POST.get('category')
        description = request.POST.get('description')

        movie = Movie(
            title=title,
            slug=slugify(title),
            owner=owner,
            image=image,
            producer=producer,
            year=year,
            category=category,
            description=description
        )
        movie.save()

        rating = Rating(
            movie=movie,
            rating=float(1.00)
        )
        
        rating.save()

        return redirect('home')

    return render(request, 'add_movie.html')


@login_required(login_url='login')
def movie_review_page(request, slug, _id):
    movie = Movie.objects.get(slug=slug, id=_id)
    profile = UserProfile.objects.get(person=request.user)
    comments = Comment.objects.filter(movie=movie)

    similar = Movie.objects.filter(category=movie.category)
    similar_movies = similar.exclude(id=movie.id)

    #creating a review
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        if comment.strip() != "":
            rate = Rating(movie=movie, rating=rating)
            rate.save()

            # Create the comment
            review = Comment(
                person=request.user,
                movie=movie,
                profile=profile,
                comment=comment,
                rate=rate
            )

            review.save()
            return redirect('review', movie.slug, movie.id)

    return render(request, 'review.html', {
        'movie': movie,
        'comments': comments,
        "similar_movies": similar_movies
    })  

@login_required(login_url='login')
def update_movie(request, movie_slug, movie_id):
    movie = Movie.objects.get(slug=movie_slug, id=movie_id)
    profile = UserProfile.objects.get(person=request.user)

    if request.method == "POST":
        form =MovieForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('review', movie.slug, movie.id)
    else:
        form = MovieForm(instance=movie)


    return render(request, 'update_movie.html', {
        'form': form,
        'movie': movie,
        'profile': profile
    })

@login_required(login_url='login')
def update_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('review', comment.movie.slug, comment.movie.id)
    else:
        form = CommentForm(instance=comment)
    return render(request, "update_comment.html", {
        'form': form
    })


@login_required(login_url='login')
def delete_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if request.method == "POST":
        comment.delete()
        return redirect('review', comment.movie.slug, comment.movie.id)
    else:
        return render(request, "delete_comment.html", {
        'comment': comment
    })
