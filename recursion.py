import pygame
import random
import sys
import colorsys

# --- GLOBAL CONSTANTS ---
# Default values (will be overwritten by fullscreen detection)
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 30  # Optimized for low-end devices

PEG_WIDTH = 10
BASE_HEIGHT = 20
PLATE_HEIGHT = 30
MIN_PLATE_WIDTH = 60
MAX_PLATE_WIDTH = 300

# Visual Constants
# Note: PEG_Y is calculated dynamically in the classes based on current height
LIFT_HEIGHT = 150 

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (40, 40, 40)
NAVY = (26, 35, 126)
SLATE = (44, 62, 80)
HOVER_COLOR = (227, 242, 253)
GREEN = (0, 150, 0)
CYAN = (0, 100, 150)
ORANGE = (255, 165, 0)
RED = (183, 28, 28)

class Plates:
    def __init__(self):
        self.values_list = []
        self.plate_count = 0
        self.colors = {} 

    def generate_random_plates(self, count):
        self.plate_count = count
        # Perfect Pyramid: Unique sizes
        self.values_list = random.sample(range(5, 50), count)
        self.values_list.sort(reverse=True) 
        self.generate_colors(count)

    def generate_colors(self, count):
        self.colors = {}
        for i, val in enumerate(self.values_list):
            hue = i / count 
            rgb = colorsys.hsv_to_rgb(hue, 0.8, 0.9)
            pygame_color = (int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))
            self.colors[val] = pygame_color

    def get_color(self, value):
        return self.colors.get(value, (255, 0, 0))

