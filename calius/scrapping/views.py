from django.shortcuts import render
from bs4 import BeautifulSoup
import requests

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
