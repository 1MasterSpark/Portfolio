import pygame
import math
import random
pygame.init()

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.lines = []  # List to keep track of connected lines

    def draw(self, surface):        
        pygame.draw.circle(surface, (0, 0, 0), (self.x, self.y), 5)

class Line():
    def __init__(self):
        self.startpoint = None
        self.endpoint = None
        self.traced = False  # Flag to track if the line has been traced
        self.angle = 0
        self.color = (255, 0, 0)

    def set_startpoint(self, point):
        self.startpoint = point
        point.lines.append(self)  # Add the line to the startpoint's lines array

    def set_endpoint(self, point):
        self.endpoint = point
        point.lines.append(self)  # Add the line to the endpoint's lines array

    def draw(self, surface):
        if self.startpoint and self.endpoint:
            pygame.draw.line(surface, self.color, (self.startpoint.x, self.startpoint.y), (self.endpoint.x, self.endpoint.y), 5)

def draw_button(color, text, x, y):
    rect = pygame.Rect(x, y, 180, 90)
    pygame.draw.rect(screen, color, rect)
    text = pygame.font.SysFont(None, 36).render(text, True, (0, 0, 0))
    screen.blit(text, (x + 90 - text.get_width() / 2, y + 45 - text.get_height() / 2))
    return rect

def distance(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

def angle_between_points(p1, p2):
    return math.atan2(p2.y - p1.y, p2.x - p1.x)

def check_even_lines(points):
    # Check if each point's lines array has an even count
    for point in points:
        if len(point.lines) % 2 != 0:
            return False  # There's at least one point with an odd number of lines

    return True  # All points have an even number of lines

def trace_line(line, current_color, current_point=None):
    # Mark the line as traced
    line.traced = True
    line.color = current_color
    next_line = None
    otherpoint = None

    if not current_point:
        current_point = line.endpoint
    elif current_point == line.endpoint:
        current_point = line.startpoint
    elif current_point == line.startpoint:
        current_point = line.endpoint

    for eachline in current_point.lines:
        if current_point == eachline.endpoint:
            otherpoint = eachline.startpoint
        else:
            otherpoint = eachline.endpoint
        eachline.angle = angle_between_points(current_point, otherpoint)

    # Sort the lines at the current point by angle
    sorted_lines = sorted(current_point.lines, key=lambda l: l.angle)

    # Find the next line by finding the current line's index in sorted_lines
    current_line_index = sorted_lines.index(line)
    next_line_index = (current_line_index + (len(sorted_lines) // 2)) % len(sorted_lines)
    next_line = sorted_lines[next_line_index]

    if not next_line.traced:
        # Continue tracing recursively
        trace_line(next_line, current_color, current_point)

def render_multiline_text(text, font, color, max_width):
    # Splits text into multiple lines so it doesn't go off the screen
    words = text.split(' ')
    lines = []
    current_line = ''

    for word in words:
        test_line = f"{current_line} {word}".strip()
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    line_surfaces = [font.render(line, True, color) for line in lines]
    height = sum(s.get_height() for s in line_surfaces)
    surface = pygame.Surface((max_width, height), pygame.SRCALPHA)
    y = 0
    for s in line_surfaces:
        surface.blit(s, (0, y))
        y += s.get_height()
    return surface

def count_closed_loops(lines):
    closed_loops = 0

    for line in lines:
        if not line.traced:
            current_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            # Start tracing a new line
            trace_line(line, current_color)
            closed_loops += 1

    for line in lines:
        line.traced = False

    return closed_loops

points = []
lines = []
current_mode = 'point'
current_line = Line()

screen = pygame.display.set_mode([700, 500])
screen.fill((0, 0, 255))

# Add buttons and variables
points_button = draw_button((0, 255, 0), "Add points", 510, 10)
lines_button = draw_button((0, 255, 0), "Add lines", 510, 110)
loops_button = draw_button((0, 255, 0), "Count loops", 510, 210)
clear_button = draw_button((0, 255, 0), "Clear", 510, 310)
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 72)
loops_text = "Closed loops:"
loops = 0
error_mode = False

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                current_mode = 'point'
            elif event.key == pygame.K_l:
                current_mode = 'line'
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if points_button.collidepoint(x, y):
                current_mode = 'point'
            elif lines_button.collidepoint(x, y):
                current_mode = 'line'
            elif loops_button.collidepoint(x, y):
                if check_even_lines(points):
                    # Count and print the number of closed loops
                    loops = count_closed_loops(lines)
                    loops_text = "Closed loops:"
                    error_mode = False
                else:
                    loops_text = "Error: There are points with an odd number of lines"
                    loops = 0
                    error_mode = True
            elif clear_button.collidepoint(x, y):
                points = []
                lines = []
                loops = 0
                loops_text = "Closed loops:"
                error_mode = False

            elif 0 <= x <= 500 and 0 <= y <= 500:
                if current_mode == 'point':
                    new_point = Point(x, y)
                    points.append(new_point)
                elif current_mode == 'line':
                    # Find the nearest point
                    if points:
                        nearest_point = min(points, key=lambda point: distance(point.x, point.y, x, y))
                        if distance(nearest_point.x, nearest_point.y, x, y) > 50:
                            new_point = Point(x, y)
                            points.append(new_point)
                            nearest_point = new_point
                        if not current_line.startpoint:
                            current_line.set_startpoint(nearest_point)
                        else:
                            current_line.set_endpoint(nearest_point)
                            lines.append(current_line)
                            current_line = Line()  # Reset the current line after drawing
                    else:
                        new_point = Point(x, y)
                        points.append(new_point)
                        current_line.set_startpoint(new_point)

    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(0, 0, 500, 500))
    pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(500, 400, 200, 500))
    point_surface = pygame.Surface((500, 500), pygame.SRCALPHA)
    line_surface = pygame.Surface((500, 500), pygame.SRCALPHA)

    for line in lines:
        line.draw(line_surface)
    for point in points:
        point.draw(point_surface)

    if error_mode:
        text_surface = render_multiline_text(loops_text, font, (255, 0, 0), 190)
        screen.blit(text_surface, (505, 405))
    else:
        text1_surface = font.render(loops_text, True, (255, 255, 255))
        text2_surface = big_font.render(str(loops), True, (255, 255, 255))
        screen.blit(text1_surface, (510, 410))
        screen.blit(text2_surface, (510, 440))
    screen.blit(line_surface, (0, 0))
    screen.blit(point_surface, (0, 0))

    if current_mode == 'line' and current_line.startpoint:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_x < 500:  # Only draw in the drawing area
            pygame.draw.line(screen, (255, 0, 0), (current_line.startpoint.x, current_line.startpoint.y), (mouse_x, mouse_y), 5)
    pygame.display.flip()

pygame.quit()