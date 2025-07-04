import pygame,math,os,random
        
class StatusBar(pygame.sprite.Sprite):
    '''creates a statusbar (lifebar,armourbar,reloadbar)'''
    def __init__(self,position,color1,color2,size,status1,status2,type,increase):
        '''Accepts position,color1,color2,size,status1,status2,type, and increase.
        type 0=normal status bar
        type 1=reloading status bar
        '''
        pygame.sprite.Sprite.__init__(self)
        
        #Set variables
        self.__colors=[color1,color2]
        self.__size=size
        self.__s1=status1 #current status value
        self.__s2=float(status2) if status2 != 0 else 1  # Prevent division by zero
        self.__m=size[0]/(self.__s2/self.__s2*100) #multipler
        self.__type=type
        self.__increase=increase
        
        #Create image
        self.image=pygame.Surface(size)
        self.image.fill(color2)
        pygame.draw.rect\
              (self.image,color1,\
               ((0, 0),(self.__s1/self.__s2*100*self.__m,self.__size[1])), 0)
        
        # Set the rect attribute for our StatusBar sprite
        self.rect = self.image.get_rect()
        self.rect.left = position[0]
        self.rect.top = position[1]
    
    def set_position(self,position):
        '''sets the rect of the status bar'''
        self.rect.left=position[0]
        self.rect.top=position[1]
        
    def set_status(self,current_status):
        '''sets the status of the reload bar aka the numerator'''
        self.image.fill(self.__colors[1])
        pygame.draw.rect\
              (self.image,self.__colors[0],\
               ((0, 0),(current_status/self.__s2*100*self.__m,self.__size[1])), 0)
        
    def get_reload(self):
        '''get whether reload has finished or not, returns a bool'''
        if self.__s2-self.__s1<0:
            return True
        
    def update(self):
        '''update only applies for reloading so it only occurs when type is 1'''
        if self.__type:
            self.image.fill(self.__colors[1])
            self.__s1+=self.__increase
            pygame.draw.rect\
                  (self.image,self.__colors[0],\
                   ((0, 0),(self.__s1/self.__s2*100*self.__m,self.__size[1])), 0)
            
            if self.__s2-self.__s1<-1:
                self.kill()
                
class Text(pygame.sprite.Sprite):
    '''a text class that works for any text blitting and has the ability
    to accept as many variables as entered and string formatting'''
    def __init__(self,size,color,position,variables,message,alpha):
        '''accepts size,color,position,variables,message and alpha'''
        pygame.sprite.Sprite.__init__(self)
        try:
            self.__font = pygame.font.Font("American Captain.ttf", size)
        except FileNotFoundError:
            self.__font = pygame.font.SysFont(None, size)  # Use default font if file is missing
        self.__color=color
        self.__position=position
        
        if variables:
            self.__variables=variables.split(',') #splits variables into a list
            
        self.__message=message
        self.__m=''
        self.__alpha=alpha
        
    def set_variable(self,index,value):
        '''accepts an index and a value to set the variable at that index to'''
        self.__variables[index]=value
        
    def set_alpha(self,alpha):
        self.__alpha=alpha
        
    def update(self):
        '''This method will be called automatically to display
        the text at the set position.'''
        if self.__variables:
            #string formating using zip to create a tuple from list
            self.__m = self.__message %\
                    (list(zip(*[iter(self.__variables)]*len(self.__variables)))[0])
        else:
            self.__m=self.__message
            
        self.image = self.__font.render(self.__m, 1, self.__color)
        self.image.set_alpha(self.__alpha)
        self.rect = self.image.get_rect()
        self.rect.center = (self.__position)
        
