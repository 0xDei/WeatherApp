import flet as ft
from database import init_db
from logic import *

def main(page: ft.Page):
    page.title = "Weather App"
    page.theme_mode = ft.ThemeMode.DARK
    
    db_conn = init_db()
    
    def route_change(route):
        page.views.clear()
        set_root_page(page)
        if page.route == "/settings": 
            print("TODO")


    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

if __name__ == "__main__":
    ft.app(main)