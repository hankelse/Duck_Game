import pygame, sys, time, random, pyautogui
from pygame.constants import K_SPACE, K_ESCAPE, K_w, K_a, K_s, K_d, K_LSHIFT
pygame.init()

from sprites import Character, Person

size = width, height =  800, 800
cycle_time = 0.025

#screen = pygame.display.set_mode(size)
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
size = width, height = pygame.display.get_window_size()

def new_person(lane, wait_time):
    return(Person(width+player_width, lane, people_num+2, player_width, player_height, "bread", land_width, land_height, width, height, wait_time, debug_mode))

#--------SETTINGS---------#
debug_mode = False

bread_decay_interval = 4

bindings = {
    "up" : K_w, 
    "down": K_s,
    "left": K_a,
    "right": K_d,
    "sprint": K_LSHIFT
}

#_PLAYER_#
player_acceleration, player_decleration = 1, 0.2
player_maxspeed, playerminspeed = 6, -6
player_width, player_height = 100, 100
player_startingx, player_startingy = 400, 400
player_sprint_factor = 1.5

#_PEOPLE_#
people_num = 5
player_width, player_height = 100, 100

#_LAND_#
land_width = int(width/4)
land_height = height*7/8


#---------SETUP---------#
def setup():
    if debug_mode == True: print("Setup: Starting")
    player = Character(player_startingx, player_startingy, player_acceleration, player_decleration, player_width, player_height, player_maxspeed, playerminspeed, land_width, debug_mode)
    throwables = []
    people = []
    bread = []
    for i in range(people_num+1): people.append(new_person(i+1, random.randint(0, 100)))
    if debug_mode == True: print("Setup: Complete")
    return player, people, throwables, bread
    
    

player, people, throwables, bread = setup()
land_img = pygame.image.load("Duck/Photoshop/Land/Land.png")
land_img = pygame.transform.scale(land_img, (int(land_width), int(land_height)))

while 1:
    now = time.time()
    screen.fill((160, 160, 255))
    screen.blit(land_img, (width-land_width, 0+(height-land_height)/2))
    #pygame.draw.rect(screen, (60, 20, 10), pygame.Rect(width*3/4, 0, width*1/4, height))
    keys=pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        quit()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    
    player.move(keys, bindings, width, height, player_sprint_factor)

    for person in people:
        person_state, create_ball, thrown = person.move()
        #print(person_stadte, create_ball, ball)
        if create_ball == "yes":
             throwables.append(thrown)
            
        if person_state == "delete":
            if debug_mode == True: print("Person "+str(person.lane)+": Deleted and Replaceed")
            people.append(new_person(person.lane, 0))
            people.remove(person)
        
    #print(len(throwables))
    for thrown in throwables: 
        state, thing = thrown.move(bread_decay_interval)
        if state == "active":
            bread.append(thing)
            throwables.remove(thrown)
    #print(len(throwables))


    for slice in bread:
        slice.draw(screen)


    player.draw(screen)
    for person in people: person.draw(screen)

    for thrown in throwables: 
        thrown.draw(screen)
    
    pygame.display.flip()
    
    elapsed = time.time()-now
    if elapsed < cycle_time:
        time.sleep(cycle_time-elapsed)


