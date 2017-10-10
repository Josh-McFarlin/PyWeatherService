# PyWeatherService

This code is a proof of concept SMS weather information system written in Python 3. 

It utilizes the following APIs:

* Twilio - For sending and recieving text messages and media.
* Weather Underground - For receiving current weather conditions, weather alerts, and radar images.
* Cloudinary - For hosting radar images to reduce API calls.


### Live Test

This code is currently being hosted on a Linux VM and is freely available for testing
until the Twilio funds run out.

Send a message to **(770) 212-2053** to try it out!

If the service does not respond, that may mean I'm working on the code, so try again later.
If repeated attempts fail to issue a response, that probably means I have run out of API calls,
and it is questionable if or when the service will be available again.


### Usage

Before using this code, add the necessary API keys to "config-example.py" and then rename the
file to "config.py".


### Future plans
* Clean-up app.py structure
* Send an alert to subscribed users in an area when a new weather alert is added
* Use raw XML data from NOAA to reduce paid API usage and limitations
* Switch to MongoDB
* Add backup zip-code to city methods