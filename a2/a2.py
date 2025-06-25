import tkinter as tk
from tkinter import messagebox, filedialog
from typing import Callable, Optional

from support import *


# Implement the classes, methods & functions described in the task sheet here

"""
4.1.1 Weapon()
"""


class Weapon:
    def __init__(self):
        self._name = "AbstractWeapon"
        self._symbol = "W"
        self._effect = {}
        self._range = 0

    def get_name(self) -> str:
        return self._name

    def get_symbol(self) -> str:
        return self._symbol  # Ensure this returns the correct symbol

    def get_effect(self) -> dict[str, int]:
        return self._effect

    def get_targets(self, position: tuple[int, int]) -> list[tuple[int, int]]:
        """Returns the target position within range based on the
        current position of the weapon
        parameter:
        position (tuple[int, int]): The current coordinates
        (x, y) of the weapon.
        Return value:
        list[tuple[int, int]]: List of target coordinates (x, y)
        within the weapon attack range."""
        targets = []

        # If the range is greater than 0, generate target positions of
        # up, down, left, and right
        if self._range > 0:
            x, y = position  # Get the current weapon position
            for i in range(1, self._range + 1):
                targets.append((x, y - i))  # up
                targets.append((x, y + i))  # down
                targets.append((x - i, y))  # left
                targets.append((x + i, y))  # right

        return targets

    def __str__(self) -> str:
        return self.get_name()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"


"""
4.1.2 PoisonDart(Weapon)
"""


class PoisonDart(Weapon):
    """
    Attribute:
        _name (str): Weapon name, set to "PoisonDart".
        _symbol (str): symbols "D"。
        _effect (dict): A dictionary containing weapon effects. Defaults to
        {"poison": 2}, meaning 2 points of poison effect are applied per attack.
        _range (int): The weapon's attack range, set to 2.
    """
    def __init__(self):
        super().__init__()
        self._name = "PoisonDart"
        self._symbol = "D"
        self._effect = {"poison": 2}
        self._range = 2


"""
4.1.3 PoisonSword(Weapon)
"""


class PoisonSword(Weapon):
    """。
    Attribute:
        _name (str): Weapon name, set to "PoisonSword".
        _symbol (str): Corresponds to the symbol "S".
        _effect (dict): A dictionary containing weapon effects, defaults to
        {"damage": 2, "poison": 1}, meaning 2 points of damage and 1 point of
        poison effect are applied per attack.
        _range (int): The weapon's attack range, set to 1.
    """
    def __init__(self):
        super().__init__()
        self._name = "PoisonSword"
        self._symbol = "S"
        self._effect = {"damage": 2, "poison": 1}
        self._range = 1


"""
4.1.4 HealingRock(Weapon)
"""


class HealingRock(Weapon):
    """
    Attribute:
        _name (str): Weapon name, set to "HealingRock".
        _symbol (str): Corresponds to the symbol "H".
        _effect (dict): A dictionary containing weapon effects,
        which defaults to {"healing": 2},
        meaning that each use restores 2 health points.
        _range (int): The weapon's area of effect, set to 2.
    """
    def __init__(self):
        super().__init__()
        self._name = "HealingRock"
        self._symbol = "H"
        self._effect = {"healing": 2}
        self._range = 2


"""
4.1.5 Tile()
"""


class Tile:
    """
    Represents a tile in the map that may or may not block movement,
    and may contain weapons.

    Attribute:
        _symbol (str): Symbolic representation of the tile (such as wall
        "#" or open space " ").
        _is_blocking (bool): Whether to block movement, True means blocking.
        _weapon (Optional[Weapon]): Weapons that may be included on the tile,
        defaults to None.

    Methods:
        is_blocking() -> bool: Returns whether this tile blocks movement.
        get_weapon() -> Optional[Weapon]: Returns the weapon on the tile
        (if any).
        set_weapon(weapon: Weapon) -> None: Set the weapon on this tile.
        remove_weapon() -> None: Removes weapons from tiles.
    """
    def __init__(self, symbol: str, is_blocking: bool) -> None:
        self._symbol = symbol
        self._is_blocking = is_blocking
        self._weapon = None  # The new tile does not contain weapon

    def is_blocking(self) -> bool:
        return self._is_blocking

    def get_weapon(self) -> Optional[Weapon]:
        return self._weapon

    def set_weapon(self, weapon: Weapon) -> None:
        self._weapon = weapon

    def remove_weapon(self) -> None:
        self._weapon = None

    def __str__(self) -> str:
        return self._symbol

    def __repr__(self) -> str:
        return f"Tile('{self._symbol}', {self._is_blocking})"


"""
4.1.6 create_tile(symbol: str)-> Tile
"""


