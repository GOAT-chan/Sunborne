import niquests

def get_country_name(country_code: str) -> str:
    r = niquests.get(f"https://countries.dev/alpha/{country_code.lower()}")
    return r.json()['name']

def get_country_emoji(country_code: str) -> str:
    return f":flag_{country_code.lower()}:"