import arcade
import glob
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Astral Escape"
wallHeight = (SCREEN_HEIGHT/2)+200

PlayerSpeed = 3
ShiftSpeed = PlayerSpeed * 3

frames = []
for file in glob.glob("assets/spacecraft_frames/*.png"):
    frame = arcade.load_texture(file)
    frames.append(frame)

print (frames)


class MyGame(arcade.Window):

    def __init__(self): 

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.csscolor.BLACK)


        self.shapes = arcade.ShapeElementList()

        color1 = (188, 155, 189)
        color2 = (165, 205, 212)

        points = (0, 0), (SCREEN_WIDTH, 0), (SCREEN_WIDTH, SCREEN_HEIGHT), (0, SCREEN_HEIGHT)

        colors = (color1, color2, color2, color2)

        rect = arcade.create_rectangle_filled_with_colors(points, colors)

        self.shapes.append(rect)


        self.scene = None

        self.physics_engine = None
        self.coin_engine = None
        self.meteor_engine = None

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.shift_pressed = False

        self.PlayerHP = 5

        self.score = 0
        

        self.frameTrack = 0
        self.timeTrack = 0

        self.coinBoost = False
        self.coinSec = 0

        self.existingMeteorList = []

        self.frameIndex=0
        


    def setup(self): 
        

        self.scene = arcade.Scene()

        self.scene.add_sprite_list("Rocket")
        self.scene.add_sprite_list("Walls")
        self.scene.add_sprite_list("OuterWalls")

        self.scene.add_sprite_list("Coins")
        self.scene.add_sprite_list("Meteors")


        self.player_list = arcade.SpriteList()
        self.meteor_list = arcade.SpriteList(); 


        self.player_sprite = arcade.Sprite("assets/spacecraft_a_2.png",0.1) #file location , Sprite Scaling (1 = 100%)
        self.player_sprite.center_x=400
        self.player_sprite.center_y=400


        self.scene.add_sprite("Rocket",self.player_sprite)


        # Adding walls
        for chunk in range(0,SCREEN_WIDTH+200,10): #wall is 50x50 1/5 = 0.2 
            wall =  arcade.Sprite("assets/test_invisible_wall.png",0.2) #file location , Sprite Scaling (1 = 100%)
            wall.center_x=chunk
            wall.center_y=0
            self.scene.add_sprite("OuterWalls",wall)

        for chunk in range(0,SCREEN_WIDTH+10,10): #wall is 50x50 1/5 = 0.2 
            wall =  arcade.Sprite("assets/test_invisible_wall.png",0.2) #file location , Sprite Scaling (1 = 100%)
            wall.center_x=chunk
            wall.center_y=wallHeight
            self.scene.add_sprite("Walls",wall)

        for chunk in range(0,SCREEN_WIDTH+10,10): #wall is 50x50 1/5 = 0.2 
            wall =  arcade.Sprite("assets/test_invisible_wall.png",0.2) #file location , Sprite Scaling (1 = 100%)
            wall.center_x=chunk
            wall.center_y=20
            self.scene.add_sprite("Walls",wall)

        for chunk in range(0,int(wallHeight),10): #wall is 50x50 1/5 = 0.2 
            wall =  arcade.Sprite("assets/test_invisible_wall.png",0.2) #file location , Sprite Scaling (1 = 100%)
            wall.center_x=20
            wall.center_y=chunk
            self.scene.add_sprite("Walls",wall)
          
        for chunk in range(0,int(wallHeight),10): #wall is 50x50 1/5 = 0.2 
            wall =  arcade.Sprite("assets/test_invisible_wall.png",0.2) #file location , Sprite Scaling (1 = 100%)
            wall.center_x=SCREEN_WIDTH-20
            wall.center_y=chunk
            self.scene.add_sprite("Walls",wall)



        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.scene["Walls"]
        )

        self.coin_engines=[]

        for coin in self.scene["Coins"]:
          coin_engine = arcade.PhysicsEngineSimple(
              coin, None
          )
          self.coin_engines.append(coin_engine)

        self.meteor_engines=[]
        self.existingCoinList=[]



        
        pass

    
    def on_draw(self):

        self.clear()
        self.shapes.draw()

        frame=frames[self.frameIndex]
        frame.draw_sized(self.player_sprite.center_x, self.player_sprite.center_y, frame.width*0.1, frame.height*0.1)

        


        self.scene.draw()
        

    def updatePlayerSpeed(self):
        
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.up_pressed and not self.down_pressed:
            if self.shift_pressed:
                self.player_sprite.change_y = ShiftSpeed
            else:
                self.player_sprite.change_y = PlayerSpeed
        elif self.down_pressed and not self.up_pressed:

            if self.shift_pressed:
                self.player_sprite.change_y = -ShiftSpeed
            else:
                self.player_sprite.change_y = -PlayerSpeed
            


        if self.left_pressed and not self.right_pressed:

            if self.shift_pressed:
                self.player_sprite.change_x = -ShiftSpeed
            else:
                self.player_sprite.change_x = -PlayerSpeed 
            
        elif self.right_pressed and not self.left_pressed:
            if self.shift_pressed:
                self.player_sprite.change_x = ShiftSpeed
            else:
                self.player_sprite.change_x = PlayerSpeed 
            
      
        


    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
            self.updatePlayerSpeed()
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True
            self.updatePlayerSpeed()
        elif key == arcade.key.UP or key == arcade.key.W: #We need to set max height a player can move
            self.up_pressed = True
            self.updatePlayerSpeed()
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
            self.updatePlayerSpeed()
        if key == arcade.key.LSHIFT or key == arcade.key.RSHIFT:
            self.shift_pressed = True
            self.updatePlayerSpeed()
        #elif key == arcade.key.SPACE: # spacebeam
            #   

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
            self.updatePlayerSpeed()
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False
            self.updatePlayerSpeed()
        elif key == arcade.key.UP or key == arcade.key.W: #We need to set max height a player can move
            self.up_pressed = False
            self.updatePlayerSpeed()
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
            self.updatePlayerSpeed()
        if key == arcade.key.LSHIFT or key == arcade.key.RSHIFT:
            self.shift_pressed = False
            self.updatePlayerSpeed()

    def on_update(self,delta_time):
        ## movement and game logic in here
        self.physics_engine.update()

        for coin_engine in self.coin_engines:
            coin_engine.update()

        

        for meteor_engine in self.meteor_engines:
            meteor_engine.update()





        for coin in self.scene["Coins"]:
          coin.change_y = -PlayerSpeed *2


        for meteor in self.scene["Meteors"]:
           
            if(self.coinBoost):meteor.change_y = -PlayerSpeed * 5
            else:meteor.change_y = -PlayerSpeed * 2
        # for coin in self.scene["Coins"]:
        #     coin.change_y = -PlayerSpeed

        self.score=self.score+0.01

        meteorDamage = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["Meteors"]
        )

        for meteor in meteorDamage:
            meteor.remove_from_sprite_lists()
            self.PlayerHP = self.PlayerHP - 1
            print(self.PlayerHP)


        coinCatch = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["Coins"]
        )

        for coin in coinCatch:
            coin.remove_from_sprite_lists()
            self.score=self.score+20
            self.coinBoost=True


        for chunk in self.scene["OuterWalls"]:
          meteorDestroy = arcade.check_for_collision_with_list(
            chunk, self.scene["Meteors"]
          )
          for meteor in meteorDestroy:
              
              meteor.remove_from_sprite_lists()

        for chunk in self.scene["OuterWalls"]:
          coinDestroy = arcade.check_for_collision_with_list(
            chunk, self.scene["Coins"]
          )
          for coin in coinDestroy:
              coin.remove_from_sprite_lists()

        if self.PlayerHP<=0:
          arcade.get_window().close()#make it to go to game over screen when ==0

        self.frameTrack=self.frameTrack+1

        if (self.frameTrack%10==0):
            if (self.frameIndex==1):
                self.frameIndex=0
            else:
                self.frameIndex=1


        seconds=int(self.frameTrack/60)

        if self.coinBoost == False:
            self.coinSec = seconds
        
        if(self.timeTrack!=seconds):

            if (self.timeTrack==self.coinSec+2):
                self.coinBoost = False

            

            self.timeTrack=seconds
            if (self.timeTrack%5==0):
                randomNumber=random.randrange(10,790)

                coin=arcade.Sprite("assets/coin.png",0.1)
                coin.center_x=randomNumber # will need to add some randomness here
                coin.center_y=SCREEN_HEIGHT
                coin.change_angle=random.randrange(-2,2)
                self.scene.add_sprite("Coins",coin)

                for coin in self.scene["Coins"]:
                    if coin not in self.existingCoinList:
                        coin_engine = arcade.PhysicsEngineSimple(
                            coin, None
                        )
                        self.coin_engines.append(coin_engine)
                        self.existingCoinList.append(coin)

            elif (self.timeTrack%1==0):