class Tower:
    def __init__(self, plates_obj, screen):
        self.screen = screen
        self.plates_obj = plates_obj
        self.towers = {
            "First Tower": [],
            "Second Tower": [],
            "Third Tower": []
        }
        self.towers["First Tower"] = plates_obj.values_list[:]
        
        self.peg_positions = {
            "First Tower": SCREEN_WIDTH // 4,
            "Second Tower": SCREEN_WIDTH // 2,
            "Third Tower": (SCREEN_WIDTH * 3) // 4
        }
        
        self.font = pygame.font.SysFont("Georgia", 20, bold=True)
        self.ui_font = pygame.font.SysFont("Georgia", 20)
        
        # Static Text
        self.static_ui_text = self.ui_font.render("[R] Reset | [Q] Quit", True, SLATE)
        self.plate_text_cache = {} 
        
        # --- UI LAYOUT ---
        # Position buttons to avoid overlap
        # Speed controls at (20, 60)
        self.btn_speed_down = pygame.Rect(20, 60, 40, 30)
        self.btn_speed_up = pygame.Rect(70, 60, 40, 30) # Spaced out
        
        # Skip button below
        self.btn_skip = pygame.Rect(20, 100, 160, 30)

    def get_peg_x(self, tower_name):
        return self.peg_positions[tower_name]

    def render_background_snapshot(self):
        surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        surface.fill(WHITE)
        
        # Recalculate PEG_Y based on current screen height
        current_peg_y = SCREEN_HEIGHT - BASE_HEIGHT

        # Draw Floor
        pygame.draw.rect(surface, SLATE, (0, SCREEN_HEIGHT - BASE_HEIGHT, SCREEN_WIDTH, BASE_HEIGHT))

        # Draw Pegs and Static Plates
        for tower_name, x_pos in self.peg_positions.items():
            peg_height = 400
            pygame.draw.rect(surface, SLATE, (x_pos - PEG_WIDTH//2, current_peg_y - peg_height, PEG_WIDTH, peg_height))
            
            plates = self.towers[tower_name]
            for i, plate_value in enumerate(plates):
                self._draw_plate_on_surface(surface, plate_value, x_pos, i)

        # Draw Top Right UI Text
        surface.blit(self.static_ui_text, (SCREEN_WIDTH - self.static_ui_text.get_width() - 20, 20))
        return surface

    def draw_ui_overlay(self, move_count, speed_label):
        """
        Draws the dynamic UI (Buttons, Hover effects, Text) on top of the scene.
        """
        mouse_pos = pygame.mouse.get_pos()
        
        # 1. Move Counter
        moves_text = self.ui_font.render(f"Moves: {move_count}", True, NAVY)
        self.screen.blit(moves_text, (20, 20))
        
        # 2. Speed Buttons with Hover Animation
        color_down = HOVER_COLOR if self.btn_speed_down.collidepoint(mouse_pos) else LIGHT_GRAY
        pygame.draw.rect(self.screen, color_down, self.btn_speed_down)
        pygame.draw.rect(self.screen, SLATE, self.btn_speed_down, 1)
        txt_minus = self.ui_font.render("-", True, BLACK)
        self.screen.blit(txt_minus, (self.btn_speed_down.centerx - txt_minus.get_width()//2, self.btn_speed_down.y + 2))

        color_up = HOVER_COLOR if self.btn_speed_up.collidepoint(mouse_pos) else LIGHT_GRAY
        pygame.draw.rect(self.screen, color_up, self.btn_speed_up)
        pygame.draw.rect(self.screen, SLATE, self.btn_speed_up, 1)
        txt_plus = self.ui_font.render("+", True, BLACK)
        self.screen.blit(txt_plus, (self.btn_speed_up.centerx - txt_plus.get_width()//2, self.btn_speed_up.y + 2))
        
        # 3. Speed Text
        txt_speed = self.ui_font.render(f"Speed: {speed_label}", True, SLATE)
        self.screen.blit(txt_speed, (120, 65)) 

        # 4. Skip Button
        color_skip = HOVER_COLOR if self.btn_skip.collidepoint(mouse_pos) else LIGHT_GRAY
        pygame.draw.rect(self.screen, color_skip, self.btn_skip)
        pygame.draw.rect(self.screen, SLATE, self.btn_skip, 1)
        txt_skip = self.ui_font.render("SKIP TO RESULT", True, RED)
        self.screen.blit(txt_skip, (self.btn_skip.centerx - txt_skip.get_width()//2, self.btn_skip.y + 4))

    def draw_full_scene(self, background_surf, move_count, speed_label):
        """Combines the cached background and dynamic UI."""
        self.screen.blit(background_surf, (0, 0))
        self.draw_ui_overlay(move_count, speed_label)

    def _draw_plate_on_surface(self, target_surf, plate_value, x_center, stack_index, custom_y=None):
        plate_width = MIN_PLATE_WIDTH + (plate_value * 5)
        if plate_width > MAX_PLATE_WIDTH: plate_width = MAX_PLATE_WIDTH
        
        x = x_center - (plate_width // 2)
        if custom_y is not None:
            y = custom_y
        else:
            y = SCREEN_HEIGHT - BASE_HEIGHT - ((stack_index + 1) * PLATE_HEIGHT)

        color = self.plates_obj.get_color(plate_value)

        pygame.draw.rect(target_surf, color, (x, y, plate_width, PLATE_HEIGHT))
        pygame.draw.rect(target_surf, BLACK, (x, y, plate_width, PLATE_HEIGHT), 2)
        
        if plate_value not in self.plate_text_cache:
            self.plate_text_cache[plate_value] = self.font.render(str(plate_value), True, BLACK)
            
        text = self.plate_text_cache[plate_value]
        text_rect = text.get_rect(center=(x + plate_width//2, y + PLATE_HEIGHT//2))
        target_surf.blit(text, text_rect)
        
    def draw_single_plate(self, plate_value, x_center, stack_index, custom_y=None):
        self._draw_plate_on_surface(self.screen, plate_value, x_center, stack_index, custom_y)

class Animation:
    def __init__(self, tower_obj, screen):
        self.tower_obj = tower_obj
        self.screen = screen
        self.clock = pygame.time.Clock()
        
        self.speeds = [1.2, 0.8, 0.3, 0.05] 
        self.speed_labels = ["Slow", "Normal", "Fast", "Turbo"]
        self.current_speed_idx = 1 
        
        self.skipping = False
        
    def check_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    return "restart"
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.tower_obj.btn_skip.collidepoint(event.pos):
                    self.skipping = True
                
                if self.tower_obj.btn_speed_up.collidepoint(event.pos):
                    if self.current_speed_idx < len(self.speeds) - 1:
                        self.current_speed_idx += 1
                
                if self.tower_obj.btn_speed_down.collidepoint(event.pos):
                    if self.current_speed_idx > 0:
                        self.current_speed_idx -= 1
                        
        return None

    def animate_move(self, plate_val, source_name, target_name, move_count):
        if self.skipping: return "done"
            
        start_x = self.tower_obj.get_peg_x(source_name)
        end_x = self.tower_obj.get_peg_x(target_name)
        
        start_y = SCREEN_HEIGHT - BASE_HEIGHT - ((len(self.tower_obj.towers[source_name]) + 1) * PLATE_HEIGHT)
        end_y = SCREEN_HEIGHT - BASE_HEIGHT - ((len(self.tower_obj.towers[target_name]) + 1) * PLATE_HEIGHT)

        duration = self.speeds[self.current_speed_idx]
        speed_label = self.speed_labels[self.current_speed_idx]
        
        total_frames = int(duration * FPS)
        if total_frames < 1: total_frames = 1
        
        # 1. Generate Static Background (No UI)
        bg_snapshot = self.tower_obj.render_background_snapshot()
        
        for frame in range(total_frames + 1):
            if self.check_input() == "restart": return "restart"
            if self.skipping: return "done"
            
            t = frame / total_frames
            
            if t < 0.3: # Up
                progress = t / 0.3
                cur_x = start_x
                cur_y = start_y + (LIFT_HEIGHT - start_y) * progress
            elif t < 0.7: # Across
                progress = (t - 0.3) / 0.4
                cur_x = start_x + (end_x - start_x) * progress
                cur_y = LIFT_HEIGHT
            else: # Down
                progress = (t - 0.7) / 0.3
                cur_x = end_x
                cur_y = LIFT_HEIGHT + (end_y - LIFT_HEIGHT) * progress

            # 2. Draw Background
            self.screen.blit(bg_snapshot, (0, 0))
            
            # 3. Draw UI Overlay (Buttons with hover, Text)
            self.tower_obj.draw_ui_overlay(move_count, speed_label)

            # 4. Draw Moving Plate
            self.tower_obj.draw_single_plate(plate_val, int(cur_x), -1, int(cur_y)) 
            
            pygame.display.flip()
            self.clock.tick(FPS)
            
        return "done"

class Logic:
    # Handles the Recursive Algorithm and State Management.  
    def __init__(self, tower_obj, animation_obj):
        self.tower_obj = tower_obj
        self.animation = animation_obj
        self.move_count = 0
        self.running = True

    def hanoi_move(self, n, source, target, auxiliary):
        if not self.running: return "restart"

        if n > 0:
            if self.hanoi_move(n - 1, source, auxiliary, target) == "restart": return "restart"
            
            if self.animation.check_input() == "restart": return "restart"

            if self.tower_obj.towers[source]:
                plate = self.tower_obj.towers[source].pop()
                
                if not self.animation.skipping:
                    res = self.animation.animate_move(plate, source, target, self.move_count)
                    if res == "restart": return "restart"
                
                self.tower_obj.towers[target].append(plate)
                self.move_count += 1
                
                if self.animation.skipping:
                     pygame.event.pump()
                else:
                     # Update scene between moves
                     bg = self.tower_obj.render_background_snapshot()
                     label = self.animation.speed_labels[self.animation.current_speed_idx]
                     self.tower_obj.draw_full_scene(bg, self.move_count, label)
                     pygame.display.flip()

            if self.hanoi_move(n - 1, auxiliary, target, source) == "restart": return "restart"

    def start_simulation(self):
        label = self.animation.speed_labels[self.animation.current_speed_idx]
        bg = self.tower_obj.render_background_snapshot()
        self.tower_obj.draw_full_scene(bg, 0, label)
        pygame.display.flip()
        pygame.time.delay(500)
        
        num_plates = len(self.tower_obj.towers["First Tower"])
        result = self.hanoi_move(num_plates, "First Tower", "Third Tower", "Second Tower")
        
        # Final Draw
        label = self.animation.speed_labels[self.animation.current_speed_idx]
        bg = self.tower_obj.render_background_snapshot()
        self.tower_obj.draw_full_scene(bg, self.move_count, label)
        pygame.display.flip()
        
        return result

def get_user_input_gui(screen):
    font = pygame.font.SysFont("Georgia", 40, bold=True)
    font_small = pygame.font.SysFont("Georgia", 24)
    font_error = pygame.font.SysFont("Georgia", 20, bold=True)
    
    input_value = ""
    error_msg = ""
    clock = pygame.time.Clock()
    
    numpad_map = {
        pygame.K_KP0: "0", pygame.K_KP1: "1", pygame.K_KP2: "2", pygame.K_KP3: "3",
        pygame.K_KP4: "4", pygame.K_KP5: "5", pygame.K_KP6: "6",
        pygame.K_KP7: "7", pygame.K_KP8: "8", pygame.K_KP9: "9"
    }
    
    while True:
        screen.fill(WHITE)
        title = font.render("TOWER OF HANOI", True, NAVY)
        prompt = font_small.render("Type how many plates (3-8)", True, SLATE)
        prompt2 = font_small.render("Press ENTER to start", True, SLATE)
        current = font.render(f"Plates: {input_value}", True, CYAN)
        
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 150))
        screen.blit(prompt, (SCREEN_WIDTH//2 - prompt.get_width()//2, 250))
        screen.blit(prompt2, (SCREEN_WIDTH//2 - prompt2.get_width()//2, 300))
        screen.blit(current, (SCREEN_WIDTH//2 - current.get_width()//2, 400))
        
        if error_msg:
            err_surf = font_error.render(error_msg, True, RED)
            screen.blit(err_surf, (SCREEN_WIDTH//2 - err_surf.get_width()//2, 450))
        
        pygame.display.flip()
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                
                # Logic: If user types anything, clear the error message
                error_msg = ""
                
                if event.unicode.isnumeric():
                    input_value += event.unicode
                elif event.key in numpad_map:
                    input_value += numpad_map[event.key]
                elif event.key == pygame.K_BACKSPACE:
                    input_value = input_value[:-1]
                    
                elif event.key == pygame.K_RETURN:
                    # VALIDATION LOGIC
                    try:
                        if input_value == "":
                            error_msg = "Please enter a number!"
                        else:
                            val = int(input_value)
                            if 3 <= val <= 8: 
                                return val
                            else:
                                error_msg = "Invalid Input! Please enter a number between 3-8 only."
                                input_value = "" # Clear invalid input
                    except ValueError:
                        error_msg = "Invalid Input! Numbers only."
                        input_value = ""

def main():
    # Use globals so updated screen size affects all classes
    global SCREEN_WIDTH, SCREEN_HEIGHT

    pygame.init()
    pygame.font.init()
    
    # MODIFIED: Set to FULLSCREEN using the monitor's native resolution
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF)
    
    # MODIFIED: Update global constants to match the actual fullscreen resolution
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
    
    pygame.display.set_caption("Tower of Hanoi Simulation")
    
    while True:
        num_plates = get_user_input_gui(screen)
        
        plates = Plates()
        plates.generate_random_plates(num_plates)
        
        tower = Tower(plates, screen)
        animation = Animation(tower, screen)
        logic = Logic(tower, animation)
        
        status = logic.start_simulation()
        
        if status == "restart":
            continue
            
        waiting = True
        clock = pygame.time.Clock()
        while waiting:
            # Draw final state
            bg = tower.render_background_snapshot()
            label = animation.speed_labels[animation.current_speed_idx]
            tower.draw_full_scene(bg, logic.move_count, label)
            
            font = pygame.font.SysFont("Georgia", 50, bold=True)
            text = font.render("Complete! Press R or Q", True, GREEN)
            
            bg_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 25))
            bg_rect.inflate_ip(20, 20)
            pygame.draw.rect(screen, WHITE, bg_rect)
            pygame.draw.rect(screen, SLATE, bg_rect, 2)
            screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 - 50))
            
            pygame.display.flip()
            clock.tick(FPS)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_r:
                        waiting = False

if __name__ == "__main__":
    main()