def create_tile(symbol: str) -> Tile:
    """
    Create and return the corresponding Tile object based on the input symbol.

    This function creates different types of Tiles based on different symbols:
        If the symbol is "#", create a Tile that blocks movement.
        If the symbol is " " or "G", create a Tile that does not block movement.
        If the symbol is "D", "S", or "H", create a Tile that does not block
        movement and set the corresponding weapon.
          "D" spawns the PoisonDart weapon.
          "S" spawns the PoisonSword weapon.
          "H" spawns the HealingRock weapon.
        For other symbols, returns an empty Tile that does not block movement.

    parameter:
        symbol (str): Symbol indicating which type of Tile should be created.

    Return value:
        Tile: Tile objects created from symbols.
    """
    if symbol == "#":
        return Tile("#", True)
    elif symbol in [" ", "G"]:
        return Tile(symbol, False)
    elif symbol in ["D", "S", "H"]:
        # Create a non-blocking ground tile and set the corresponding weapons
        weapon_map = {
            "D": PoisonDart,
            "S": PoisonSword,
            "H": HealingRock
        }
        tile = Tile(" ", False)
        tile.set_weapon(weapon_map[symbol]())
        return tile
    else:
        return Tile(" ", False)


"""
4.1.7 Entity()
"""


class Entity:
    """
    Represents an entity in the game with attributes of maximum health and
    current health.

    Attribute:
        _max_health (int): The entity's maximum health.
        _current_health (int): The entity's current health value,
        initially set to its maximum health value.

    Methods:
        get_health() -> int: Returns the current health value.
        is_alive() -> bool: Determine whether the entity is alive.
        take_damage(amount: int) -> None: Causes damage to entities,
        reducing their health.
        heal(amount: int) -> None: Restore health to the entity.
    """
    def __init__(self, max_health: int):
        self._max_health = max_health  # max health
        self._current_health = max_health  # initial current max health
        self._poison_stat = 0  # initial poison
        self._weapon: Optional[Weapon] = None  # initial no weapon
        self._name = "Entity"  # default name
        self._symbol = "E"  # default symbol

    def get_symbol(self) -> str:
        return self._symbol

    def get_name(self) -> str:
        return self._name

    def get_health(self) -> int:
        return self._current_health

    def get_poison(self) -> int:
        return self._poison_stat

    def get_weapon(self) -> Optional[Weapon]:
        return self._weapon

    def equip(self, weapon: Weapon) -> None:
        """Equip weapons, replace existing weapons"""
        self._weapon = weapon

    def get_weapon_targets(self, position: tuple[int, int]) -> list[tuple[int, int]]:
        """Returns the target position that the weapon can attack"""
        if self._weapon:
            return self._weapon.get_targets(position)
        return []

    def get_weapon_effect(self) -> dict[str, int]:
        """Returns the effect of the current weapon. If there is no weapon,
        returns an empty dictionary."""
        if self._weapon:
            return self._weapon.get_effect()
        return {}

    def apply_effects(self, effects: dict[str, int]) -> None:
        """Apply damage, healing and poison effects"""
        if "healing" in effects:
            self._current_health = min(self._max_health, self._current_health + effects["healing"])
        if "damage" in effects:
            self._current_health = max(0, self._current_health - effects["damage"])
        if "poison" in effects:
            self._poison_stat += effects["poison"]

    def apply_poison(self) -> None:
        """Apply poison effect every turn"""
        if self._poison_stat > 0:
            self._current_health = max(0, self._current_health - self._poison_stat)
            self._poison_stat = max(0, self._poison_stat - 1)

    def is_alive(self) -> bool:
        """Determine whether the entity is still alive"""
        return self._current_health > 0

    def __str__(self) -> str:
        """Return entity name"""
        return self.get_name()

    def __repr__(self) -> str:
        """Returns a string constructible in the REPL"""
        return f"{self.__class__.__name__}({self._max_health})"


"""
4.1.8 Player(Entity)
"""


class Player(Entity):
    """
    Represents the player entity in the game, inherited from the Entity class.

    Players have their own maximum health and have unique symbols and names.

    Properties inherited from Entity class:
        _max_health (int)
        _current_health (int)
        _poison_stat (int)
        _weapon (Optional[Weapon])

    Methods:
        get_symbol() -> str: Returns the symbol "P" representing the player.
        get_name() -> str: Returns the player's name "Player".
    """
    def __init__(self, max_health: int) -> None:
        super().__init__(max_health)

    def get_symbol(self) -> str:
        return "P"

    def get_name(self) -> str:
        return "Player"


"""
4.1.9 Slug(Entity)
"""


