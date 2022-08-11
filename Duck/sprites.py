from distutils.log import debug
from re import S
import time, math, random, pygame

pygame.init()

class Character:
    def __init__(self, startingx, startingy, acceleration, deceleration, player_width, player_height, player_maxspeed, playerminspeed, land_width, debug_mode):
        self.debug_mode = debug_mode
        
        self.land_width = land_width
        self.acceleration, self.deceleration, self.width, self.height = acceleration, deceleration, player_width, player_height
        self.x, self.y = startingx, startingy

        self.xv, self.yv = 0, 0
        self.xd, self.yd = 0, 0
        self.xv_max, self.yv_max = player_maxspeed, player_maxspeed
        self.xv_min, self.yv_min = playerminspeed, playerminspeed
        
        self.rotate_speed = 15
        self.angle = 90
        self.desired_angle = 90
        self.angles = {
        #    [0, 0] : 0,
            "0, 1" : 270,
            "1, 0" : 0,
            "-1, 0" : 180,
            "0, -1" : 90,
            "1, -1" : 45,
            "1, 1" : 315,
            "-1, -1" : 135,
            "-1, 1" : 225,

        }

        self.last_move = 0
        self.move_delay = 0
        self.sprint_factor = 1
        self.angle = 90

        self.original_img = pygame.image.load('Duck/Photoshop/Duck/Duck.png')
        self.original_img = pygame.transform.scale(self.original_img, (self.width, self.height))

        self.img = self.original_img


        if self.debug_mode == True: print("Player: Created")
    def move(self, keys, bindings, width, height, sprint_factor):

        self.xd, self.yd = 0, 0

        if keys[bindings["sprint"]]: 
            self.sprint_factor = sprint_factor
        elif self.sprint_factor == sprint_factor: self.sprint_factor = 1
        
        if keys[bindings["left"]] and time.time() - self.last_move >= self.move_delay:
            if self.debug_mode == True: print("User: Left Pressed")
            self.xd = -1
            if self.xv == self.xv_min*self.sprint_factor: pass
            elif self.xv - self.acceleration*self.sprint_factor >= self.xv_min*self.sprint_factor:
                self.xv-=self.acceleration*self.sprint_factor
            else: self.xv = self.xv_min*self.sprint_factor

            self.last_move = time.time()
        
        elif keys[bindings["right"]] and time.time() - self.last_move >= self.move_delay:
            if self.debug_mode == True: print("User: Right Pressed")
            self.xd = 1
            if self.xv == self.xv_max*self.sprint_factor: pass
            elif self.xv + self.acceleration*self.sprint_factor <= self.xv_max:
                self.xv+=self.acceleration*self.sprint_factor
            else: self.xv = self.xv_max*self.sprint_factor
            
            self.last_move = time.time()
        else: self.xd = 0
        
        if keys[bindings["down"]] and time.time() - self.last_move >= self.move_delay:
            if self.debug_mode == True: print("User: Down Pressed")
            
            self.yd = 1
            if self.yv == self.yv_max*self.sprint_factor: pass
            elif self.yv + self.acceleration*self.sprint_factor <= self.yv_max*self.sprint_factor:
                self.yv+=self.acceleration*self.sprint_factor
            else: self.yv = self.yv_max*self.sprint_factor
            self.last_move = time.time()
        
        elif keys[bindings["up"]] and time.time() - self.last_move >= self.move_delay:
            if self.debug_mode == True: print("User: Up Pressed")
            self.yd = -1
            if self.yv == self.yv_min*self.sprint_factor: pass
            elif self.yv - self.acceleration*self.sprint_factor >= self.yv_min*self.sprint_factor:
                self.yv-=self.acceleration*self.sprint_factor
            else: self.yv = self.yv_min*self.sprint_factor
            self.last_move = time.time()
        else: self.yd = 0

        
        if self.xv != 0:
            if abs(self.xv) <= self.deceleration: 
                self.xv = 0
                if self.debug_mode == True: print("Player: Stopped Moving (X)")
        if self.yv != 0:
            if abs(self.yv) <= self.deceleration: 
                self.yv = 0
                if self.debug_mode == True: print("Player: Stopped Moving (Y)")


        if self.xv != 0:
            if self.xv >0: 
                
                if self.x+self.xv < width-self.land_width-self.img.get_width()/2:
                    self.x += self.xv
                    if self.debug_mode == True: print("Player: Moved Left")

                self.xv -= self.deceleration*self.sprint_factor
            elif self.xv <0: 

                if self.x+self.xv > self.img.get_width()/2:
                    self.x += self.xv
                
                if self.debug_mode == True: print("Player: Moved Right")

                self.xv += self.deceleration*self.sprint_factor
        if self.yv != 0:

            if self.yv >0: 
                
                if self.y+self.yv < height-self.img.get_height()/2:
                    self.y += self.yv
                
                if self.debug_mode == True: print("Player: Moved Down")

                self.yv -= self.deceleration
            elif self.yv <0: 
                
                if self.y+self.yv > self.img.get_height()/2:
                    self.y += self.yv

                if self.debug_mode == True: print("Player: Moved Up")

                self.yv += self.deceleration

        if self.debug_mode == True: print("Player: Move Over")

    def draw(self, screen):
        change = 0

        self.angle = (self.angle + change)%360
        if self.angle < 0:
            self.angle = 360 + self.angle

        if self.angle > 360 or self.angle < -360:
            self.angle = self.angle % 360

        #print(str(self.xd)+", "+str(self.yd))
        if self.xd == 0 and self.yd == 0: pass
        else:
            #print(str(self.xd)+", "+str(self.yd))
            self.desired_angle = self.angles[str(self.xd)+", "+str(self.yd)]

        if abs(self.desired_angle - self.angle) < self.rotate_speed or abs(360-self.desired_angle + self.angle) < self.rotate_speed:
            change = self.desired_angle-self.angle
        # elif self.desired_angle - self.angle < self.angle + 360 - self.desired_angle: change = self.rotate_speed
        # else: change = self.rotate_speed *-1

        else:

            if 360-self.angle > 360-self.desired_angle: change = self.rotate_speed
            else: change = -self.rotate_speed
            if abs(self.desired_angle-self.angle) > 180: change *= -1

 
        self.angle = (self.angle + change)%360
        if self.angle < 0:
            self.angle = 360 + self.angle
        
        #print(self.angle, self.desired_angle)
 
        self.img = pygame.transform.rotozoom(self.original_img, self.angle-90, 1)

        screen.blit(self.img, (round(self.x - self.img.get_width()/2), round(self.y - self.img.get_height()/2)))
   
