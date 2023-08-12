import requests
import os

def get_access_token(client_id, client_secret, scope, token_url):
    """
    Retrieves an access token from the token URL using client credentials.

    Args:
        client_id (str): The client ID.
        client_secret (str): The client secret.
        scope (str): The scope of the access token.
        token_url (str): The complete URL to retrieve the access token from.

    Returns:
        str: The access token.

    Raises:
        ValueError: If the response status code is not 200.
        requests.exceptions.HTTPError: If an HTTP error occurs during the request.
    """
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials",
        "scope": scope
    }
    try:
        response = requests.post(token_url, data=data)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    access_token = response.json()["access_token"]
    return access_token

def fetch_chapters_and_verses(access_token):
    base_url = "https://bhagavadgita.io/api/v1"
    chapters_url = base_url + "/chapters"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(chapters_url, headers=headers)
    chapters = response.json()

    output_dir = 'bhagavad_gita_txt'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for chapter in chapters:
        chapter_number = chapter['chapter_number']
        chapter_title = chapter['name']

        verses_url = f"{base_url}/verses?chapter_number={chapter_number}"
        response = requests.get(verses_url, headers=headers)
        verses = response.json()

        chapter_filename = f'{chapter_number:02d}_{chapter_title}.txt'
        chapter_filepath = os.path.join(output_dir, chapter_filename)

        with open(chapter_filepath, 'w', encoding='utf-8') as f:
            for verse in verses:
                if verse['language'] == 'en':
                    f.write(verse['text'] + '\n\n')

        print(f'Chapter {chapter_number} saved as {chapter_filename}')

    print('All chapters saved.')

if __name__ == "__main__":
    client_id = 'uDRlmWCMjhhHYwig43mj6gJ6ZNvPALMHuQI9TDmr'
    client_secret = 'JVGaTwLyzO571u47KOkC9zdb5aUwEdX2ozawlJvQV7TpNeJcEp'
    scope = '1 1'  # Replace with the appropriate scope
    token_url = 'https://bhagavadgita.io/auth/oauth/token'

    access_token = get_access_token(client_id, client_secret, scope, token_url)
    fetch_chapters_and_verses(access_token)
