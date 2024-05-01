import sys
import pygame
import random
import numpy as np
from pygame_combat import run_pygame_combat
from pygame_human_player import PyGameHumanPlayer
from pygame_ai_player import PyGameAIPlayer
from battleLogs import battle_log

from pathlib import Path
from typing import List, Tuple

sys.path.append(str((Path(__file__) / ".." / "..").resolve().absolute()))

from lab2.cities_n_routes import get_randomly_spread_cities, get_routes
from lab3.travel_cost import get_route_cost, generate_terrain, route_to_coordinates
from lab5.landscape import get_landscape, elevation_to_rgba, get_elevation
from lab7.ga_cities import game_fitness, setup_GA, solution_to_cities
from lab11.sprite import Sprite

get_combat_bg = lambda pixel_map: elevation_to_rgba(
    get_elevation(pixel_map), "RdPu"
)

pygame.font.init()
game_font = pygame.font.SysFont("Comic Sans MS", 15)


def get_landscape_surface(size: Tuple[int, int]) -> pygame.Surface:
    landscape = get_landscape(size)
    print("Created a landscape of size", landscape.shape)
    pygame_surface = pygame.surfarray.make_surface(landscape[:, :, :3])
    return pygame_surface


def get_combat_surface(size: Tuple[int, int]) -> pygame.Surface:
    landscape = get_combat_bg(size)
    print("Created a landscape of size", landscape.shape)
    pygame_surface = pygame.surfarray.make_surface(landscape[:, :, :3])
    return pygame_surface


def setup_window(width: int, height: int, caption: str) -> pygame.Surface:
    pygame.init()
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption(caption)
    return window


def displayCityNames(city_locations: List[Tuple[int, int]], city_names: List[str]) -> None:
    for i, name in enumerate(city_names):
        text_surface = game_font.render(str(i) + " " + name, True, (0, 0, 150))
        screen.blit(text_surface, city_locations[i])

def route_is_real(routes, cities, city_idx1, city_idx2):
    city1 = tuple(cities[city_idx1])
    city2 = tuple(cities[city_idx2])
    for route in routes:
        route = tuple(map(tuple, route))
        if (city1 in route) and (city2 in route):
            return True
    return False


class State:
    def __init__(
        self,
        current_city: int,
        destination_city: int,
        travelling: bool,
        encounter_event: bool,
        cities: List[Tuple[int, int]],
        routes: List[Tuple[Tuple[int, int], Tuple[int, int]]],
    ):
        self.current_city = current_city
        self.destination_city = destination_city
        self.travelling = travelling
        self.encounter_event = encounter_event
        self.cities = cities
        self.routes = routes


if __name__ == "__main__":
    size = width, height = 640, 480
    black = 1, 1, 1
    start_city = 0
    end_city = 9
    sprite_path = "assets/lego.png"
    sprite_speed = 1
    landscape = get_landscape(size)

    screen = setup_window(width, height, "Game World Gen Practice")

    landscape_surface = get_landscape_surface(size)
    combat_surface = get_combat_surface(size)
    city_names = [
        "Morkomasto",
        "Morathrad",
        "Eregailin",
        "Corathrad",
        "Eregarta",
        "Numensari",
        "Rhunkadi",
        "Londathrad",
        "Baernlad",
        "Forthyr",
    ]

#    #GA implementation to get more realistic cities
#    elevation = get_elevation(size)
#    elevation = np.array(elevation)
#    elevation = (elevation - elevation.min()) / (elevation.max() - elevation.min())
#    fitness = lambda solution, idx: game_fitness(
#        solution, idx, elevation=elevation, size=size
#    )
#    fitness_function, ga_instance = setup_GA(fitness, len(city_names), size)
#    cities = solution_to_cities(ga_instance.initial_population[0], size)
#    ga_instance.run()
#
#    #set cities
#    city_locations = solution_to_cities(ga_instance.best_solution()[0], size(city_names))
#    routes = get_routes(city_locations)
    city_locations = get_randomly_spread_cities(size, len(city_names))
    routes = get_routes(city_locations)

    random.shuffle(routes)
    routes = routes[:10]

    player_sprite = Sprite(sprite_path, city_locations[start_city])

    humanPlayer = "-1"
    while(humanPlayer != "N" and humanPlayer != "Y"):
        humanPlayer = input("Would you like to play as the human player? Y/N: ")
    if (humanPlayer == "Y"):
        player = PyGameHumanPlayer
    if (humanPlayer == "N"):
        player = PyGameAIPlayer

    state = State(
        current_city=start_city,
        destination_city=start_city,
        travelling=False,
        encounter_event=False,
        cities=city_locations,
        routes=routes,
    )

    while True:
        action = player.selectAction(player, state)
        if 0 <= int(chr(action)) <= 9:
            if int(chr(action)) != state.current_city and not state.travelling:
                ''' 
                Check if a route exist between the current city and the destination city.
                '''
                start_city = state.current_city
                destination_city = int(chr(action))
                route = [(0,0),(0,0)]
                if route_is_real(routes, city_locations, start_city, destination_city):
                    start = city_locations[state.current_city]
                    route[0] = tuple(start)
                    state.destination_city = int(chr(action))
                    destination = city_locations[state.destination_city]
                    route[1] = tuple(destination)
                    player_sprite.set_location(city_locations[state.current_city])
                    state.travelling = True
                    print("Travelling from", state.current_city, "to", state.destination_city)
                else:
                    print("No available route")

        screen.fill(black)
        screen.blit(landscape_surface, (0, 0))

        for city in city_locations:
            pygame.draw.circle(screen, (255, 0, 0), city, 5)

        for line in routes:
            pygame.draw.line(screen, (255, 0, 0), *line)

        displayCityNames(city_locations, city_names)
        if state.travelling:
            state.travelling = player_sprite.move_sprite(destination, sprite_speed)
            state.encounter_event = random.randint(0, 1000) < 2
            if not state.travelling:
                print('Arrived at', state.destination_city)
                travel_cost = int(get_route_cost(route, landscape))
                if travel_cost < 5:
                    travel_cost = random.randint(2,5)
                print('Travel cost = {travel_cost}')
                #player.gold -= travel_cost
                print('Remaining gold = {player.gold}')

        if not state.travelling:
            encounter_event = False
            state.current_city = state.destination_city

        if state.encounter_event:
            run_pygame_combat(combat_surface, screen, player_sprite)
            print(battle_log())
            state.encounter_event = False
        else:
            player_sprite.draw_sprite(screen)
        pygame.display.update()
        if state.current_city == end_city:
            print('You have reached the end of the game!')
            break
