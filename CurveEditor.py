import BezierCurve as bc
import pygame


class CurveEditor:
    def __init__(self, debug_point_size: int = 6):
        self.curve: bc.BezierCurve = None
        self.selected_point: tuple[int, int] = (None, 0)
        self.is_creating = False
        self.debug_point_size = debug_point_size

    def on_mouse_up(self, button: int):
        if button != 1:
            return

        x, y = pygame.mouse.get_pos()

        if self.curve is None:
            self.is_creating = True
            self.curve = bc.BezierCurve([bc.BezierCurvePoint(x, y, x, y)])
            self.curve.pts.append(bc.BezierCurvePoint(x, y, x, y))
            self.selected_point = (1, 0)
        elif self.is_creating:
            self.curve.pts.append(bc.BezierCurvePoint(x, y, x, y))
            self.selected_point = (len(self.curve.pts) - 1, 0)
        else:
            self.selected_point = (None, 0)

    def on_mouse_down(self, button: int):
        if button != 1 or self.curve is None:
            return

        x, y = pygame.mouse.get_pos()

        if self.is_creating:
            self.selected_point = (self.selected_point[0], 1)
        elif self.selected_point == (None, 0):
            for i in range(len(self.curve.pts)):
                dist = (self.curve.pts[i].x - x) ** 2 + (self.curve.pts[i].y - y) ** 2
                control_dist = (self.curve.pts[i].control_x - x) ** 2 + (self.curve.pts[i].control_y - y) ** 2
                opposite_control_dist = (self.curve.pts[i].opposite_control_point()[0] - x) ** 2 + (
                        self.curve.pts[i].opposite_control_point()[1] - y) ** 2

                if control_dist < self.debug_point_size ** 2:
                    self.selected_point = (i, 1)
                    break
                elif opposite_control_dist < self.debug_point_size ** 2:
                    self.selected_point = (i, 2)
                    break
                elif dist < self.debug_point_size ** 2:
                    self.selected_point = (i, 0)
                    break

    def on_mouse_moved(self):
        if self.curve is None:
            return

        x, y = pygame.mouse.get_pos()

        if self.selected_point != (None, 0):
            if self.selected_point[1] == 0:
                self.curve.pts[self.selected_point[0]] = self.curve.pts[self.selected_point[0]].translated(
                    x - self.curve.pts[self.selected_point[0]].x,
                    y - self.curve.pts[self.selected_point[0]].y)
            elif self.selected_point[1] == 1:
                self.curve.pts[self.selected_point[0]].control_x = x
                self.curve.pts[self.selected_point[0]].control_y = y
            elif self.selected_point[1] == 2:
                self.curve.pts[self.selected_point[0]].control_x = self.curve.pts[self.selected_point[0]].x - (
                        x - self.curve.pts[self.selected_point[0]].x)
                self.curve.pts[self.selected_point[0]].control_y = self.curve.pts[self.selected_point[0]].y - (
                        y - self.curve.pts[self.selected_point[0]].y)

    def on_key_pressed(self, key: int):
        if self.curve is None:
            return

        if key == pygame.K_ESCAPE:
            self.selected_point = (None, 0)
            self.is_creating = False
            self.curve.pts.pop(len(self.curve.pts) - 1)
        elif key == pygame.K_DELETE or key == pygame.K_BACKSPACE:
            self.curve.pts.pop(len(self.curve.pts) - 1)

    def draw_editing(self, screen: pygame.Surface, line_color: pygame.Color = pygame.Color(0, 0, 0),
                     line_width: int = 3, edit_color: pygame.Color = pygame.Color(255, 0, 0),
                     edit_width: int = 1):
        if self.curve is not None:
            self.curve.draw(screen, line_color, line_width)
            self.curve.draw_debug(screen, edit_color, edit_width)

    def draw(self, screen):
        self.curve.draw(screen, pygame.Color(0, 0, 0), 3)
