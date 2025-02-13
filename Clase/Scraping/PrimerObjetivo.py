import requests
import json
from bs4 import BeautifulSoup
from Pelicula import Pelicula


def ejecutar(salida):
    lista = []

    url = "https://www.filmaffinity.com/es/rdcat.php?id=upc_th_es"
    response = requests.get(url)
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')

    divs_peliculas = soup.find_all('div', class_='top-movie')

    for div_pelicula in divs_peliculas:
        # Intenta encontrar el título de la película dentro del div actual
        div_mc_right = div_pelicula.find('div', class_='mc-right')
        if div_mc_right:
            titulo_element = div_mc_right.find('h3').find('a')
            if titulo_element:
                link = titulo_element.get('href')
                titulo = titulo_element.text.strip()
            else:
                titulo = "Título no encontrado"
        else:
            titulo = "Título no encontrado"

        fecha_lanzamiento = div_pelicula.find('span', class_='date').text

        valoracion = div_pelicula.find('div', class_='avg-rating').text

        lista.append(Pelicula(titulo, fecha_lanzamiento, valoracion, link, 0, 0, 0, 0))

    lista_ordenada = sorted(lista, key=lambda pelicula: pelicula.valoracion, reverse=True)

    if salida == '0':
        for pelicula in lista_ordenada:
            pelicula.mostrar_informacion()
    if salida == '1':
        listaPeliculas = ""
        for pelicula in lista_ordenada:
            listaPeliculas += pelicula.devolver_links()

        return listaPeliculas

