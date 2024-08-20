import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_instagram_data(url):
    """Récupère les données d'une publication Instagram à partir de son URL.

    Args:
        url (str): L'URL de la publication Instagram.

    Returns:
        dict: Un dictionnaire contenant les données récupérées (likes, commentaires, hashtags).
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Adapter les sélecteurs CSS en fonction de la structure de la page Instagram
    likes = soup.find('meta', property='og:like_count')['content']
    comments = soup.find('meta', property='og:comment_count')['content']
    hashtags = [hashtag['content'] for hashtag in soup.find_all('meta', property='al:tag')]

    return {'likes': likes, 'comments': comments, 'hashtags': hashtags}

def select_winner(participants, min_likes, required_hashtags):
    """Sélectionne un gagnant parmi les participants en fonction des critères.

    Args:
        participants (list): Une liste de dictionnaires représentant les participants.
        min_likes (int): Le nombre minimum de likes requis.
        required_hashtags (list): La liste des hashtags requis.

    Returns:
        dict: Le gagnant, ou None si aucun participant ne correspond aux critères.
    """
    candidates = [participant for participant in participants
                  if participant['likes'] >= min_likes
                  and all(hashtag in participant['hashtags'] for hashtag in required_hashtags)]

    if candidates:
        winner = random.choice(candidates)
        return winner
    else:
        return None

# Charger les données des participants (à remplacer par votre chargement réel)
participants_data = pd.read_csv("participants.csv")

# Créer l'interface Streamlit
st.title("Sélecteur de gagnants Instagram")

# Champ pour saisir l'URL
post_url = st.text_input("URL de la publication Instagram")

if st.button("Récupérer les données et sélectionner un gagnant"):
    if post_url:
        data = get_instagram_data(post_url)
        # Mettre à jour les données des participants avec les nouveaux critères
        participants_data['hashtags'] = data['hashtags']

        # Paramètres de sélection
        min_likes = st.number_input("Nombre minimum de likes", min_value=0)
        required_hashtags = st.text_input("Hashtags requis (séparés par des virgules)", value="#concours").split(",")

        # Sélectionner le gagnant
        winner = select_winner(participants_data.to_dict('records'), min_likes, required_hashtags)

        if winner:
            st.success(f"Le gagnant est : {winner['nom']}")
        else:
            st.error("Aucun participant ne correspond aux critères.")