class Person:
    def __init__(self, x, lane, people_num, width, height, throwing, land_width, land_height, screen_width, screen_height, starting_wait_time, debug_mode):
        self.debug_mode = debug_mode

        self.skins = skins[random.randint(0, len(skins)-1)]
        self.width, self.height = width, height

        self.original_normal = pygame.image.load(self.skins[0])
        self.original_throwing = pygame.image.load(self.skins[1])
        self.original_throwing_full = pygame.image.load(self.skins[2])

        self.original_normal = pygame.transform.scale(self.original_normal, (self.width, self.height))
        self.original_throwing = pygame.transform.scale(self.original_throwing, (self.width, int(self.height*1.1)))
        self.original_throwing_full = pygame.transform.scale(self.original_throwing_full, (self.width, int(self.height*1.2)))

        self.state = "walking" #or throwing
        self.img_state = "normal"
        self.waiting = 0
        self.wait_time = 5 # wait time between frames of throwing
        self.current_img = self.original_normal


        self.x = x
        self.lane = lane
        self.width, self.height = self.current_img.get_width(), self.current_img.get_height()

        min_y = int( (screen_height-land_height)/2)
        max_y = int( screen_height-(screen_height-land_height)/2)
        space_per_person = round( (max_y-min_y)/people_num)
        
        
        #(max_y-min_y)/lane
        self.y = random.randint(int( min_y + space_per_person*(lane-1)+self.width ), int( min_y + space_per_person*(lane)))

        self.angle = 180


        self.throwing = throwing
        
        
        self.walk_speed = random.randint(4, 6)
        
        self.has_thrown = False

        
        self.starting_wait_frames = starting_wait_time


        self.wait_frames1 = random.randint(50, 200)#before throw
        self.wait_frames2 = random.randint(10, 20)# after throw
        self.queue = self.get_moves(land_width, screen_width)


        if self.debug_mode == True: print("Person "+str(self.lane)+": Created")
    def get_moves(self, land_width, screen_width):
        moves = []

        for i in range(self.starting_wait_frames):
            moves.append([0, 0])

        for i in range(math.floor((self.x-(screen_width-land_width+self.height))/self.walk_speed)):
            moves.append([-self.walk_speed, 0])
        
        for i in range(self.wait_frames1):
            moves.append([0, 0])
        
        moves.append(['THROW', 'THROW'])

        for i in range(self.wait_frames2):
            moves.append([0, 0])

        for i in range(math.floor((screen_width-land_width)/self.walk_speed)):
            moves.append([self.walk_speed, 0])
        
        moves.append(['DELETE', 'DELETE'])

        if self.debug_mode == True: print("Person "+str(self.lane)+": Moves Gotten")

        return(moves)

    def move(self):
        #print(self.state)
        #print("move")
        if self.queue[0][0] == 'THROW': 
            self.state = "throwing"
            if self.debug_mode == True: print("Person "+str(self.lane)+": State Switched (Throwing)")
            #print("throwing")
        elif self.queue[0][0] == 'DELETE':  
            self.state = "delete"
            #print("delete")

        if self.state == "walking":
            #print("walking")
            self.x += self.queue[0][0]
            self.y += self.queue[0][1]
            self.queue = self.queue[1::]

            if self.debug_mode == True: print("Person "+str(self.lane)+": Walking")
        
        elif self.state == "throwing":
            #print("throwing is ran!")
            self.state, create_ball, thrown = self.throw()
            self.queue = self.queue[1::]
            return self.state, create_ball, thrown
        
        return self.state, None, None
    
    def throw(self):
        if self.waiting == 0:
            if self.img_state == "normal":
                self.img_state = "throwing"
                #print("switch")
                self.current_img = self.original_throwing
                self.waiting = self.wait_time
                if self.debug_mode == True: print("Person "+str(self.lane)+": IMG switched to throwing")

            elif self.img_state == "throwing":
                self.img_state = "throwing_full"
                #print("switch2")
                self.current_img = self.original_throwing_full
                self.waiting = self.wait_time
                if self.debug_mode == True: print("Person "+str(self.lane)+": IMG switched to throwing_full")
                
            
            elif self.img_state == "throwing_full":
                self.img_state = "throwing1"
                #print("switch3")
                self.current_img = self.original_throwing
                self.waiting = self.wait_time
                self.x -= self.width/2

                if self.debug_mode == True: print("Person "+str(self.lane)+": IMG switched to throwing1")

                if self.has_thrown == False:
                    self.has_thrown = True
                    if self.debug_mode == True: print("Person "+str(self.lane)+": Returned bread Object")
                    return self.state, "yes", Thrown(self.x, self.y, "bread", 10, self.debug_mode)


            elif self.img_state == "throwing1":
                self.img_state = "normal"
                #print("switch4")
                self.current_img = self.original_normal
                self.waiting = self.wait_time
                self.x += self.width/2

                if self.debug_mode == True: print("Person "+str(self.lane)+": IMG switched to Normal")

                self.angle = 360
                self.state = "walking"
        else: 
            self.waiting -= 1
            if self.debug_mode == True: print("Person "+str(self.lane)+": Waiting to Switch IMG")
            #print("waiting")
        return self.state, "no", [] 

        


    def draw(self, screen):


        self.img = pygame.transform.rotozoom(self.current_img, self.angle-90, 1)
        screen.blit(self.img, (round(self.x - self.img.get_width()/2), round(self.y - self.img.get_height()/2)))

