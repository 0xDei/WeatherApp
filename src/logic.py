import flet as ft
from database import get_token

def set_root_page(page):
    if get_token() == None:
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("Weather App Not Logged In"))
                ]
            )
        )
    else:
        page.views.append(get_main_page())
    page.update()


def get_main_page():
    return ft.View(
        "/",
        [
            ft.AppBar(title=ft.Text('Weather App Logged In'))
        ]
    )