import pygame

import BezierCurve
import CurveEditor
import Track
import Camera
import time
import Car


def build_track(open_saved: bool = False):
    editor = CurveEditor.CurveEditor()

    if open_saved:
        with open('track.txt', 'r') as f:
            editor.curve = BezierCurve.BezierCurve.deserialize(f.read())

    mouse_down_pos = [None, None, None]

    pygame.init()

    screen = pygame.display.set_mode([500, 500])

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button <= 3:
                    mouse_down_pos[event.button - 1] = (event.pos[0], event.pos[1])
                    editor.on_mouse_down(event.button)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button <= 3:
                    mouse_down_pos[event.button - 1] = None
                    editor.on_mouse_up(event.button)
            elif event.type == pygame.MOUSEMOTION:
                editor.on_mouse_moved()
            elif event.type == pygame.KEYDOWN:
                editor.on_key_pressed(event.key)
                
                if event.key == pygame.K_RETURN:
                    with open('track.txt', 'w') as f:
                        f.write(editor.curve.serialize())
                    running = False

        screen.fill((255, 255, 255))

        editor.draw_editing(screen, pygame.Color(0, 0, 0), 3)

        pygame.display.update()

    pygame.quit()


def main(load_weights: bool = False, camera_option: int = 0, select_count: int = 2, fixed_frame: bool = False, ai_count: int = 10, approx_intersect: bool = False):
    
    pygame.init()

    screen = pygame.display.set_mode([800, 600])

    # init entities
    track = Track.Track('track.txt', 100)
    player_car = Car.PlayerCar(camera_option == MainOptions.PLAYER)
    player_car.set_track_data(track)

    ai_cars = [Car.AICar(approx_intersect) for _ in range(ai_count)]
    if not load_weights:
        for car in ai_cars:
            car.set_track_data(track)
    else:
        with open('weights.txt', 'r') as f:
            weights = f.read().splitlines()
            for i, car in enumerate(ai_cars):
                car.set_track_data(track)
                car.nn.from_string(weights[i % 2])
                car.nn.mutate(0.1, 0.1)

    camera = Camera.Camera(screen, player_car if camera_option == MainOptions.PLAYER else None)

    running = True
    start_time = time.time()
    delta_time: float = 0
    fixed_dt = 0.032
    time_scale: float = 1
    acc_time: float = 0
    
    def next_iteration():
        Car.selection_and_reproduce(select_count, ai_cars)
        player_car.set_track_data(track)
        for car in ai_cars:
            car.set_track_data(track)
    
    while running:
        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    next_iteration()
                elif event.key == pygame.K_ESCAPE:
                    with open('weights.txt', 'w') as f:
                        f.write('\n'.join(str(car.nn) for car in sorted(ai_cars, key=lambda c: c.get_fitness(), reverse=True)[:2]))

        # next iteration
        if all(car.out_of_track for car in ai_cars) or acc_time > 120:
            next_iteration()
            acc_time = 0

        # updates
        if camera_option == MainOptions.FOLLOW_AI:
            Car.follow_best_ai_car(ai_cars, camera)
        player_car.update(fixed_dt, track)
        for car in ai_cars:
            if not car.out_of_track:
                car.update(fixed_dt, track)
        camera.update(fixed_dt)

        # draws
        screen.fill((255, 255, 255))

        track.draw(screen, pygame.Color(0, 0, 0), camera, 5)
        player_car.draw(screen, pygame.Color(0, 0, 0), camera)
        for car in ai_cars:
            car.draw(screen, pygame.Color(0, 0, 0), camera)

        pygame.display.update()

        # delta time
        end_time = time.time()
        delta_time = end_time - start_time
        
        if fixed_frame and delta_time < fixed_dt:
            time.sleep(fixed_dt - delta_time)

        end_time = time.time()
        delta_time = (end_time - start_time) * time_scale
        acc_time += fixed_dt
        start_time = end_time

    pygame.quit()


class MainOptions:
    PLAYER = 0
    FOLLOW_AI = 1
    FREE_CAM = 2
    
    def __init__(self, run_build_track: bool = False, camera_option: int = 0, select_count: int = 2, fixed_frame: bool = False,
                 ai_count: int = 10, approx_intersect: bool = True):
        if run_build_track:
            build_track()
        else:
            main(True, camera_option, select_count, fixed_frame, ai_count, approx_intersect)


if __name__ == "__main__":
    MainOptions(False, MainOptions.FOLLOW_AI, 2, False, 10, False)