class Slug(Entity):
    """
    Represents the slug entity in the game, inherited from the Entity class.

    The slug entity has a turn counter to determine whether
    it can move during the current turn. This category serves as a base class,
    and specific movement and attack logic needs to be implemented
    by subclasses.

    Properties inherited from Entity class:
        _max_health (int):
        _current_health (int):
        _poison_stat (int):
        _weapon (Optional[Weapon]):

    New attributes:
        turn_count (int): Round counter, used to determine
        whether the slug can move in the current round.

    Methods:
        get_name() -> str: Returns the name of the slug "Slug".
        get_symbol() -> str: Returns the symbol "M" for the slug.
        end_turn() -> None: Executed at the end of each round,
        updating the round count.
        can_move() -> bool: Checks if the slug can move during the current turn.
        move() -> None: The movement logic that should be implemented
        in subclasses.
        attack() -> None: Attack logic that should be implemented in subclasses.
        choose_move() -> None: Select move logic that should be implemented
        in subclasses.
    """
    def __init__(self, max_health: int) -> None:
        super().__init__(max_health)
        self.turn_count = 0

    def get_name(self) -> str:
        """Return entity name 'Slug'"""
        return "Slug"

    def get_symbol(self) -> str:
        """Return entity symbol 'M'"""
        return "M"

    def end_turn(self):
        """Executed at the end of each round,
        updating the round counter and deciding whether to move"""
        self.turn_count += 1

    def can_move(self) -> bool:
        """Checks whether the entity can move during the current turn"""
        return self.turn_count % 2 == 0

    def move(self):
        """should be implemented in subclasses"""
        raise NotImplementedError("Slug subclasses must implement the move method")

    def attack(self):
        """should be implemented in subclasses"""
        raise NotImplementedError("Slug subclasses must implement the attack method")

    def choose_move(self, valid_positions: list,
                    current_position: tuple[int, int],
                    target_position: tuple[int, int]):
        """Movement logic should be implemented in subclasses"""
        raise NotImplementedError(
            "Slug subclasses must implement a choose_move method.")


"""
4.1.10 NiceSlug(Slug)
"""


class NiceSlug(Slug):
    """
    Represents a NiceSlug, inherited from the Slug class.

    NiceSlug always has a maximum health of 10 and comes
    equipped with a HealingRock as a weapon.
    Its action characteristic is that it will never move and will only stay at
    its current location.

    Properties inherited from Slug class:
        turn_count (int): Round counter, used to determine whether the slug
        can move in the current round.
        _max_health (int): Max health, fixed to 10 for NiceSlug.
        _weapon (Weapon): Equipped with HealingRock weapon.

    Methods:
        choose_move() -> tuple[int, int]: NiceSlug Does not move,
        always returns to current location.
        get_symbol() -> str: Returns the symbol "N" for NiceSlug.
        get_name() -> str: Returns the name of NiceSlug "NiceSlug".
        __repr__() -> str: Returns the type name of this object.
    """
    def __init__(self) -> None:
        super().__init__(10)  # NiceSlug always has max_health of 10
        self.equip(HealingRock())  # Equip HealingRock weapon

    def choose_move(
            self,
            candidates: list[tuple[int, int]],
            current_position: tuple[int, int],
            target_position: tuple[int, int],
    ) -> tuple[int, int]:
        # NiceSlug always stays in its current position
        return current_position

    def get_symbol(self) -> str:
        return "N"

    def get_name(self) -> str:
        return "NiceSlug"

    def __repr__(self) -> str:
        return self.__class__.__name__ + "()"


"""
4.1.11 AngrySlug(Slug)
"""


class AngrySlug(Slug):
    """
    Represents an angry slug (AngrySlug), inherited from the Slug class.

    AngrySlug has a maximum health of 5 and is equipped with a
    PoisonSword as a weapon.
    It selects the closest movement position based on the player's position and
    uses squared distances for comparison, thus avoiding floating
    point calculations.

    Properties inherited from Slug class:
        turn_count (int): Round counter, used to determine whether the slug
        can move in the current round.
        _max_health (int): Max health, fixed to 5 for AngrySlug.
        _weapon (Weapon): Equipped with the PoisonSword weapon.

    Methods:
        choose_move() -> tuple[int, int]: Selects the closest movement position
        based on the player's position.
        squared_distance() -> int: Calculate the squared Euclidean distance
        between two locations to avoid floating point calculations.
        get_symbol() -> str: Returns the symbol "A" for AngrySlug.
        get_name() -> str: Returns the name of the AngrySlug "AngrySlug".
        __repr__() -> str: Returns the type name of this object.
    """
    def __init__(self) -> None:
        super().__init__(5)  # AngrySlug always has max_health of 5
        self.equip(PoisonSword())  # Equip PoisonSword weapon

    def choose_move(
            self,
            candidates: list[tuple[int, int]],
            current_position: tuple[int, int],
            player_position: tuple[int, int]
    ) -> tuple[int, int]:
        # Use a lambda to determine the closest position and a tuple as a
        # tiebreaker if the distance is the same
        return min(
            candidates + [current_position],
            key=lambda pos: (self.squared_distance(pos, player_position), pos)
        )

    def squared_distance(self, pos1: tuple[int, int],
                         pos2: tuple[int, int]) -> int:
        # Calculate squared Euclidean distance to avoid floating point calculations
        x1, y1 = pos1
        x2, y2 = pos2
        return (x1 - x2) ** 2 + (y1 - y2) ** 2

    def get_symbol(self) -> str:
        return "A"

    def get_name(self) -> str:
        return "AngrySlug"

    def __repr__(self) -> str:
        return self.__class__.__name__ + "()"


"""
4.1.12 ScaredSlug(Slug)
"""


