Change&idealog:

1. import requests n'emp�che pas le plugin de se lancer, donc je pr�sume qu'il l'importe bien

2. en l'ayant trouv� dans le plugin natif d'edmc pour eddb, j'ai essay� d'ajouter: 

STATION_UNDOCKED: str = 'No data found'  # "Station" name to display when not docked = U+00D7

au load.py encore une fois sans probl�me si ce n'est que �a ne semble rien changer

3. j'ai aussi copi� et modifi� les url de:

def system_url(system_name: str) -> str:
    if this.system_address:
        return requests.utils.requote_uri(f'https://en.wikipedia.org/{this.system_address}')

    if system_name:
        return requests.utils.requote_uri(f'https://en.wikipedia.org/{system_name}')

    return ''

Encore une fois sans comprendre si ce que je fais marchais ou pas.