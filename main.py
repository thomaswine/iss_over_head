import time
import requests
from datetime import datetime
import smtplib

MY_LAT = 47.594073 # Your latitude
MY_LONG = 19.059144 # Your longitude
MY_EMAIL = "email"
MY_PASSWORD = "pwd"


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if MY_LAT in range(int(iss_latitude) - 5, int(iss_latitude) + 5) and MY_LONG in range(int(iss_longitude) - 5, int(iss_longitude) + 5):
        return True

def is_nightime():
    parameter = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameter)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = datetime.now().hour

    if time_now > sunset or time_now < sunrise:
        return True

while True:
    time.sleep(60)
    if is_iss_overhead() and is_nightime():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs="email",
                msg=f"Subject:LOOK UP ON THE SKY\n\nHey, ISS is nearby to you, look up.")
            connection.close()

    else:
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs="email",
                msg=f"Subject:SKY IS CLEAR\n\nThere is nothing on the sky.")
            connection.close()