class Zombie(pygame.sprite.Sprite):
    '''a zombie class that is randomly blitted off screen left, right and bottom.
    It will rotate and move towards the player. It also has an attack delay'''
    def __init__(self,screen,speed,damage,hp,attack_speed,value,image,zombie_type,player_pos):
        '''accepts screen,speed,damage,hp,attack_speed,value,image,wave_type,player_pos'''
        pygame.sprite.Sprite.__init__(self)
        #Assign screen to a variable
        self.__screen=screen
        
        #Assign speed to a variable
        # Apply 20% speed reduction
        self.__speed = speed * 0.8
        self.__default_speed = speed * 0.8
        
        #Assign the bullet damage to a variable
        self.__damage=damage
        
        #Assign hp to a variable
        self.__max_hp = hp  # Store max HP for health bar calculation
        self.__hp = hp
        
        #Assign attack speed to a variable
        self.__attack_speed = attack_speed

        # Create health bar surface with transparency
        self.__health_bar_width = 40
        self.__health_bar_height = 5
        self.__health_bar = pygame.Surface((self.__health_bar_width, self.__health_bar_height), pygame.SRCALPHA)
        
        #Assign value to a variable
        self.__value=value
        
        #Assign the wave type to a varible
        self.__zombie_type=zombie_type
        
        #Set variables for move
        self.__move=True
        
        #Set a counter for attack speed
        self.__count=(attack_speed-1)
        #Set up variables for slow
        self.__slow=False
        self.__slow_counter=0
            
        self.image=image
        self.image.convert_alpha()
        self.__saved_image=self.image
        self.rect = self.image.get_rect() 
        
        #Assign the enemy position
        self.spawn()
        
        #Rotate the image
        self.rotate(player_pos)
        
        #Calculate distance and step amount
        self.set_step_amount(player_pos)
        
        
    def reset_attack(self):
        '''resets the attack count'''
        self.__count=self.__attack_speed-1
        
    def get_attack(self):
        '''adds one to attack count and returns True or False if count is equal
        to attack speed'''
        self.__count+=1
        if self.__count==self.__attack_speed:
            self.__count=0
            return True
        else:
            return False
        
    def get_zombie_type(self):
        '''get the zombie type'''
        return self.__zombie_type
    
    def get_damage(self):
        '''get the damage'''
        return self.__damage
    
    def get_value(self):
        '''get the value'''
        return self.__value
        
    def damage_hp(self,damage):
        '''subtract damage from hp and returns the state of the hp'''
        self.__hp-=damage
        if self.__hp>0:
            return True
        else:
            return False
        
    def slow(self):
        '''halves the speed of the zombie and sets slow to true'''
        self.__speed=self.__speed/2
        self.__slow=True
        
    def restore_speed(self):
        '''Restores the zombie's speed to its default value'''
        self.__speed = self.__default_speed
        self.__slow = False
        self.__slow_counter = 0
        
    def set_step_amount(self,player_pos):
        '''calculate step amount using player_pos and trig'''
        #Calculate distance and step amount
        try:
            self.__distance=math.sqrt\
                (pow(player_pos[0]-self.rect.centerx,2)+pow(player_pos[1]-self.rect.centery,2))
            self.__animation_steps=self.__distance/self.__speed
            self.__dx=(player_pos[0]-self.rect.centerx)/self.__animation_steps
            self.__dy=(player_pos[1]-self.rect.centery)/self.__animation_steps
        except:
            self.__dx=0
            self.__dy=0
    
    def move(self,bool):
        '''sets the move variable to a passed in bool'''
        self.__move=bool
    
    def spawn(self):
        '''randomly spawns zombies from either left,right or bottom'''
        self.__spawn=random.randint(1,3)
        #Left
        if self.__spawn==1:
            self.__x=random.randrange(0,-300,-30)
            self.__y=random.randint(0,self.__screen.get_height()-100)
        #Right
        elif self.__spawn==2:
            self.__x=random.randint(self.__screen.get_width(),self.__screen.get_width()+300)
            self.__y=random.randint(0,self.__screen.get_height()-100)  
        #Bottom
        else:
            self.__x=random.randint(0,self.__screen.get_width())
            self.__y=random.randint(self.__screen.get_height(),self.__screen.get_height()+300)
            
        self.rect.center=(self.__x,self.__y)
        
        
    def rotate(self,player_pos):
        '''accepts player position and rotates towards it'''
        self.__angle = math.degrees(math.atan2\
              (self.rect.centerx-player_pos[0], self.rect.centery-player_pos[1]))
        
        self.image=pygame.transform.rotate\
            (self.__saved_image, self.__angle)
        
        self.rect = self.image.get_rect(center=self.rect.center)
        
    def update(self):
        '''if move is true, the zombie will move. if slow is true, slow counter 
        be increased and when the counter reaches 400 or greater, the counter resets
        and slow is no longer true'''
        
        if self.__move:
            self.rect.centerx+=self.__dx
            self.rect.centery+=self.__dy
        if self.__slow:
            self.__slow_counter+=1
            if self.__slow_counter>=400:
                self.__speed=self.__default_speed
                self.__slow_counter=0
                self.__slow=False

        # Update health bar
        self.__health_bar.fill((0, 0, 0, 0))  # Clear with transparency
        
        # Draw black outline
        pygame.draw.rect(self.__health_bar, (0, 0, 0, 255), 
                        (0, 0, self.__health_bar_width, self.__health_bar_height))
        
        # Draw red background
        pygame.draw.rect(self.__health_bar, (255, 0, 0, 255), 
                        (1, 1, self.__health_bar_width-2, self.__health_bar_height-2))
        
        # Draw green health remaining
        health_percentage = self.__hp / self.__max_hp
        if health_percentage > 0:
            green_width = int((self.__health_bar_width-2) * health_percentage)
            if green_width > 0:  # Ensure we don't draw if width rounds to 0
                pygame.draw.rect(self.__health_bar, (0, 255, 0, 255),
                               (1, 1, green_width, self.__health_bar_height-2))
        
        # Draw health bar above zombie
        health_pos = (self.rect.centerx - self.__health_bar_width // 2,
                     self.rect.top - 10)
        self.__screen.blit(self.__health_bar, health_pos)
     
