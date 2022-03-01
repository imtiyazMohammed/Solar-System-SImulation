import pygame 
import math
pygame.init()

WIDTH, HEIGHT = 800,800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

SUN_COLOR = (253, 184, 19)
MERCURY_COLOR = (80, 78, 81)
VENUS_COLOR = (248,226,176)
EARTH_COLOR = (107, 147, 214)
MARS_COLOR = (193, 68, 14)
JUPITER_COLOR = (227, 220, 203)
SATURN_COLOR = (206,184,184)
URANUS_COLOR = (101, 134, 139)
NEPTUNE_COLOR = (91,93,223)
WHITE = (255, 255, 255)

FONT = pygame.font.SysFont("comicsans", 16)

class Planet:
    AU = 149.6e6 * 1000 # Astronomical Unit -> Distance from the earth to the sun = 149,597,870.7 KM
    G = 6.67428e-11 # Universal Gravitational Constant, 6.67408 × 10-11 m3 kg-1 s-2
    SCALE = 100/AU # 1 AU = 100 pixels
    TIMESTEP = 3600*24 # 1 Day
    def __init__(self, name,  x, y, radius, color, mass):
        self.name = name
        self.x = x 
        self.y = y 
        self.radius = radius
        self.color = color 
        self.mass = mass
        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0
        self.x_vel = 0
        self.y_vel = 0
    
    def draw(self, win):
        x = self.x * self.SCALE + WIDTH/2
        y = self.y * self.SCALE + HEIGHT/2
        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x,y = point 
                x = x*self.SCALE + WIDTH/2
                y = y*self.SCALE + HEIGHT/2
                updated_points.append((x,y))
            
            pygame.draw.lines(win, self.color, False, updated_points, 1)

        pygame.draw.circle(win, self.color, (x,y), self.radius)
        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/1000, 2)}KM . " + f"{self.name}", 1, WHITE)
            win.blit(distance_text, (x - distance_text.get_width()/2 ,y - distance_text.get_height()/2))
    
    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x 
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)

        if other.sun:
            self.distance_to_sun = distance
        
        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force 
        force_y = math.sin(theta) * force 

        return force_x, force_y
    
    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            
            fx, fy = self.attraction(planet)
            total_fx += fx 
            total_fy += fy
        
        self.x_vel += total_fx/self.mass * self.TIMESTEP
        self.y_vel += total_fy/self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))

        

def main():
    run = True 
    clock = pygame.time.Clock()

    # Initialize SUN
    sun = Planet( "SUN",0, 0, 30, SUN_COLOR, 1.98892* 10**30)
    sun.sun = True
    
    # Initialize MERCURY
    mercury = Planet("MERCURY", 0.387*Planet.AU, 0, 8, MERCURY_COLOR, 0.330* 10**24)
    mercury.y_vel = -47.4 * 1000
    
    # Initialize VENUS
    venus = Planet("VENUS", 0.723*Planet.AU, 0 ,14, VENUS_COLOR, 4.8685* 10**24)
    venus.y_vel = -35.02 * 1000

    # Initialize EARTH
    earth = Planet("EARTH",-1*Planet.AU, 0, 16, EARTH_COLOR, 5.9742* 10**24)
    earth.y_vel = 29.783 * 1000

    # Initialize MARS
    mars = Planet("MARS" ,-1.524*Planet.AU, 0, 12, MARS_COLOR, 6.39* 10**23)
    mars.y_vel = 24.077 * 1000

    # Initialize JUPITER
    jupiter = Planet("JUPITER", 5.204*Planet.AU, 0, 22, JUPITER_COLOR, 1898.13* 10**24)
    jupiter.y_vel = -13.06*1000

    # Initialize SATURN
    saturn = Planet("SATURN", 9.573*Planet.AU, 0, 19, SATURN_COLOR, 568.32* 10**24)
    saturn.y_vel = -9.68 * 1000

    # Initialize URANUS
    uranus = Planet("URANUS", -19.165*Planet.AU, 0, 18, URANUS_COLOR, 86.81* 10**24)
    uranus.y_vel = 6.80 * 1000

    # Initialize NEPTUNE
    neptune = Planet("NEPTUNE", -30.178*Planet.AU, 0, 17, NEPTUNE_COLOR, 102.40* 10**24)
    neptune.y_vel = 5.43 * 1000

    planets = [sun, earth, mars, mercury, venus, jupiter, saturn, uranus, neptune]

    while run:
        clock.tick(60)
        WIN.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()
    pygame.quit()

main()