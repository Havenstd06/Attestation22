import asyncio
import glob
import os
import time
import json
from functools import wraps

from halo import Halo
from pyppeteer import launch
from rich import print
from rich.text import Text
from rich.console import Console
console = Console()


def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


def get_choice(question: str, choices: list):
    prompt = console.input(f'{question} ([bold orange_red1]{str("/".join(map(str, choices)))}[/]) : ')
    if prompt not in choices:
        console.print('[bold red]Erreur ! Veuillez sélectionner une option[/]')
        return get_choice(question, choices)
    else:
        return prompt


def get_attestation_dir():
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), 'attestations')


@coro
async def main():
    try:
        config_file_name = input('Quel est le fichier configuration ? ')

        if not os.path.exists(f'{config_file_name}.json'):
            new_config = {
                'prenom': console.input('Quel est ton prénom ? '),
                'nom': console.input('Quel est ton nom ? '),
                'date_naissance': console.input('Quel est ta date de naissance ? [bold green]JJ/MM/AAAA (J = Jour | M = Mois | A = Année)[/] '),
                'lieu_de_naissance': console.input('Quel est ton lieu de naissance ? '),
                'adresse': console.input('Quel est ton adresse ? '),
                'ville': console.input('Quel est ta ville ? '),
                'code_postal': console.input('Quel est ton code postal ? '),
                'motif': get_choice('Quel est ton motif de sortie ? ',
                                    choices=['travail', 'achats', 'sante', 'famille', 'handicap', 'sport_animaux', 'convocation', 'missions', 'enfants'])
            }

            with open(f'{config_file_name}.json', 'w') as config_file:
                config_file.write(json.dumps(new_config, indent=4))
            console.print('[bold bright_green]Le fichier config a été crée[/]')

        spinner = Halo(text='Génération de la convocation...', spinner='clocks')
        spinner.start()

        if os.path.exists(f'{config_file_name}.json'):
            with open(f'{config_file_name}.json') as config:
                config = json.loads(config.read())

                browser = await launch({'headless': True})
                page = await browser.newPage()
                await page.setViewport(
                    {"width": 1920, "height": 1080, "deviceScaleFactor": 1.0}
                )
                await page.goto('https://media.interieur.gouv.fr/deplacement-covid-19/')

                await page.type('#field-firstname', config.get('prenom'))  # Prenom
                await page.type('#field-lastname', config.get('nom'))  # Nom
                await page.type('#field-birthday', config.get('date_naissance'))  # Date de naissance (DD/MM/YYYY)
                await page.type('#field-placeofbirth', config.get('lieu_de_naissance'))  # Lieu de naissance
                await page.type('#field-address', config.get('adresse'))  # Adresse
                await page.type('#field-city', config.get('ville'))  # Ville
                await page.type('#field-zipcode', config.get('code_postal'))  # Code Postal
                await page.type('#field-heuresortie', time.strftime('%I%M%p'))  # Heure de sortie

                await page.evaluate(f'''() => 
                    document.querySelector('#checkbox-{config.get('motif')}').click()
                ''')

            if not os.path.isdir(get_attestation_dir()):
                os.mkdir(get_attestation_dir())

            cdp = await page.target.createCDPSession()
            await cdp.send('Page.setDownloadBehavior', {
                'behavior': 'allow',
                'downloadPath': get_attestation_dir()
            })

            default_file_count = len([iq for iq in os.scandir(get_attestation_dir())])

            await page.click('#generate-btn')
            time.sleep(2)

            list_of_files = glob.glob(os.path.join(get_attestation_dir(), '*'))
            latest_file = max(list_of_files, key=os.path.getctime)
            os.rename(rf'{latest_file}', f"{get_attestation_dir()}/Attestation-{time.strftime('%d-%m-%d-%Y-%H-%M-%S')}-{config_file_name}.pdf")

            after_file_count = len([iq for iq in os.scandir(get_attestation_dir())])

            await page.close()
            await browser.close()

            if after_file_count == default_file_count + 1:
                spinner.succeed(text='Votre convocation a été crée avec succès !')
            else:
                spinner.fail(text='Un problème est survenue lors du téléchargement de votre convocation, merci de vérifier le fichier configuration.')

    # except AssertionError as error:
    #     print(error)
    except Exception:
        print('Un problème est survenue, merci de vérifier le fichier configuration.')

if __name__ == "__main__":
    main()
    input('Tappez entrer pour quittez')
