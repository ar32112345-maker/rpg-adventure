class GameMap:
    def __init__(self, width=10, height=10):
        self.width = width
        self.height = height

        self.locations = {
            (2, 2): "Dark Forest",
            (5, 3): "Abandoned village",
            (7, 7): "Ancient Ruins",
            (3, 8): "Merchant Camp"
        }
    def is_valid_position(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def move_player(self, player, dx, dy):
        new_x = player.x + dx
        new_y = player.y + dy

        if not self.is_valid_position(new_x, new_y):
            print("you cannot move outside the map borders.")
            return False
        player.move(new_x - player.x, new_y - player.y)
        location = self.get_location(player.x , player.y)
        print(f"you moved to ({player.x}, {player.y})")

        if location:
            print(f"you discovered: {location}!")

        return True
    def get_location(self, x, y):
        return self.locations.get((x,y))
    def show_map(self, player):
        print("\n--- WORLD MAP ---")

        for y in range(self.height):
            row = ""

            for x in range(self.width):
                if player.x == x and player.y == y:
                    row += " P "
                elif (x,y) in self.locations:
                    row += "L"
                else:
                    row += " . "

            print(row)
        print("\nP = Player | L = Location | . = Empty space")

if __name__ == "__main__":
    from player import Player

    player = Player("Hero")
    game_map = GameMap()

    game_map.show_map(player)

    game_map.move_player(player, 1, 0)
    game_map.move_player(player, 1, 1)

    game_map.show_map(player)