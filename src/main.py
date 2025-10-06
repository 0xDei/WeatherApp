import flet as ft
import flet_geolocator as fgl
from database import init_db
from logic import *
import asyncio


async def main(page: ft.Page):
    page.title = "Weather App"
    page.theme_mode = ft.ThemeMode.DARK
    
    db_conn = init_db()
    gl = fgl.Geolocator(location_settings=fgl.GeolocatorSettings(accuracy=fgl.GeolocatorPositionAccuracy.LOW))
    page.overlay.append(gl)
    page.update()

    async def route_change(route):
        page.views.clear()
        await set_root_page(page)
        if page.route == "/settings": 
            print("TODO")

    def view_pop():
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    async def handle_permission_request():
        print("Requesting location permission...")
        try:
            page.snack_bar = ft.SnackBar(ft.Text("Requesting for location permission..."), True)
            page.update()
            
            await gl.request_permission(wait_timeout=60)

            page.snack_bar.open = False
            page.update()
        except Exception as e:
            print("Error requesting for permission: ", e)

    async def after_render():
        await asyncio.sleep(0.2) # adds a small delay to make sure Geolocator control is added
        if await gl.get_permission_status_async() not in [fgl.GeolocatorPermissionStatus.ALWAYS, fgl.GeolocatorPermissionStatus.WHILE_IN_USE, fgl.GeolocatorPermissionStatus.UNABLE_TO_DETERMINE]: await handle_permission_request()

    await after_render()

    try:
        pos = await gl.get_current_position_async(fgl.GeolocatorPositionAccuracy.LOW)
        longitude = pos.longitude
        latitude = pos.latitude
        set_longitude(longitude)
        set_latitude(latitude)
        init_weather_api()

    except Exception:
        print("Error with getting current position, using default position instead.")
        init_weather_api()

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.go(page.route)

if __name__ == "__main__":
    asyncio.run(ft.app_async(target=main))