class Player(pygame.sprite.Sprite):
    '''player class creates a list of image of the different weapons. it accepts
    mouse positon for rotation and has methods to move the rect'''
    def __init__(self,screen):
        pygame.sprite.Sprite.__init__(self)
        
        # Initialize gold
        self.__gold = 0
        
        # Add gun offset positions for bullet spawning
        self.__gun_offsets = {
            0: (40, 0),   # Pistol offset
            1: (45, 2),   # Uzi offset
            2: (50, -2),  # Slow gun offset
            3: (42, 0),   # Machine gun offset
            4: (48, 2)    # Last gun offset
        }
        self.__current_weapon = 0
        self.__last_mouse_pos = None
        
        #Create list of images
        self.__list = []
        for file in os.listdir('player/'):
            self.__list.append(pygame.image.load('./player/'+file))
            
        #Set original image
        self.image = self.__list[0]
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()    
        
        #Set saved image
        self.__saved_image = self.image
        
        # Set the rect attribute for our player sprite
        self.rect.left = 0
        self.rect.top = 200
        self.__speed = 4
        
        #set the angle value
        self.__angle=0
    
    def get_gold(self):
        '''returns the player's gold'''
        return self.__gold
    
    def add_gold(self, amount):
        '''adds gold to the player'''
        self.__gold += amount
    
    def reset_speed(self):
        '''reset speed to default'''
        self.__speed=4
        
    def increase_speed(self):
        '''set speed to 8'''
        self.__speed=8
        
    def go_left(self,screen):
        '''go left, if rect.left is less than 0 no movement occurs'''
        if self.rect.left < 0:
            None
        else:
            self.rect.left-=self.__speed
    
    def go_right(self,screen):
        '''go right, if rect.right is greater than screen width no movement occurs'''
        if self.rect.right > screen.get_width():
            None
        else:
            self.rect.right+=self.__speed

    def go_up(self,screen):
        '''go up if rect.top is less than screen height no movement occurs'''
        if self.rect.top < 100:
            None
        else:
            self.rect.top-=self.__speed
    
    def go_down(self,screen):
        '''go up if rect.bottom is greater than screen height no movement occurs'''
        if self.rect.bottom > screen.get_height():
            None
        else:
            self.rect.bottom+=self.__speed
    
    def get_angle(self):
        '''returns current angle'''
        return self.__angle
    
    def get_bullet_spawn_pos(self):
        """Returns the correct position where bullets should spawn based on current weapon"""
        # Get the offset for the current weapon
        offset_x, offset_y = self.__gun_offsets[self.__current_weapon]
        
        # Convert angle to radians
        angle_rad = math.radians(self.__angle)
        
        # Calculate rotated offset
        rotated_x = offset_x * math.cos(angle_rad) - offset_y * math.sin(angle_rad)
        rotated_y = offset_x * math.sin(angle_rad) + offset_y * math.cos(angle_rad)
        
        # Return position adjusted by offset
        return (self.rect.centerx + rotated_x, self.rect.centery + rotated_y)
    
    def set_weapon(self, weapon_index):
        """Sets the current weapon and updates the player image"""
        self.__current_weapon = weapon_index
        self.change_image(weapon_index)
        # If we have a last known mouse position, update rotation
        if self.__last_mouse_pos:
            self.rotate(self.__last_mouse_pos)
    
    def rotate(self,mouse_pos):
        '''accepts mouse position and rotates player towards it'''
        self.__last_mouse_pos = mouse_pos  # Store last mouse position
        self.__angle = math.degrees(math.atan2(
            self.rect.centerx-mouse_pos[0], 
            self.rect.centery-mouse_pos[1]))
        
        self.image = pygame.transform.rotate(self.__saved_image, self.__angle)
        self.rect = self.image.get_rect(center=self.rect.center)
    
    def change_image(self, weapon):
        """Accepts an index(weapon). Changes the player image based on index."""
        try:
            image_path = f'./player/player_gun_{weapon+1}-0.png'
            self.image = pygame.image.load(image_path)
            self.image = self.image.convert_alpha()
            self.__saved_image = self.image
            # Maintain position when changing weapons
            old_center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = old_center
        except pygame.error as e:
            print(f"Error loading player image: {image_path} - {e}")