class ScaredSlug(Slug):
    """
    Represents a slug (ScaredSlug) that is afraid of the player, inherited
    from the Slug class.

    ScaredSlug has a maximum health of 3 and is equipped with a PoisonDart
    as a weapon.s
    It selects the farthest move position based on the player's position and
    uses squared distances for comparison, thus avoiding floating point
    calculations.

    Properties inherited from Slug class:
        turn_count (int): Round counter, used to determine whether the slug
        can move in the current round.
        _max_health (int): Max health, fixed to 3 for ScaredSlug.
        _weapon (Weapon): Equipped with PoisonDart weapon.

    Methods:
        choose_move() -> tuple[int, int]: Choose the furthest movement location
        based on the player's position.
        squared_distance() -> int: Calculate the squared Euclidean distance
        between two locations to avoid floating point calculations.
        get_symbol() -> str: Returns the symbol "L" for ScaredSlug.
        get_name() -> str: Returns the name of the ScaredSlug "ScaredSlug".
        __repr__() -> str: Returns the type name of this object.
    """
    def __init__(self) -> None:
        super().__init__(3)  # ScaredSlug always has max_health of 3
        self.equip(PoisonDart())  # Equip PoisonDart weapon

    def choose_move(
            self,
            candidates: list[tuple[int, int]],
            current_position: tuple[int, int],
            player_position: tuple[int, int]
    ) -> tuple[int, int]:
        # Use a lambda to determine the furthest position and a tuple as a
        # tiebreaker if the distance is the same
        return max(
            candidates + [current_position],
            key=lambda pos: (self.squared_distance(pos, player_position), pos)
        )

    def squared_distance(self, pos1: tuple[int, int],
                         pos2: tuple[int, int]) -> int:
        x1, y1 = pos1
        x2, y2 = pos2
        """
        Use squared distance to compare distances 
        without needing to take square root
        """
        return (x1 - x2) ** 2 + (y1 - y2) ** 2

    def get_symbol(self) -> str:
        return "L"

    def get_name(self) -> str:
        return "ScaredSlug"

    def __repr__(self) -> str:
        return self.__class__.__name__ + "()"


"""
4.1.13 SlugDungeonModel()
"""


