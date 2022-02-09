from rasa_sdk import Action
import requests
import json
import scraping as api
import logging
logger = logging.getLogger(__name__)

#searching movies by actor
class ActionSearchMoviesByActor(Action):

    def name(self):
        return 'action_search_movie_by_actor'

    def run(self, dispatcher, tracker, domain):
        actor = tracker.get_slot('actor_name')
        
        if (actor is None or len(actor) == 0):
            dispatcher.utter_message("Συγγνώμη, δεν γνωρίζω αυτόν/-ην τον/την ηθοποιό. Δοκίμασε κάτι άλλο.")
            return
            
        movies = api.get_movies_by_crew(actor)
        if len(movies) == 0:
            dispatcher.utter_message("Δεν βρήκα καμία ταινία με τον/την {}".format(actor))
        else: 
            dispatcher.utter_message("Ο/Η {} παίζει σε αυτές τις ταινίες:".format(actor))
            i = 1
            for movie in movies:
                dispatcher.utter_message(str(i) + ". " + movie)
                i = i+1

        return[]
        
#______________________________________________________________________        
#searching movies by director
class ActionSearchMoviesByDirector(Action):

    def name(self):
        return 'action_search_movie_by_director'

    def run(self, dispatcher, tracker, domain):
    
        director = tracker.get_slot('director_name')
        
        if (director is None or len(director) == 0):
            dispatcher.utter_message("Συγγνώμη, δεν γνωρίζω αυτόν/-ην τον/την σκηνοθέτη. Δοκίμασε κάτι άλλο.")
            return
            
        movies = api.get_movies_by_crew(director)
        if len(movies) == 0:
            dispatcher.utter_message("Δεν βρήκα καμία ταινία με σκηνοθέτη τον/την {}".format(director))
        else: 
            dispatcher.utter_message("Ρίξε μια ματιά στις ταινίες του/της {}:".format(director))
            i = 1
            for movie in movies:
                dispatcher.utter_message(str(i) + ". " + movie)
                i = i+1

        return[]
        
#______________________________________________________________________           
#searching movies by release
class ActionSearchReleaseYearForMovie(Action):

    def name(self):
        return 'action_search_release_year'

    def run(self, dispatcher, tracker, domain):
        movie_title = tracker.get_slot('movie_title')
        
        if (movie_title is None or len(movie_title) == 0):
            dispatcher.utter_message("Συγγνώμη, δεν γνωρίζω αυτήν την ταινία. Δοκίμασε κάτι άλλο.")
            return
            
        results = api.get_attributes_by_movie_title(movie_title)
        if len(results) == 0:
            dispatcher.utter_message("Δεν βρήκα καμία ταινία με τίτλο: {}".format(movie_title))
        else:
            movie = results[0]
            original_title = movie['original_title']
            release_year = movie['release_date'].split('-')[0]
            
            dispatcher.utter_message("Το {title} κυκλοφόρησε το {year}".format(title=original_title, year=release_year))
            
        return[]
      
#______________________________________________________________________         
#searching for movie plot/overview       
class ActionSearchPlotForMovie(Action):

    def name(self):
        return 'action_search_plot'
        
    def run(self, dispatcher, tracker, domain):
        movie_title = tracker.get_slot('movie_title')
        
        if (movie_title is None or len(movie_title) == 0):
            dispatcher.utter_message("Συγγνώμη, δεν γνωρίζω αυτήν την ταινία. Δοκίμασε κάτι άλλο.")
            return
        
        results = api.get_attributes_by_movie_title(movie_title)
        
        if len(results) == 0:
            dispatcher.utter_message("Δεν βρήκα καμία ταινία με τίτλο: {}".format(movie_title))
        else:
            movie = results[0]
            original_title = movie['title']
            overview = movie['overview']
            
            dispatcher.utter_message("Ρίξε μια ματιά στην πλοκή του {title}: {overview}".format(title=original_title, overview=overview))
            
        return[]

#______________________________________________________________________   
#searching for movie ratings by movie title
class ActionSearchRatingForMovie(Action):

    def name(self):
        return 'action_search_rating'
        
    def run(self, dispatcher, tracker, domain):
    
        movie_title = tracker.get_slot('movie_title')
        
        if (movie_title is None or len(movie_title) == 0):
            dispatcher.utter_message("Συγγνώμη, δεν γνωρίζω αυτήν την ταινία. Δοκίμασε κάτι άλλο.")
            return
        
        results = api.get_attributes_by_movie_title(movie_title)

        if len(results) == 0:
            dispatcher.utter_message("Δεν βρήκα καμία ταινία με τίτλο: {}".format(movie_title))
        else:
            movie = results[0]
            original_title = movie['title']
            rating = movie['vote_average']
            
            dispatcher.utter_message("Το {title} έχει βαθμολογηθεί με {rating}".format(title=original_title, rating=rating))
            
        return[]

