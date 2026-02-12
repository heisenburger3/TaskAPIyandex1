import os
import requests
import arcade

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 450
WINDOW_TITLE = "MAP"
MAP_FILE = "map.png"
lat = '55.757718'
lon = '37.677751'
z = 0


class GameView(arcade.Window):
    def setup(self):
        self.get_image(z, lat, lon)
        self.z = z
        self.lon = lon
        self.lat = lat

    def request(self, z, lat, lon):
        server_address = 'https://static-maps.yandex.ru/v1?'
        api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
        params = {
            'll': ','.join([lon, lat]),
            'z': z,
            'apikey': api_key
        }
        response = requests.get(server_address, params=params)
        return response

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.lon = str(float(self.lon) - 0.001)
            self.get_image(self.z, self.lat, self.lon)
        elif key == arcade.key.RIGHT:
            self.lon = str(float(self.lon) + 0.001)
            self.get_image(self.z, self.lat, self.lon)
        elif key == arcade.key.UP:
            self.lat = str(float(self.lat) + 0.001)
            self.get_image(self.z, self.lat, self.lon)
        elif key == arcade.key.DOWN:
            self.lat = str(float(self.lat) - 0.001)
            self.get_image(self.z, self.lat, self.lon)
        elif key == arcade.key.PAGEUP and self.z < 21:
            self.z += 1
            self.get_image(self.z, lat, lon)
        elif key == arcade.key.PAGEDOWN and self.z > 0:
            self.z -= 1
            self.get_image(self.z, lat, lon)

    def on_draw(self):
        self.clear()

        arcade.draw_texture_rect(
            self.background,
            arcade.LBWH(
                (self.width - self.background.width) // 2,
                (self.height - self.background.height) // 2,
                self.background.width,
                self.background.height
            ),
        )

    def get_image(self, z, lat, lon):
        response = self.request(z, lat, lon)
        with open(MAP_FILE, "wb") as file:
            file.write(response.content)

        self.background = arcade.load_texture(MAP_FILE)


def main():
    gameview = GameView(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    gameview.setup()
    arcade.run()
    os.remove(MAP_FILE)


if __name__ == "__main__":
    main()