class SlugDungeonModel:
    """
    SlugDungeonModel Responsible for managing the game map, players,
    slugs and game turn logic.

    This category contains a variety of methods for managing game state,
    including slug movement, attack, and turn end logic,
    and handling player interaction with the map.

    Property:
        _tiles (list[list[Tile]]): A list of tiles on the map.
        _slugs (dict[tuple[int, int], Slug]): A dictionary of the locations and
        entities of all slugs on the map.
        _player (Player): Player entity.
        _player_position (tuple[int, int]): The player's current position
        on the map.
        _prev_player_position (tuple[int, int]): The player's position
        during the previous turn, used to track player movement.
    """
    def __init__(self,
                 tiles: list[list[Tile]],
                 slugs: dict[tuple[int, int], Slug],
                 player: Player,
                 player_position: tuple[int, int]) -> None:
        self._tiles = tiles
        self._slugs = slugs.copy()
        self._player = player
        self._player_position = player_position
        self._prev_player_position = player_position

    def get_tiles(self) -> list[list[Tile]]:
        return self._tiles

    def get_slugs(self) -> dict[tuple[int, int], Slug]:
        return self._slugs

    def get_player(self) -> Player:
        return self._player

    def get_player_position(self) -> tuple[int, int]:
        return self._player_position

    def get_tile(self, position: tuple[int, int]) -> Tile:
        row, col = position
        return self._tiles[row][col]

    def get_dimensions(self) -> tuple[int, int]:
        return len(self._tiles), len(self._tiles[0]) if self._tiles else 0

    def get_slug_position(self, slug: Slug) -> tuple[int, int]:
        """Get the current position of a specified slug from _slugs"""
        for pos, s in self._slugs.items():
            if s is slug:
                return pos
        return None  # If not found, returns None

    def get_valid_slug_positions(self, slug: Slug) -> list[tuple[int, int]]:
        """
        Returns a list of valid locations that the slug can move to.

        If the slug cannot move, or its position is invalid, the current position is returned.

        parameter:
            slug (Slug): To calculate the effective position of the slug.

        Return value:
            list[tuple[int, int]]: List of locations that can be moved to.
            If there is no valid position, return the current position.
        """
        if not slug.can_move():
            return []

        slug_position = self.get_slug_position(slug)
        if slug_position is None:
            return []

        row, col = slug_position

        potential_positions = [
            (row, col),  # The current location is also considered a potential location
            (row - 1, col),
            (row + 1, col),
            (row, col - 1),
            (row, col + 1),
        ]

        valid_positions = []
        max_row, max_col = self.get_dimensions()

        for pos in potential_positions:
            r, c = pos
            if 0 <= r < max_row and 0 <= c < max_col:
                tile = self.get_tile(pos)
                # Check if the location is valid: no blockers, no other slugs, and not a player location
                if not tile.is_blocking() and (
                        pos not in self._slugs or pos == slug_position) and pos != self._player_position:
                    valid_positions.append(pos)

        return valid_positions if valid_positions else [
            slug_position]  # Guaranteed to return at least the current position

    def perform_attack(self, entity: Entity, position: tuple[int, int]) -> None:
        weapon = entity.get_weapon()
        if not weapon:
            return

        effect = entity.get_weapon_effect()
        for target_position in weapon.get_targets(position):
            if isinstance(entity, Player) and target_position in self._slugs:
                self._slugs[target_position].apply_effects(effect)
            elif isinstance(entity,
                            Slug) and target_position == self._player_position:
                self._player.apply_effects(effect)  # Make sure the effect is applied to the player

    def end_turn(self) -> None:
        """
        Handle logic at the end of each game round, including:
            - Apply poison effect to player
            - Move the movable slug
            - Check for dead slugs and remove them
            - Slugs attack

        Return:
            None: This method does not return any value.
        """
        # Apply poison to player (Apply only once)
        self._player.apply_poison()

        # Copy the current slugs dictionary to avoid modifying the original dictionary while iterating
        slugs_copy = self._slugs.copy()
        slugs_to_remove = []

        # Deal with toxins and death first
        for position, slug in slugs_copy.items():
            slug.apply_poison()
            if not slug.is_alive():
                # Drop weapon on the tile if slug dies
                tile = self.get_tile(position)
                if slug.get_weapon():
                    tile.set_weapon(slug.get_weapon())
                slugs_to_remove.append(
                    position)  # Mark this slug for removal later

        # Remove dead slugs
        for position in slugs_to_remove:
            del self._slugs[position]

        # Move the movable slug
        slugs_copy = self._slugs.copy()  # Copy the slugs again after updating
        for position, slug in slugs_copy.items():
            if slug.can_move():
                # Get valid mobile location
                valid_positions = self.get_valid_slug_positions(slug)
                if valid_positions:
                    # Use choose_move to choose the slug's moving position, based on squared_distance
                    new_position = slug.choose_move(valid_positions, position,
                                                    self._prev_player_position)
                    # Update the slug's position
                    del self._slugs[position]
                    self._slugs[new_position] = slug
                else:
                    # If there is no moveable position, keep the slug in place
                    self._slugs[position] = slug

            # Each slug ends its turn
            slug.end_turn()

        # Slug performs attack
        for position, slug in self._slugs.items():
            self.perform_attack(slug, position)

        # Record the player's last position at the end of the round
        self._prev_player_position = self._player_position

    def handle_player_move(self, position_delta: tuple[int, int]) -> None:
        new_position = (self._player_position[0] + position_delta[0],
                        self._player_position[1] + position_delta[1])

        if self.is_valid_position(new_position):
            self._player_position = new_position

            tile = self.get_tile(new_position)
            weapon = tile.get_weapon()
            if weapon:
                self._player.equip(weapon)
                tile.remove_weapon()

            self.perform_attack(self._player, new_position)
            self.end_turn()

    def is_valid_position(self, position: tuple[int, int]) -> bool:
        row, col = position
        max_row, max_col = self.get_dimensions()
        return (0 <= row < max_row and 0 <= col < max_col and
                not self.get_tile(position).is_blocking() and
                position not in self._slugs)

    def has_won(self) -> bool:
        return not self._slugs and self.get_tile(self._player_position).__str__() == "G"

    def has_lost(self) -> bool:
        return not self._player.is_alive()


"""
4.1.14 load level(filename: str) -> SlugDungeonModel
"""


def load_level(filename: str) -> SlugDungeonModel:
    """
    Load the game level from the given file and create the
    corresponding map model.

    This function will read the level data from the specified file, generate
    tiles, players and various Slug enemies on the map based on the symbols in
    the file, and finally return a complete `SlugDungeonModel`

    File format:
    - The first line contains the player's maximum health.
    - Starting from the second line, each line represents a line of the map,
      and the corresponding map elements are generated based on the symbols:
        - "#"：Wall tiles (blocking).
        - "G"：Target tile (not blocking).
        - "P"：The player's position.
        - "A"：Generate AngrySlug.
        - "N"：Generate NiceSlug.
        - "L"：Generate ScaredSlug.
        - Other symbols: Use the `create_tile` function to generate
          corresponding tiles.

    parameter:
        filename (str): The path to the file containing the level data.

    Return value:
        SlugDungeonModel: Returns a model containing map tiles, slug enemies,
        players, and player positions.
    """
    tiles = []
    slugs = {}
    player = None
    player_position = None

    # Read file contents
    with open(filename, 'r') as file:
        lines = file.readlines()

    # The first line provides the player's max_health
    player_max_health = int(lines[0].strip())
    player = Player(player_max_health)

    """
    Starting from the second line, 
    parse the map and check the positions of weapons and entities
    """
    for row_index, line in enumerate(lines[1:]):
        tile_row = []
        for col_index, symbol in enumerate(line.strip('\n')):
            position = (row_index, col_index)

            # Creates a blank floor tile by default
            tile = create_tile(" ")

            if symbol == "#":
                tile = create_tile("#")  # wall
            elif symbol == "G":
                tile = create_tile("G")  # target floor tiles
            elif symbol == "P":
                player_position = position
            elif symbol == "A":
                slugs[position] = AngrySlug()
            elif symbol == "N":
                slugs[position] = NiceSlug()
            elif symbol == "L":
                slugs[position] = ScaredSlug()
            else:
                tile = create_tile(symbol)

            tile_row.append(tile)
        tiles.append(tile_row)

    return SlugDungeonModel(tiles, slugs, player, player_position)


