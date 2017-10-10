from flask import Flask, request, session
from twilio.twiml.messaging_response import Message, MessagingResponse
from utils.SMS import Twilio
from utils.Weather import WU
from utils.Location import Location
import cloudinary
from cloudinary import uploader
from requests.exceptions import RequestException
from urllib.error import HTTPError


app = Flask(__name__)
app.config.from_pyfile("config.py")


@app.route("/sms", methods=["POST"])
def sms():

    message_body = request.form['Body'].lower()
    resp = MessagingResponse()
    reply_message = Message()

    registered = session.get("registered", False)
    zip_c = session.get("zip_c", "30322")

    if registered:
        loc = Location(zip_c)
        wu = WU(wu_key, loc)

        if "zipchange" in message_body.lower():
            nums = [int(i) for i in message_body.split() if i.isdigit()]
            if len(nums):
                zip_code = str(nums[0])
                try:
                    temp_loc = Location(zip_code)
                    session["zip_c"] = zip_code
                    reply_text = "Your zip code has been changed to {} - {}, {}.".format(zip_code, temp_loc.city,
                                                                                         temp_loc.state)
                except KeyError:
                    reply_text = "The zip code provided was not valid."
            else:
                reply_text = "The correct syntax for this command is zipchange (zip code here)."
        else:
            if len(message_body.split()) == 1:
                if "commands" in message_body:
                    reply_text = (
                        "Available commands include:\n\n"
                        "alerts - See a list of weather alerts for the set area.\n\n"
                        "conditions - See current weather conditions for the set area.\n\n"
                        "radar - View a live weather radar image for the set area. This command has a delay.\n\n"
                        "zipchange - Change the zip code of the selected area.\n\n"
                        "details - View details about this service.\n\n"
                        "credit - View information about Weather Underground, the weather data provider.")
                elif "alerts" in message_body:
                    try:
                        reply_text = wu.get_alerts()
                    except RequestException:
                        reply_text = "Weather alerts could not be found at this time, please try again later."
                elif "conditions" in message_body:
                    try:
                        reply_text = wu.get_conditions()
                    except RequestException:
                        reply_text = "The weather conditions could not be found at this time, please try again later."
                elif "radar" in message_body:
                    try:
                        file_name = wu.get_animation()
                        uploader.upload("Images/" + file_name + ".gif", public_id=file_name)
                        c_url = cloudinary.utils.cloudinary_url(file_name)[0]
                        reply_message.media(c_url)
                        reply_text = "{}, {} Radar".format(loc.city, loc.state)
                    except HTTPError:
                        reply_text = "The radar imagery could not be found at this time, please try again later."
                elif "details" in message_body:
                    reply_text = ("This service was created by Josh McFarlin in Python. "
                                  "This service is a proof of concept, and is not intended for lifesaving uses. "
                                  "Messaging and data rates may apply.\n\nhttp://JoshMcFarlin.me/")
                elif "credit" in message_body:
                    reply_text = "All weather data is provided by Weather Underground."
                    reply_message.media("https://icons.wxug.com/logos/PNG/wundergroundLogo_4c_rev.png")
                else:
                    reply_text = 'Please reply with a valid command, type "commands" to view a list of commands.'
            else:
                reply_text = "Please only use one command at a time."
    else:
        if message_body.isdigit():
            session["registered"] = True
            session["zip_c"] = message_body
            reply_text = 'Thanks for registering! Type "commands" to view a list of commands.'
        else:
            reply_text = "Welcome. In order to subscribe to weather updates, please reply with a zip code."

    reply_message.body(reply_text)
    resp.append(reply_message)
    return str(resp)

if __name__ == "__main__":
    cloudinary.config(
        cloud_name=app.config["C_CLOUD_NAME"],
        api_key=app.config["C_API_KEY"],
        api_secret=app.config["C_API_SECRET"]
    )

    app.secret_key = app.config["APP_SECRET_KEY"]
    app.config["SESSION_TYPE"] = "filesystem"
    t = Twilio(app.config["T_ACCOUNT_SID"], app.config["T_AUTH_TOKEN"], app.config["T_FROM_NUMBER"])
    wu_key = app.config["WU_API_KEY"]

    app.run()
