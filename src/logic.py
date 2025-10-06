import flet as ft
from database import get_token
from weatherapi import WeatherAPI


longitude = 123.375341
latitude = 13.405957
weather_api = None


def set_longitude(num):
    global longitude
    longitude = num

def get_longitude():
    return longitude


def set_latitude(num):
    global latitude
    latitude = num

def get_latitude():
    return latitude


def init_weather_api():
    global weather_api
    weather_api = WeatherAPI(get_latitude(), get_longitude())


async def set_root_page(page):
    if get_token() is not None: # make this 'token == None' when log in page is implemented 
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("Weather App Not Logged In"))
                ]
            )
        )
    else:
        page.views.append(await get_main_page())
    page.update()


async def get_main_page():
    loc = await weather_api.get_location()
    return ft.View(
        "/",
        [
            ft.AppBar(title=ft.Text(f'Location: {loc['city']}, {loc['countryCode']}'))
        ]
    )