"""
4.2.1 DungeonMap(AbstractGrid)
"""


class DungeonMap(AbstractGrid):
    """
    The DungeonMap class inherits from AbstractGrid and is responsible for
    drawing the game map, player and slug positions.

    This class uses the provided map tiles, player position, and slug position
    to dynamically clear and redraw the map.

    Attributes:
        master: The parent window or canvas object, usually a Tkinter element.
        dimensions (tuple[int, int]): The number of rows and columns of the map.
        size (tuple[int, int]): The dimensions of the drawing area
        (width, height).

    Methods:
        redraw(tiles, player_position, slugs) -> None: Clear and redraw the map,
        including tiles, players and slugs.
    """
    def __init__(self, master, dimensions: tuple[int, int],
                 size: tuple[int, int]):
        super().__init__(master, dimensions, size)
        self.config(width=size[0], height=size[1])
        self.pack(side="left", padx=0, pady=0)

    def redraw(self, tiles: list[list[str]], player_position: tuple[int, int],
               slugs: dict[tuple[int, int], str]) -> None:
        """Clears and redraws the map based on the positions of the provided
        tiles, player_position and slugs"""
        # Clear current map
        self.clear()

        # Draw floor tiles
        for row in range(len(tiles)):
            for col in range(len(tiles[row])):
                tile = tiles[row][col]
                bbox = self.get_bbox((row, col))
                # Get the bounds of the current cell

                if tile.is_blocking():
                    self.create_rectangle(bbox,
                                          fill=WALL_COLOUR)  # Drawing walls
                elif str(tile) == GOAL_TILE:
                    self.create_rectangle(bbox,
                                          fill=GOAL_COLOUR)  # Draw goal tile
                else:
                    self.create_rectangle(bbox,
                                          fill=FLOOR_COLOUR)  # Draw floor tiles

                weapon = tile.get_weapon()
                if weapon:
                    self.annotate_position((row, col), weapon.get_symbol(),
                                           font=REGULAR_FONT)

            # Draw Slugs
            for slug_position, slug in slugs.items():
                sx, sy = slug_position
                slug_bbox = self.get_bbox((sx, sy))

                if slug.can_move():
                    slug_colour = 'light pink'
                    # If the slug can move, it will be pink in color
                else:
                    slug_colour = 'green'

                self.create_oval(slug_bbox, fill=slug_colour)

                if isinstance(slug, AngrySlug):  # Angry Slug's symbol
                    self.annotate_position((sx, sy), "Angry\nSlug",
                                           font=REGULAR_FONT)
                elif isinstance(slug, NiceSlug):  # Nice Slug's symbol
                    self.annotate_position((sx, sy), "Nice\nSlug",
                                           font=REGULAR_FONT)
                elif isinstance(slug, ScaredSlug):  # Scared Slug's symbol
                    self.annotate_position((sx, sy), "Scared\nSlug",
                                           font=REGULAR_FONT)
                else:
                    self.annotate_position((sx, sy), "?", font=REGULAR_FONT)

            # Draw the player last, ensuring the player is on top
            px, py = player_position
            player_bbox = self.get_bbox((px, py))
            self.create_oval(player_bbox, fill=PLAYER_COLOUR)
            # Use blue circles to represent players
            self.annotate_position((px, py), "Player",
                                   font=REGULAR_FONT)  # Indicate player


"""
4.2.2 DungeonInfo(AbstractGrid)
"""