class Bread: 
        def __init__(self, x, y, width, height, decay_interval, debug_mode):
            self.debug_mode = debug_mode
            self.x = x
            self.y = y
            self.width, self.height = width, height
            self.rotation = random.randint(0, 360)
            self.points = 10
            self.decay_interval = decay_interval

            self.img1 = pygame.image.load("Duck/Photoshop/Bread/sitting_bread.png")
            self.img1 = pygame.transform.scale(self.img1, (self.width, self.height))
            self.img1 = pygame.transform.rotate(self.img1, self.rotation)

            self.img2 = pygame.image.load("Duck/Photoshop/Bread/sitting_bread1.png")
            self.img2 = pygame.transform.scale(self.img2, (self.width, self.height))
            self.img2 = pygame.transform.rotate(self.img2, self.rotation)

            self.img3 = pygame.image.load("Duck/Photoshop/Bread/sitting_bread2.png")
            self.img3 = pygame.transform.scale(self.img3, (self.width, self.height))
            self.img3 = pygame.transform.rotate(self.img3, self.rotation)

            
            self.index = 0
            self.skins = [self.img1, self.img2, self.img3]
            self.img = self.skins[self.index]

            self.last_change = time.time()

            if self.debug_mode == True: print("Bread: IMG switched to throwing")
        
        def decay(self):
            if time.time()-self.last_change > self.decay_interval:
                self.next_skin()

        def next_skin(self):
            self.index+=1
            self.index = self.index % len(self.skins)
            self.img = self.skins[self.index]

        def draw(self, screen):
            if self.debug_mode == True: print("Bread: Drawn")
            screen.blit(self.img, (self.x-self.width/2, self.y-self.height/2))