#______________________________________________________________________   
#search popular movies by year
class ActionSearchPopularityByYear(Action):

    def name(self):
        return 'action_search_popularity_by_year'
        
    def run(self, dispatcher, tracker, domain):
        year = tracker.get_slot('release_date')
        
        if (year is None or len(year) == 0):
            dispatcher.utter_message("Συγγνώμη, δεν αναγνωρίζω αυτήν την ημερομηνία. Δοκίμασε κάτι άλλο.")
            return
            
        movies = api.get_popularity_by_year(year)
        
        dispatcher.utter_message("Αυτές είναι οι πιο δημοφιλείς ταινίες για το {}".format(year))
        
        i = 1
        for movie in movies:
            dispatcher.utter_message(str(i) + ". " + movie['title'] + ": " + str(movie['vote_average']))
            i = i + 1
            
        return[]
        
#______________________________________________________________________   
#search director for specific movie
class ActionSearchMovieDirector(Action):

    def name(self):
        return 'action_search_movie_director'
        
    def run(self, dispatcher, tracker, domain):
        movie_title = tracker.get_slot('movie_title')
        
        if (movie_title is None or len(movie_title) == 0):
            dispatcher.utter_message("Συγγνώμη, δεν γνωρίζω αυτήν την ταινία. Δοκίμασε κάτι άλλο.")
            return 
        
        results = api.get_attributes_by_movie_title(movie_title)
        crew = api.get_director_by_movie(results[0]['id'])
        
        if len(results) == 0:
            dispatcher.utter_message("Δεν βρήκα καμία ταινία με τίτλο: {}".format(movie_title))
        else:
            for member in crew:
                if (member['job'] == 'Director'):
                    dispatcher.utter_message('Το' + results[0]['title'] + ' έχει σκηνοθέτη τον/την ' + member['name'])
                    
        return[]
#______________________________________________________________________   
#search actors for specific movie
class ActionSearchMovieActors(Action):

    def name(self):
        return 'action_search_movie_actors'
        
    def run(self, dispatcher, tracker, domain):
        movie_title = tracker.get_slot('movie_title')
        
        if (movie_title is None or len(movie_title) == 0):
            dispatcher.utter_message("Συγγνώμη, δεν γνωρίζω αυτήν την ταινία. Δοκίμασε κάτι άλλο.")
            return
            
        results = api.get_attributes_by_movie_title(movie_title)
        cast = api.get_cast_by_movie(results[0]['id'])
        
        if len(results) == 0:
            dispatcher.utter_message("Δεν βρήκα καμία ταινία με τίτλο: {}".format(movie_title))
        else:
            dispatcher.utter_message("Δες τους ηθοποιούς του {}:".format(movie_title))
            i = 1
            for member in cast:
                actor = member['name']
                character = member['character']
                dispatcher.utter_message(str(i) + ". " + actor + ' ως ' + character)
                i = i + 1   
                if (i > 10):
                    break
                    
        return[]
#______________________________________________________________________   
#search similar movies
class ActionSearchSimilarMovies(Action):
    
    def name(self):
        return 'action_search_similar_movies'
        
    def run(self, dispatcher, tracker, domain):
        movie_title = tracker.get_slot('movie_title')
        
        if (movie_title is None or len(movie_title) == 0):
            dispatcher.utter_message("Συγγνώμη, δεν γνωρίζω αυτήν την ταινία. Δοκίμασε κάτι άλλο.")
            return
            
        results = api.get_attributes_by_movie_title(movie_title)
        
        similar = api.get_similar_movies(results[0]['id'])
        
        if len(results) == 0:
            dispatcher.utter_message("Δεν βρήκα καμία ταινία παρόμοια με το {}".format(movie_title))
        else:
            dispatcher.utter_message("Αν σου άρεσε το {}, μπορεί να σου αρέσουν και αυτές οι ταινίες:".format(movie_title))
            i = 1
            for member in similar:
                suggestion = member['title']
                release = member['release_date']
                dispatcher.utter_message(str(i) + ". " + suggestion + ' του ' + release)
                i = i + 1   
                if (i > 10):
                    break
                    
        return[]