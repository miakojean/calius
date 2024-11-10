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


from django.http import HttpResponse

def search_facebook_ads(request):
    query = request.GET.get('query', '')

    if not query:
        return render(request, 'search.html', {'error_message': 'Veuillez entrer un terme de recherche.'})

    url = "https://graph.facebook.com/v21.0/ads_archive"  # Mettez à jour vers v21.0
    params = {
        'search_terms': query,
        'ad_type': 'POLITICAL_AND_ISSUE_ADS',
        'access_token': settings.META_ACCESS_TOKEN,
        'fields': 'ad_creative_body,ad_delivery_start_time,ad_creative_link_title,demographic_distribution',
        'limit': 10
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        ads = data.get('data', [])

        if 'error' in data:
            error_message = data['error']['message']
            return render(request, 'search.html', {'error_message': error_message})

    except requests.exceptions.RequestException as e:
        error_message = f"Une erreur s'est produite lors de la requête : {e}"
        return render(request, 'search.html', {'error_message': error_message})

    return render(request, 'search.html', {'ads': ads, 'query': query})

def meta_test(request):
    # Remplacez par votre token d'accès
    access_token = settings.META_ACCESS_TOKEN

    # URL de l'API Meta pour obtenir les informations utilisateur
    url = "https://graph.facebook.com/v17.0/me"

    # Paramètres de la requête
    params = {
        "access_token": access_token,
        "fields": "id,name,email"  # Vous pouvez personnaliser les champs
    }

    try:
        # Envoi de la requête à l'API Meta
        response = requests.get(url, params=params)
        response.raise_for_status()

        # Récupération des données JSON
        data = response.json()
        return render(request, 'meta_test.html', {'data': data})
    except requests.exceptions.RequestException as e:
        # Gestion des erreurs
        return render(request, 'meta_test.html', {'error': str(e)})

def test_business_api(request):
    url = "https://graph.facebook.com/v21.0/me"
    params = {
        'access_token': settings.META_ACCESS_TOKEN,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        app_info = data

        # Vérifier si le type de l'application est présent dans la réponse
        if 'id' in app_info:
            success_message = "L'application est configurée et a renvoyé une réponse API valide."
            return render(request, 'test.html', {'app_info': app_info, 'message': success_message})
        else:
            error_message = "L'application ne semble pas être de type Business ou manque d'autorisations nécessaires."
            return render(request, 'test.html', {'error_message': error_message})

    except requests.exceptions.RequestException as e:
        error_message = f"Erreur lors de la requête API : {e}"
        return render(request, 'scraper/test.html', {'error_message': error_message})