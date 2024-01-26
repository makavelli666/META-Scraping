
import urllib
import facebook
import instaloader
from pymongo import MongoClient

# Configuration des tokens 
FACEBOOK_TOKEN = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
INSTAGRAM_TOKEN = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# Configuration MongoDB
MONGODB_URI = 'mongodb://localhost:27017/'
DB_NAME = 'social_media_data'
COLLECTION_NAME = 'posts'

class SocialMediaCollector:
    def __init__(self, facebook_token, instagram_token):
        # Initialisation des API
        self.facebook_graph = facebook.GraphAPI(access_token=facebook_token, version='3.1')
        self.instagram_loader = instaloader.Instaloader()

    def collect_facebook_posts(self, query, num_posts=10000): 
        # Collecte des posts Facebook en fonction d'une requête avec l'API Graph de Facebook
        results = self.facebook_graph.request('/search', {'q': query, 'type': 'post', 'limit': num_posts})
        for post in results.get('data', []):
            post_data = {
                'source': 'facebook',
                'text': post.get('message', ''),
                'image_url': post.get('full_picture', ''),
                'comments': self.facebook_graph.get_connections(post['id'], 'comments')['data']
            }
            self.store_data(post_data)



    def collect_instagram_posts(self, query, num_posts=10000): 
        try:
            # Collecte des posts Instagram en fonction d'un hashtag
            posts = self.instagram_loader.context.get_hashtag_posts(query)
            for post in posts:
                post_data = {
                    'source': 'instagram',
                    'text': post.caption,
                    'image_url': post.url,
                    'comments': [comment.text for comment in post.get_comments()]
                }
                self.store_data(post_data)

            print(f"Collected {len(posts)} Instagram posts on '{query}'.")
        except instaloader.InstaloaderException as e:
            print(f"Instagram API Error: {e}")

    def store_data(self, data):
        # Stockage des données dans MongoDB
        collection.insert_one(data)



# Exemple d'utilisation
if __name__ == "__main__":
    try:
        # Connexion à la base de données MongoDB
        mongo_client = MongoClient('mongodb://localhost:27017/')
        db = mongo_client['social_media_BD'] 
        collection =  db['collection_posts']

        # Création de l'instance du collecteur
        collector = SocialMediaCollector(FACEBOOK_TOKEN, INSTAGRAM_TOKEN)

        # Collecte des posts Facebook et Instagram pour un sujet donné
        collector.collect_facebook_posts('le décès du président Jacques Chirac', num_posts=5) #5 posts     
        collector.collect_instagram_posts('JacquesChirac', )  # par default 10000 posts

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Fermeture de la connexion à la base de données
        if 'mongo_client' in locals():
            mongo_client.close()