class Thrown:
    def __init__(self, x, y, type, speed, debug_mode):
        self.debug_mode = debug_mode
        self.x, self.y = x, y
        self.og_x, self.og_y = x, y
        self.type, self.speed = type, speed
        self.xv, self.yv = -speed-random.randint(0, speed*2), -speed/3
        self.x_decel, self.y_decel = 1, 0.3 
        self.width, self.height = 50, 50
        self.state = "moving"

        

        self.bread_skins = [
            "Duck/Photoshop/Bread/throw_bread1.png", 
            "Duck/Photoshop/Bread/throw_bread2.png", 
            "Duck/Photoshop/Bread/throw_bread3.png", 
            "Duck/Photoshop/Bread/throw_bread4.png", 
        ]
        
        self.rock_skins = []

        if self.type == "bread": self.skins = self.bread_skins
        elif self.type== "rock": self.skins = self.rock_skins

        skin1 = pygame.image.load(self.skins[0])
        skin2 = pygame.image.load(self.skins[1])
        skin3 = pygame.image.load(self.skins[2])
        skin4 = pygame.image.load(self.skins[3])

        skin1 = pygame.transform.scale(skin1, (self.width, self.height))
        skin2 = pygame.transform.scale(skin2, (self.width, self.height))
        skin3 = pygame.transform.scale(skin3, (self.width, self.height))
        skin4 = pygame.transform.scale(skin4, (self.width, self.height))

        self.skins = [skin1, skin2, skin3, skin4]
        # for skin in self.skins:
        #     skin = pygame.transform.scale(skin, (self.width, self.height))

        self.skin_index = 0
        self.frame_count = 0
        self.skin = self.skins[self.skin_index]

        #sitting_skin = pygame.image.load("Duck/Photoshop/Bread/sitting_bread.png")
        #self.sitting_skin = pygame.transform.scale(sitting_skin, (self.width, self.height))

        if self.debug_mode == True: print("Thrown "+self.type+": Created")

    def move(self, bread_decay_interval):
        if self.state == "moving":
            if self.y < self.og_y+self.yv and self.y > self.og_y-self.yv and self.x != self.og_x:
                self.state = "active"
                if self.debug_mode == True: print("Thrown "+self.type+": Landed and Bread obj Returned")
                return("active", Bread(self.x, self.y, 50, 50, bread_decay_interval, self.debug_mode))
            else:
                self.frame_count += 1
                if self.frame_count%10 == 0: 
                    self.skin_index += 1
                    self.skin = self.next_skin(self.skin_index)
                self.x += self.xv
                self.y += self.yv
                if self.xv + self.x_decel > 0:
                    self.xv += self.x_decel
                self.yv += self.y_decel
                if self.debug_mode == True: print("Thrown "+self.type+": Moving")
            return("moving", None)
        elif self.state == "active":
            if self.debug_mode == True: print("Thrown "+self.type+": Waiting to be Deleted ERROR")
            return("", None)

    def next_skin(self, index):
        index = index % len(self.skins)
        if self.debug_mode == True: print("Thrown "+self.type+": Skin Switched")
        return(self.skins[index])
    
    def draw(self, screen):
        if self.debug_mode == True: print("Thrown "+self.type+": Drawn")
        screen.blit(self.skin, (self.x-self.width/2, self.y-self.height/2))
        #pass
        #pygame.draw.ellipse(screen, (0, 0, 0), pygame.Rect(self.x-self.size/2, self.y-self.size/2, self.size, self.size))
    
    

skins = {
    0 : ['Duck/Photoshop/Person1/Normal.png', 'Duck/Photoshop/Person1/Throwing.png', 'Duck/Photoshop/Person1/Throwing_Full.png']
}


