import requests


class Location:
    zip_code = "30332"
    city = "Atlanta"
    state = "GA"

    def __init__(self, zip_code=None, city=None, state=None):
        if zip_code:
            self.zip_code = zip_code
            self.set_city_state(self.zip_code)
        elif city and state:
            self.city = city
            self.state = state
        self.format_location()

    def set_city_state(self, zip_code):
        url = "http://ziptasticapi.com/" + str(zip_code)
        r = requests.get(url)
        j = r.json()
        if "error" in j:
            raise KeyError
        elif "city" in j:
            self.city = j["city"]
            self.state = j["state"]
            self.format_location()

    def format_location(self):
        city_words = self.city.split()
        formatted_words = [i[0].upper() + i[1:].lower() for i in city_words]
        self.city = " ".join(formatted_words)
        self.state = self.state.upper()
