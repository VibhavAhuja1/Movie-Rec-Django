from django.shortcuts import render
import pickle
import pandas as pd

movies_dict = pickle.load(open('recommendations/movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('recommendations/similarity.pkl', 'rb'))

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies

def dissimilar(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), key=lambda x: x[1])[:5]  
    dissimilar_movies = []
    for i in movies_list:
        dissimilar_movies.append(movies.iloc[i[0]].title)
    return dissimilar_movies

def home(request):
    recommendations = []
    dissimilar_movies_list = []
    
    if request.method == 'POST':
        selected_movie = request.POST.get('selected_movie')
        
        if 'recommend' in request.POST:
            recommendations = recommend(selected_movie)
        elif 'dissimilar' in request.POST:
            dissimilar_movies_list = dissimilar(selected_movie)

        return render(request, 'home.html', {
            'selected_movie': selected_movie,
            'recommendations': recommendations,
            'dissimilar_movies': dissimilar_movies_list,
            'movies': movies['title'].values
        })

    return render(request, 'home.html', {'movies': movies['title'].values})
