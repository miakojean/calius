from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from django.conf import settings
from django.http import JsonResponse

def scrape_city(request):
    if request.method == 'POST':
        # Récupérer le nom de la ville du formulaire
        city = request.POST.get('city')
        url = f'https://fr.wikipedia.org/wiki/{city}'

        # Effectuer la requête vers Wikipedia
        response = requests.get(url)
        if response.status_code != 200:
            return render(request, 'scraper/city_scrape.html', {'error': f'Page Wikipedia pour "{city}" introuvable.'})

        soup = BeautifulSoup(response.content, 'html.parser')

        # Extraire le titre de la page
        title = soup.find('h1', id='firstHeading').text

        # Extraire la première image
        infobox = soup.find('table', class_='infobox')
        image_url = None
        if infobox:
            image = infobox.find('img')
            if image:
                image_url = 'https:' + image['src']

        # Passer les données au template
        return render(request, 'scraper/scrape.html', {
            'title': title,
            'image_url': image_url
        })

    # Afficher le formulaire si c'est une requête GET
    return render(request, 'scraper/scrapesearch.html')


def search_facebook_ads(request):
    query = request.GET.get('query', '')  # Récupérer le terme de recherche de l'utilisateur
    ads = []

    if query:
        # URL de l'API Facebook Ads Library
        url = "https://graph.facebook.com/v17.0/ads_archive"
        params = {
            'search_terms': query,
            'ad_type': 'POLITICAL_AND_ISSUE_ADS',
            'access_token': settings.META_ACCESS_TOKEN,
            'limit': 10
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            ads = data.get('data', [])
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de l'appel à l'API Facebook : {e}")

    # Rendre le template avec les résultats
    return render(request, 'search.html', {'ads': ads, 'query': query})