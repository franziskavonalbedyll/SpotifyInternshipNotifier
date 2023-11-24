import requests
import re

def download_html(url):
    """
    Downloads the HTML content of the given URL.

    Parameters:
    url (str): The URL to download the HTML content from.

    Returns:
    str: The HTML content of the page.
    """
    response = requests.get(url)
    response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
    return response.text

def check_internship_availability(html_content):
    """
    Checks if there are internship positions available in the HTML content of the Spotify jobs page.

    Parameters:
    html_content (str): HTML content of the Spotify jobs page.

    Returns:
    bool: True if there are internship positions available, False otherwise.
    """

    results = {}
    match = re.search(r'"label":"Internship","positions":(\d+)', html_content)
    if match:
        number_of_positions = match.group(1)
        results["match"] = True
        results["number_of_positions"] = int(number_of_positions)
        return results
    else:
        results["match"] = False
        return results


# URL of the Spotify jobs page
url = 'https://www.lifeatspotify.com/jobs?j=internship'

## Download the HTML content of the page
html_content = download_html(url)

## Check if there are internship positions available
result = check_internship_availability(html_content)
print(result)