class Bullet(pygame.sprite.Sprite):
    '''Has speed and damage varaibles. Rotates based on player's current angle.
    An image can be passed it and then it becomes a bullet_img, but if no
    image is passed in it becomes a bullet_hitbox'''
    def __init__(self, image, angle, spawn_pos, mouse_pos, speed, damage, double_damage):
        pygame.sprite.Sprite.__init__(self)
        
        # Assign the bullet damage to a variable
        if double_damage:
            self.__damage = damage * 2
        else:
            self.__damage = damage
        self.__min_damage = damage
        self.__max_damage = damage * 2
        
        # Use spawn position instead of player position
        self.__x = spawn_pos[0]
        self.__y = spawn_pos[1]
        
        # Assign the mouse target position
        self.__target_x = mouse_pos[0]
        self.__target_y = mouse_pos[1]
        
        if image:
            self.image = image
            self.image.convert()
            self.rect = self.image.get_rect()
            self.rect.center = (self.__x, self.__y)
            self.image = pygame.transform.rotate(self.image, angle)
            self.rect = self.image.get_rect(center=self.rect.center)
        else:
            self.image = pygame.Surface((5,5))
            self.image.fill((255,0,0))
            self.image.set_alpha(0)
            self.rect = self.image.get_rect()
            self.rect.center = (self.__x, self.__y)
        
        # Calculate distance and step amount
        self.__distance = math.sqrt(
            pow(self.__target_x - self.__x, 2) + 
            pow(self.__target_y - self.__y, 2)
        )
        self.__animation_steps = self.__distance / speed
        self.__dx = (self.__target_x - self.__x) / self.__animation_steps
        self.__dy = (self.__target_y - self.__y) / self.__animation_steps
        
    def get_damage(self):
        '''get damage'''
        return self.__damage
    
    def update(self):
        '''move the rect and if it goes off screen, it is killed'''
        self.rect.centerx+=self.__dx
        self.rect.centery+=self.__dy
        # Get the screen dimensions from the rect since we don't have direct screen access
        screen_width = 1920  # Full screen width
        screen_height = 1080  # Full screen height
        if (self.rect.top < 0 or self.rect.bottom > screen_height or 
            self.rect.left < 0 or self.rect.right > screen_width):
            self.kill()
        
class RailGun(pygame.sprite.Sprite):
    '''generates a railgun and when self alpha is 0, the sprite is killed'''
    def __init__(self,screen,player_pos,mouse_pos):
        '''accepts mouse position, draws line towards mouse position'''
        pygame.sprite.Sprite.__init__(self)
        #Set original image
        self.image = pygame.Surface(screen.get_size())
        self.image.fill((255,255,255))
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()  
        self.rect.left=0
        self.rect.top=0
        pygame.draw.aaline(self.image, (255, 0, 0), player_pos, mouse_pos, 1)
        
        #Assign alpha value
        self.__alpha=255
    
    def update(self):
        '''subtract alpha and kill when it is 0 or less'''
        self.image.set_alpha(self.__alpha)
        self.__alpha-=30
        if self.__alpha<=0:
            self.kill()
            
class Powerup(pygame.sprite.Sprite):
    '''power sprite has accepts an image and blits on enemy's fallen location.
    It has a type to show what kind of power up it is'''
    def __init__(self,location,num,image):
        '''accepts location, num/type, image'''

        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        self.image=image
        self.rect = self.image.get_rect()
        self.rect.center = location

        self.__type=num
        
        self.__count=0
        self.__alpha=255

    def get_type(self):
        '''This method return the type of the power up'''
        return self.__type
    
    def update(self):
        '''adds to count and if count becomes greater than 300, fade effect occurs
        when image is completely transparent, it is killed'''
        self.__count+=1
        if self.__alpha==0:
            self.kill()
        elif self.__count>=300:
            self.image.set_alpha(self.__alpha)
            self.__alpha-=3
