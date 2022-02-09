import requests
import json

key = '5f87778051207f894f1eb5294e26c6c5'
api = 'https://api.themoviedb.org/3/'


#%%
#defining subject entity search queries

#popular movies
def get_popularity_by_year(year):
    url = api + 'discover/movie'
    #parameter specification
    params = {'api_key': key, 'sort_by' : 'popularity.desc', 'include_adult' : 'false', 'primary_release_year' : year}   
    #perform request
    response = requests.get(url, params = params).text   
    response_json = json.loads(response)
    results = response_json['results']
    return results

def parse_movies_with(json_data, person):
    movies = []
    for results in json_data:
        if results['media_type'] == 'person':
            known_for = results['known_for']
            for movie in known_for:
                title = movie['title']
                movies.append(title)
    return movies   
    
#get known movies by crew person (example: actor/ director)
def get_movies_by_crew(query):
    url = api + 'search/multi'    
    params = {'api_key': key, 'query' : query, 'include_adult' : 'false'}      
    response = requests.get(url, params = params).text    
    response_json = json.loads(response)    
    results = response_json['results']    
    movies = parse_movies_with(results, query)   
    return movies
  
#get credits by movie title (example: who directed?)
def get_director_by_movie(query):
    url = api + 'movie/{}/credits'.format(query)   
    params = {'api_key': key}  
    response = requests.get(url, params = params).text
    response_json = json.loads(response)
    crew = response_json['crew']   
    return crew   
    
#get cast by movie title (example: who acted in movie?)
def get_cast_by_movie(query):
    url = api + 'movie/{}/credits'.format(query)    
    params = {'api_key': key}      
    response = requests.get(url, params = params).text   
    response_json = json.loads(response)   
    cast = response_json['cast']   
    return cast  
    
#get movie attributes by movie_title (example: rating/release_year)
def get_attributes_by_movie_title(query):
    url = api + 'search/movie'   
    params = {'api_key': key, 'query' : query, 'include_adult' : 'false'}   
    response = requests.get(url, params = params).text   
    response_json = json.loads(response)    
    if (response_json.get('results') == None):
        print("Error requesting attributes for query")
        return None    
    results = response_json['results']    
    return results

#finds movies similar to inputted title
def get_similar_movies(query):
    url = api + 'movie/{}/similar'.format(query)   
    params = {'api_key': key}     
    response = requests.get(url, params = params).text    
    response_json = json.loads(response)    
    if (response_json.get('results') == None):
        print("Error requesting attributes for query")
        return None       
    results = response_json['results']    
    return results