class DungeonInfo(AbstractGrid):
    """
    The DungeonInfo class inherits from AbstractGrid and is responsible for
    displaying status information tables of entities and players.

    This class uses the provided entity information to update and draw the
    status of every entity in the game, such as name, location, weapon, health,
    and poison status.

    Attributes:
        master: The parent window or canvas object, usually a Tkinter element.
        dimensions (tuple[int, int]): The number of rows and columns of the
        status information table.
        size (tuple[int, int]): The dimensions of the drawing area
        (width, height).
        side (str): Which side of the window the table is displayed on,
        defaults to "right".

    Methods:
        redraw(entities) -> None: Clears and repaints state information
        for all entities.
        redraw_player(player_info) -> None: Clears and displays player
        status information.
        I separate the redraw into 2 redraws because it's easier to use in 4.3.1
        And it is clear to understand the different info, although the codes are
        similar.
    """
    def __init__(self, master, dimensions: tuple[int, int],
                 size: tuple[int, int], side: str = "right"):
        super().__init__(master, dimensions, size)
        self.config()

    def redraw(self, entities: dict[Position, dict]) -> None:
        self.clear()
        """Clear and redraw the table based on the provided entity information"""
        # draw header
        headers = ["Name", "Position", "Weapon", "Health", "Poison"]
        for col, header in enumerate(headers):
            self.annotate_position((0, col), header, font=TITLE_FONT)

        # Draw information about each entity
        for row, (position, entity) in enumerate(entities.items(), start=1):
            entity_info = [
                entity.get("name", "Unknown"),
                str(position),
                entity.get("weapon", "None"),
                str(entity.get("health", "N/A")),
                str(entity.get("poison", 0))
            ]
            for col, info in enumerate(entity_info):
                self.annotate_position((row, col), info, font=REGULAR_FONT)

    def redraw_player(self, player_info: dict) -> None:
        self.clear()
        """Display player status information"""
        # draw header
        headers = ["Name", "Position", "Weapon", "Health", "Poison"]
        for col, header in enumerate(headers):
            self.annotate_position((0, col), header, font=TITLE_FONT)

        # Show player information
        player_data = [
            player_info.get("name", "Player"),
            str(player_info.get("position", (0, 0))),
            player_info.get("weapon", "None"),
            str(player_info.get("health", "N/A")),
            # Dynamically obtain the player's health value
            str(player_info.get("poison", "0"))
        ]

        for col, data in enumerate(player_data):
            self.annotate_position((1, col), data, font=REGULAR_FONT)


"""
4.2.3 ButtonPanel(tk.Frame)
"""


class ButtonPanel(tk.Frame):
    def __init__(self, root: tk.Tk, on_load: Callable, on_quit: Callable) -> \
            None:
        """
        The ButtonPanel class inherits from tk.Frame and is responsible for
        creating a panel containing "Load Game" and "Exit Game" buttons.

        This panel is located at the bottom of the window.
        After the button is clicked, the provided callback function is called
        to perform the corresponding operation.

        Attributes:
            root (tk.Tk): Tkinter The root window or main window.
            on_load (Callable): Callback function executed when the "Load Game"
            button is clicked.
            on_quit (Callable): Callback function executed when the "Exit Game"
            button is clicked.

        Methods:
            __init__(root, on_load, on_quit) -> None: Initialize the panel
            and set the buttons.s
        """
        super().__init__(root)
        self.config(width=900, height=50)
        self.pack(side="bottom", fill='x', pady=10)

        # Create an inner frame to place the button
        button_frame = tk.Frame(self)
        button_frame.pack()

        # Load game button
        load_button = tk.Button(button_frame, text="Load Game", command=on_load)
        load_button.pack(side="left", padx=20, pady=10)

        # Exit game button
        quit_button = tk.Button(button_frame, text="Quit", command=on_quit)
        quit_button.pack(side="left", padx=20, pady=10)


"""
4.3.1 SlugDungeon()
"""


