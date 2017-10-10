import requests
import string
import random
import urllib.request


def process_text(e):
    e = e.encode('utf-8').decode('utf-8')
    e = e.strip()
    e = e.replace("\\n", " ")
    e = e.replace("...", " ")
    e = e.replace("    ", " ")
    e = e.replace("   ", " ")
    e = e.replace("  ", " ")
    e = e.replace("\n\n", "\n")
    e += "..."
    return e


class WU:
    def __init__(self, api_key, location):
        self.api_key = api_key
        self.loc = location

    def get_conditions(self):
        url = "https://api.wunderground.com/api/{}/conditions/q/{}/{}.json".format(self.api_key, self.loc.state,
                                                                                   self.loc.city)
        r = requests.get(url)
        j = r.json()

        location = j["current_observation"]["display_location"]["full"]
        weather = j["current_observation"]["weather"]
        temperature = j["current_observation"]["temp_f"]
        return "The current condition in {} is {} and {} °F.".format(location, weather.lower(), temperature)

    def get_alerts(self):
        url = "https://api.wunderground.com/api/{}/alerts/q/{}/{}.json".format(self.api_key, self.loc.state,
                                                                               self.loc.city)
        r = requests.get(url)
        j = r.json()

        max_length = 1500
        alerts_j = j['alerts']

        if alerts_j:
            descriptions = [i["description"] for i in alerts_j]
            messages = [process_text(i["message"]) for i in alerts_j]
            expires = [i["expires"] for i in alerts_j]

            d_length = len("".join(descriptions))
            e_length = len("".join(expires))

            message_length = int((max_length - d_length - e_length) / len(messages))

            short_messages = [i[:message_length] for i in messages]

            alerts = []
            for i in range(len(descriptions)):
                a = "Alert: {}.\n{}...\nExpires {}.".format(descriptions[i], short_messages[i], expires[i])
                alerts.append(a)

            return "\n".join(alerts)
        else:
            return "There are no weather alerts for {}, {} at this time.".format(self.loc.city, self.loc.state)

    def get_animation(self):
        url = "https://api.wunderground.com/api/{}/animatedradar/q/{}/{}.gif?width=500&height=500&newmaps=1&num=15&smoothing=1&noclutter=1&delay=12".format(  # noqa
            self.api_key, self.loc.state, self.loc.city)
        random_name = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))
        resp = urllib.request.urlretrieve(url, "Images/" + random_name + ".gif")
        return random_name