## 50-50 chance for which meteor to generate


                
                
                def meteorSpawn(): 
                    randomRadial=random.randrange(-5,5)
                    randomNumber=random.randrange(10,790)

                    meteorSpawnNum = random.randrange(3)

                    if(meteorSpawnNum==1):
                        meteor=arcade.Sprite("assets/meteorite01.png",0.1)
                        meteor.center_x=randomNumber+random.randrange(-200,200) # will need to add some randomness here
                        meteor.center_y=SCREEN_HEIGHT+random.randrange(20,500)
                        meteor.change_angle=randomRadial
                        self.scene.add_sprite("Meteors",meteor)
                    elif(meteorSpawnNum==2):
                        meteor2=arcade.Sprite("assets/meteorite02.png",0.1)
                        meteor2.center_x=randomNumber+random.randrange(-200,200) # will need to add some randomness here
                        meteor2.center_y=SCREEN_HEIGHT+random.randrange(20,500)
                        meteor2.change_angle=randomRadial

                        self.scene.add_sprite("Meteors",meteor2)
                    else:
                        meteor=arcade.Sprite("assets/meteorite01.png",0.1)
                        meteor.center_x=randomNumber+random.randrange(-200,200) # will need to add some randomness here
                        meteor.center_y=SCREEN_HEIGHT+random.randrange(20,500)
                        meteor.change_angle=randomRadial

                        self.scene.add_sprite("Meteors",meteor)

                        meteor2=arcade.Sprite("assets/meteorite02.png",0.1)
                        meteor2.center_x=randomNumber+random.randrange(-200,200) # will need to add some randomness here
                        meteor2.center_y=SCREEN_HEIGHT+random.randrange(20,500)
                        meteor2.change_angle=randomRadial

                        self.scene.add_sprite("Meteors",meteor2)

                #if difficulty hard
                meteorSpawn()
                meteorSpawn()
                meteorSpawn()
                meteorSpawn()
                meteorSpawn()
                meteorSpawn()

                #if difficulty normal

                # meteorSpawn()
                # meteorSpawn()
                # meteorSpawn()

                #if difficulty easy

                # meteorSpawn()
                
                

                

                
                

                
                for meteor in self.scene["Meteors"]:
                    if meteor not in self.existingMeteorList:
                        meteor_engine = arcade.PhysicsEngineSimple(
                            meteor, None
                        )
                        self.meteor_engines.append(meteor_engine)
                        self.existingMeteorList.append(meteor)

                

        
        

        



        

        
           
            
        # print (self.score)
            


    

          

def main():

    window = MyGame()

    window.setup()

    arcade.run()

if __name__ == "__main__":
    main()
    
    
    