class SlugDungeon:
    """
    The SlugDungeon class is responsible for managing game logic, map drawing,
    player and slug status updates, and handling player input.

    This class interacts with the game model through the Tkinter GUI,
    dynamically displays the game's map, player, and slug status and
    responds to key input.

    Attribute:
        root (tk.Tk): Tkinter's root or main window.
        current_level (str): The file name of the currently loaded game level.
        model (SlugDungeonModel): A model representing the game state,
        containing player, slug, and map information.
        main_frame (tk.Frame): The main frame, containing the map and
        other views.
        dungeon_map (DungeonMap): The canvas responsible for displaying the map.
        dungeon_info_slugs (DungeonInfo): Table showing slug status.
        player_info_panel (DungeonInfo): A table showing player status.
        button_panel (ButtonPanel): Panel containing "Load Game" and
        "Exit Game" buttons.

    Methods:
        redraw() -> None: Redraw map and status information.
        handle_key_press(event) -> None: Handles player key input.
        load_game() -> None: Load the game files and restart the game.
        quit_game() -> None: Exit the game and close the window.s
    """
    def __init__(self, root: tk.Tk, filename: str) -> None:
        self.root = root
        self.current_level = filename
        self.model = load_level(filename)

        # Create the main frame, containing all views
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill='both', expand=True)

        # Set map size and spiral biometric size
        self.DUNGEON_MAP_SIZE = (500, 500)
        self.SLUG_INFO_SIZE = (400, 500)
        self.PLAYER_INFO_SIZE = (900, 100)

        # Bind key event
        root.bind("<Key>", self.handle_key_press)

        # Call redraw for layout and redrawing
        self.redraw()

    def redraw(self) -> None:
        """Redraw the view based on the current model's state"""

        # Clear previous layout
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Create the upper frame, containing the map and spiral bio information
        top_frame = tk.Frame(self.main_frame)
        top_frame.pack(side="top", fill='both', expand=True)

        # Create maps and spiral biological information
        self.dungeon_map = DungeonMap(top_frame, self.model.get_dimensions(),
                                      self.DUNGEON_MAP_SIZE)
        self.dungeon_info_slugs = DungeonInfo(top_frame, (7, 5),
                                              self.SLUG_INFO_SIZE)

        # Layout map and spiral bio information
        self.dungeon_map.pack(side="left", fill='both', expand=True)
        self.dungeon_info_slugs.pack(side="right", fill='both', expand=True)

        # Create the lower frame containing player information and button panels
        bottom_frame = tk.Frame(self.main_frame)
        bottom_frame.pack(side="top", fill='x')

        # Player information panel, placed above the button panel
        self.player_info_panel = DungeonInfo(bottom_frame, (2, 5),
                                             self.PLAYER_INFO_SIZE)
        self.player_info_panel.pack(side="top", fill='x')

        # Create a button panel and place it at the bottom
        self.button_panel = ButtonPanel(bottom_frame, self.load_game,
                                        self.quit_game)
        self.button_panel.pack(side="bottom", fill='x', pady=10)

        # Get game status information
        tiles = self.model.get_tiles()
        player_position = self.model.get_player_position()
        health = self.model.get_player().get_health()

        # Create slug dictionary
        slugs = {pos: slug for pos, slug in
                 self.model.get_slugs().items()}
                 # Use the slug instance directly

        # Update map dimensions (if needed)
        map_dimensions = (len(tiles), len(tiles[0]))
        self.dungeon_map.set_dimensions(map_dimensions)

        # Redraw the map
        self.dungeon_map.redraw(tiles, player_position, slugs)

        # Redraw information about spiral creatures
        slugs_info = {
            pos: {
                "name": slug.get_name(),
                "weapon": str(slug.get_weapon()) if slug.get_weapon()
                else "None",
                "health": slug.get_health(),
                "poison": slug.get_poison()
            } for pos, slug in self.model.get_slugs().items()
        }
        self.dungeon_info_slugs.redraw(slugs_info)

        # Redraw player information
        player_info = {
            "name": self.model.get_player().get_name(),
            "position": player_position,
            "weapon": str(self.model.get_player().get_weapon())
            if self.model.get_player().get_weapon() else "None",
            "health": health,
            "poison": self.model.get_player().get_poison()
        }
        self.player_info_panel.redraw_player(player_info)

    def load_level(filename: str) -> SlugDungeonModel:
        """Load game from file and return model"""
        return load_level(filename)

    def handle_key_press(self, event: tk.Event) -> None:
        """
        Handle the player's key input and check the game state immediately
        after the key press is processed.
        """
        key = event.char.lower()

        # Handling player keystrokes
        if key == 'w':
            # move up
            self.model.handle_player_move((-1, 0))
        elif key == 's':
            # move down
            self.model.handle_player_move((1, 0))
        elif key == 'a':
            # move left
            self.model.handle_player_move((0, -1))
        elif key == 'd':
            # move right
            self.model.handle_player_move((0, 1))
        elif key == ' ':
            # attack
            current_position = self.model.get_player_position()
            self.model.perform_attack(self.model.get_player(), current_position)
            self.model.end_turn()

        # Update the view and force a redraw,
        # ensuring that the view is updated before the message box appears.
        self.redraw()
        self.root.update_idletasks()

        # Check game status
        if self.model.has_won():
            # player wins game
            response = messagebox.askyesno(WIN_TITLE, WIN_MESSAGE)
            # Ask if you want to play again
            if response:
                # Reload game initial state
                self.model = load_level(self.current_level)
                self.redraw()
            else:
                self.root.destroy()
                # The player chooses not to replay and closes the game

        elif not self.model.get_player().is_alive():
            # player loses game
            response = messagebox.askyesno(LOSE_TITLE, LOSE_MESSAGE)
            # Ask if you want to play again
            if response:
                # Reload game initial state
                self.model = load_level(self.current_level)
                self.redraw()
            else:
                self.root.destroy()
                # The player chooses not to replay and closes the game

    def quit_game(self) -> None:
        """quit game"""
        self.root.destroy()

    def load_game(self) -> None:
        """Handles loading game from file"""
        filename = filedialog.askopenfilename(title="Select game file")
        if filename:
            self.current_level = filename
            self.model = load_level(filename)  # Call static method
            self.redraw()


def play_game(root: tk.Tk, file_path: str) -> None:
    """
    A function that runs the game, taking the root window and file path as
    arguments, and starts the game.
    """
    root.title("Slug Dungeon")
    game_controller = SlugDungeon(root, file_path)
    root.mainloop()


def main():
    """
    The main entrance to the program, launching the game's graphical user
    interface (GUI) and requesting the selection of a level file.

    This function initializes a Tkinter root window and uses a file dialog
    to let the user select a game level file.
    If the user selects a file, the `play_game` function will be called to
    start the game.
    If no file is selected, the program prints the message and exits.

    No parameters.

    Return value:
        None: This function does not return any value.
    """
    root = tk.Tk()
    file_path = filedialog.askopenfilename(title="Select Game File")

    if file_path:
        play_game(root, file_path)
    else:
        print("No file selected. Exiting...")

if __name__ == "__main__":
    main()