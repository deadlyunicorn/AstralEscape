import arcade
import arcade.gui
import glob
import random
from datetime import date

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Astral Escape v1.0.0"
wallHeight = (SCREEN_HEIGHT/2)+200

PlayerSpeed = 3
ShiftSpeed = PlayerSpeed * 3

playerCount=1 #global player count setting

frames = [] #used for animating spacecrafts
frames2 = []

for file in glob.glob("assets/spacecraft_frames/*1.png"):
    frame = arcade.load_texture(file)
    frames.append(frame)

for file in glob.glob("assets/spacecraft_frames/*2.png"):
    frame = arcade.load_texture(file)
    frames2.append(frame)


difficulty=1 #global difficulty setting


class mainGameView(arcade.View): #main game class

    def __init__(self): 

        #initializing game properties
        super().__init__()

        self.window.set_mouse_visible(False) #invisible mouse in game
        self.paused = False

        self.scene = None


        #player physics engines (used for movement)
        self.physics_engine = None
        self.physics2_engine = None


        self.coin_engine = None
        self.meteor_engine = None

        self.coinSpeedVarience=0


        #player control states
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.shift_pressed = False

        #player2 controls
        self.left_pressed2 = False
        self.right_pressed2 = False
        self.up_pressed2 = False
        self.down_pressed2 = False

        self.shift_pressed2 = False

        #Health
        self.PlayerHP = 5
        self.PlayerHP2 = 5


        #score
        self.score1 = 0
        self.score2 = 0
        
        #used for keeping track of time
        self.frameTrack = 0
        self.timeTrack = 0
        self.frameIndex=0 #used for animation

        #used for giving players speed boost (both)
        #and bonus score (only the one catching the coin)
        self.coinBoost = False
        self.coinBoost2 = False
        self.coinSec = 0 #used for boost duration

        #used for destroyed spaceship display on multiplayer
        self.playerLastAlive=0 
        self.playerLastAlive2=0

        #used for cleaning up meteors
        self.existingMeteorList = []

    
        self.meteorDestroy=[]
        self.coinDestroy=[] #there is actually 1 coin at a time on screen

        self.background = None
        self.backgroundMove=0

        #rocket animation
        self.animationBoost = 10 #lower values -> faster animation

        self.playerCount=playerCount

        self.logo=None
        


    def setup(self): 
        
        #our current scene
        self.scene = arcade.Scene()

        self.scene.add_sprite_list("Rocket")

        self.scene.add_sprite_list("Walls") #player moving area
        self.scene.add_sprite_list("OuterWalls") #destroy coins and meteors leaving screen


        self.scene.add_sprite_list("Coins")
        self.scene.add_sprite_list("Meteors")


        self.player_list = arcade.SpriteList()
        self.meteor_list = arcade.SpriteList(); 


        self.player_sprite1 = arcade.Sprite("assets/spacecraft_a_2.png",0.1) #Sprite Scaling: 1 == 100%
        self.player_sprite1.center_x=400
        self.player_sprite1.center_y=400
        self.scene.add_sprite("Rocket",self.player_sprite1)


        if(self.playerCount==2):
            self.player_sprite2 = arcade.Sprite("assets/spacecraft_a_2.png",0.1) #file location , Sprite Scaling (1 = 100%)
            self.player_sprite2.center_x=400
            self.player_sprite2.center_y=400
            self.scene.add_sprite("Rocket",self.player_sprite2)


        # Adding walls

        #x axis outer wall
        for chunk in range(-200,SCREEN_WIDTH+200,10): #-200, +200 because of the way I randomly spawn meteors/coins
            wall =  arcade.Sprite("assets/invisible_wall.png",0.2) #wall is 50x50. 10x10 is 1/5 = 0.2 of that. That's also the reason we leave a step of 10
            wall.center_x=chunk
            wall.center_y=-70 #y axis
            wall.alpha=0
            self.scene.add_sprite("OuterWalls",wall)

        #upper wall for player movements
        for chunk in range(0,SCREEN_WIDTH,10): 
            wall =  arcade.Sprite("assets/invisible_wall.png",0.2)
            wall.center_x=chunk
            wall.center_y=wallHeight #the upper line a player can move up to
            wall.alpha=0
            self.scene.add_sprite("Walls",wall)


        #lower wall
        for chunk in range(0,SCREEN_WIDTH,10): 
            wall =  arcade.Sprite("assets/invisible_wall.png",0.2)
            wall.center_x=chunk
            wall.center_y=20 # the lower line a player can move up to.
            wall.alpha=0
            self.scene.add_sprite("Walls",wall)

        #left wall
        for chunk in range(20,int(wallHeight),10): #from the lower to the upper line
            wall =  arcade.Sprite("assets/invisible_wall.png",0.2)
            wall.center_x=20 #x==20
            wall.center_y=chunk
            wall.alpha=0
            self.scene.add_sprite("Walls",wall)
          
        #right wall
        for chunk in range(20,int(wallHeight),10): #wall is 50x50 1/5 = 0.2 
            wall =  arcade.Sprite("assets/invisible_wall.png",0.2) #file location , Sprite Scaling (1 = 100%)
            wall.center_x=SCREEN_WIDTH-20 #x==780
            wall.center_y=chunk
            wall.alpha=0
            self.scene.add_sprite("Walls",wall)

        ##prevent player from moving against the walls
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite1, self.scene["Walls"]
        )

        if playerCount==2:
            self.physics_engine2 = arcade.PhysicsEngineSimple(
            self.player_sprite2, self.scene["Walls"]
        )
        ##


        #each coin has its own physics engine in order to move
        self.coin_engines=[]

        for coin in self.scene["Coins"]:
          coin_engine = arcade.PhysicsEngineSimple(
              coin, None
          )
          self.coin_engines.append(coin_engine)

        #If we instead of 'None' use 'OuterWall'
        #The coin will never touch-collide with the outerwall 
        #So we won't be able to remove it. It will just stop moving 
        
        self.existingCoinList=[]

        self.meteor_engines=[]

        
        self.background=arcade.load_texture("assets/space.png")

        self.heartTexture=arcade.load_texture("assets/heart.png")
        self.heartTexture2=arcade.load_texture("assets/heart2.png")
        self.logo = arcade.load_texture("assets/logo.png")



        
        pass

    
    def on_draw(self):

        
        self.clear() #delete the previous frame
        

        #our background with the sliding logic
        arcade.draw_lrwh_rectangle_textured(0, -self.backgroundMove,
                                            SCREEN_WIDTH, 4000,
                                            self.background)
        
        
        

        #player 1
        if self.PlayerHP>0:


        #When Alive

            #draw animation over sprite
            frame=frames[self.frameIndex]
            frame.draw_sized(self.player_sprite1.center_x, self.player_sprite1.center_y, frame.width*0.1, frame.height*0.1)
            
            #score update for player 1
            if(self.frameTrack%30==0):
                self.score1=self.score1+1
                
                #bonus score when shift is pressed
                if(self.shift_pressed and (self.up_pressed or self.left_pressed or self.down_pressed or self.right_pressed )):
                    self.score1=self.score1+1


            #bonus score when player1 catches the coin
            if (self.coinBoost and self.frameTrack%6==0):
                self.score1=self.score1+1
            #coinBoost won't give instantly +bonus points, but gradually
        

        #up until 5 seconds after death
        elif(self.playerLastAlive+5>self.frameTrack/60):
            frame=arcade.load_texture("assets/spacecraft_destroyed.png")
            frame.draw_sized(self.player_sprite1.center_x, self.player_sprite1.center_y, frame.width*0.2, frame.height*0.2,alpha=255-(2.45*(self.frameTrack-self.playerLastAlive*60)/3))
            self.player_sprite1.alpha=0

        #5 seconds after death
        else:
            #Basically self.player_sprite1.kill() wasn't working, 
            # so there is an invisible spacecraft behind the alive player.
            # This gives them the ability to "burn" meteors. (only in 2P mode)
            self.player_sprite1.center_x=self.player_sprite2.center_x
            self.player_sprite1.center_y=self.player_sprite2.center_y-20
            
            
        #Player2
        if playerCount==2:

            if self.PlayerHP2>0:
                #Alive

                frame2=frames2[self.frameIndex]
                frame2.draw_sized(self.player_sprite2.center_x, self.player_sprite2.center_y, frame2.width*0.1, frame2.height*0.1)
                
                if (self.coinBoost2 and self.frameTrack%6==0):
                    self.score2=self.score2+1

                if(self.frameTrack%30==0):
                    self.score2=self.score2+1

                    if(self.shift_pressed2 and ( self.up_pressed2 or self.left_pressed2 or self.down_pressed2 or self.right_pressed2 )):
                        self.score2=self.score2+1
            
            elif(self.playerLastAlive2+5>self.frameTrack/60): #recently died
                frame2=arcade.load_texture("assets/spacecraft_destroyed.png")
                frame2.draw_sized(self.player_sprite2.center_x, self.player_sprite2.center_y, frame2.width*0.2, frame2.height*0.2,alpha=255-(2.45*(self.frameTrack-self.playerLastAlive2*60)/3))
                self.player_sprite2.alpha=0
                
            else:
                self.player_sprite2.texture= arcade.load_texture("assets/invisible_wall.png")
                self.player_sprite2.center_x=self.player_sprite1.center_x
                self.player_sprite2.center_y=self.player_sprite1.center_y-20
                
                
        #Score display        
        if playerCount==2:
            arcade.draw_rectangle_filled(400,750,170,70,(0,0,0,150))
            arcade.draw_text(("Player 1: "+str(self.score1)),0,750,font_size=14,align="center",width=800)
            arcade.draw_text(("Player 2: "+str(self.score2)),0,730,font_size=14,align="center",width=800)
        else:
            arcade.draw_rectangle_filled(400,760,170,40,(0,0,0,150))
            arcade.draw_text(("Score is: "+str(self.score1)),0,750,font_size=14,align="center",width=800)


        #Health display
        arcade.draw_lrwh_rectangle_textured(800-69,748,20,18,self.heartTexture)
        arcade.draw_text(("x"+str(self.PlayerHP)),-20,750,font_size=14,align="right",width=800,font_name="calibri")

        if playerCount==2:
            arcade.draw_lrwh_rectangle_textured(800-69,728,20,18,self.heartTexture2)
            arcade.draw_text(("x"+str(self.PlayerHP2)),-20,730,font_size=14,align="right",width=800,font_name="calibri")


        self.scene.draw()

        if self.paused: #draw on top of all of the above

            arcade.draw_rectangle_filled(400,400,800,800,(0,0,50,150)) #transparent rectangle
            arcade.draw_lrwh_rectangle_textured(150,0,800,800,self.logo) #logo
            arcade.draw_text(text="Game is paused",start_x=50,start_y=520,font_size=16,align="center",width=700)
            arcade.draw_text(text="END GAME: 'H' key",start_x=550,start_y=61,font_size=12)
            arcade.draw_text(text="PAUSE: Esc key",start_x=550,start_y=43,font_size=12)
            arcade.draw_text(text="MOVE: Arrow keys or WASD",start_x=550,start_y=24,font_size=12)
            arcade.draw_text(text="BOOST: SHIFT key",start_x=550,start_y=5,font_size=12)


    def meteorSpawn(self): 
        randomRadial=random.randrange(-5,5)
        randomNumber=random.randrange(10,790)
        randomScale=random.randrange(100,110)/1000

        meteorSpawnNum = random.randrange(3)

        if(meteorSpawnNum==1):
            meteor=arcade.Sprite("assets/meteorite01.png",0.1)
            meteor.center_x=randomNumber+random.randrange(-200,200) 
            meteor.center_y=SCREEN_HEIGHT+random.randrange(20,500)
            meteor.change_angle=randomRadial
            meteor.scale=randomScale
            self.scene.add_sprite("Meteors",meteor)

        elif(meteorSpawnNum==2):
            meteor2=arcade.Sprite("assets/meteorite02.png",0.1)
            meteor2.center_x=randomNumber+random.randrange(-200,200) 
            meteor2.center_y=SCREEN_HEIGHT+random.randrange(20,500)
            meteor2.change_angle=randomRadial
            meteor2.scale=randomScale
            self.scene.add_sprite("Meteors",meteor2)

        else:
            meteor=arcade.Sprite("assets/meteorite01.png",0.1)
            meteor.center_x=randomNumber+random.randrange(-200,200) 
            meteor.center_y=SCREEN_HEIGHT+random.randrange(20,500)
            meteor.change_angle=randomRadial
            meteor.scale=randomScale
            self.scene.add_sprite("Meteors",meteor)

            meteor2=arcade.Sprite("assets/meteorite02.png",0.1)
            meteor2.center_x=randomNumber+random.randrange(-200,200)
            meteor2.center_y=SCREEN_HEIGHT+random.randrange(20,500)
            meteor2.change_angle=randomRadial
            meteor2.scale=randomScale
            self.scene.add_sprite("Meteors",meteor2)

    def updatePlayerSpeed(self):
        

        #initial speed is 0 each frame.
        self.player_sprite1.change_x = 0
        self.player_sprite1.change_y = 0

        if playerCount==2:
            self.player_sprite2.change_x = 0
            self.player_sprite2.change_y = 0

            
        #movement of player 1
        if self.PlayerHP>0:

            if self.up_pressed and not self.down_pressed: #up 
                #if both up and down are pressed
                #y change is 0.
              
                if self.shift_pressed: #speed boost
                    self.player_sprite1.change_y = ShiftSpeed
                else:
                    self.player_sprite1.change_y = PlayerSpeed
            
            elif self.down_pressed and not self.up_pressed: #down

                if self.shift_pressed:
                    self.player_sprite1.change_y = -ShiftSpeed
                else:
                    self.player_sprite1.change_y = -PlayerSpeed


            if self.left_pressed and not self.right_pressed: #left

                if self.shift_pressed:
                    self.player_sprite1.change_x = -ShiftSpeed
                else:
                    self.player_sprite1.change_x = -PlayerSpeed 
                
            elif self.right_pressed and not self.left_pressed: #right
                if self.shift_pressed:
                    self.player_sprite1.change_x = ShiftSpeed
                else:
                    self.player_sprite1.change_x = PlayerSpeed

        if playerCount==2:
            

            #movement of destroyed spacecraft

            if self.PlayerHP==0 and self.playerLastAlive+5>self.frameTrack//60:
                self.player_sprite1.change_y = -1

            if self.PlayerHP2==0 and self.playerLastAlive2+5>self.frameTrack//60:
                self.player_sprite2.change_y = -1


            #movement of player 2
            if self.PlayerHP2>0:

                if self.up_pressed2 and not self.down_pressed2: #up
                    if self.shift_pressed2:
                        self.player_sprite2.change_y = ShiftSpeed
                    else:
                        self.player_sprite2.change_y = PlayerSpeed
                elif self.down_pressed2 and not self.up_pressed2: #down
 
                    if self.shift_pressed2:
                        self.player_sprite2.change_y = -ShiftSpeed
                    else:
                        self.player_sprite2.change_y = -PlayerSpeed

                if self.left_pressed2 and not self.right_pressed2: #left

                    if self.shift_pressed2:
                        self.player_sprite2.change_x = -ShiftSpeed
                    else:
                        self.player_sprite2.change_x = -PlayerSpeed 
                    
                elif self.right_pressed2 and not self.left_pressed2: #right
                    if self.shift_pressed2:
                        self.player_sprite2.change_x = ShiftSpeed
                    else:
                        self.player_sprite2.change_x = PlayerSpeed
            
    def saveGame(self): #write score into file
        scoreFile=open("AstralEscapeScore.txt","a")

        scoreFile.write("\nSTART----------\n\n")
        scoreFile.write("Difficulty: ")

        if difficulty==1:
            scoreFile.write("EASY;\n")
        elif difficulty==2:
            scoreFile.write("NORMAL;\n")
        elif difficulty==3:
            scoreFile.write("HARD;\n")
                
        scoreFile.write("Score: "+str(self.score1)+";\n")
        scoreFile.write("Date: "+str(date.today())+";\n")
        scoreFile.write("\nEND------------\n")

        if playerCount==2:

            scoreFile.write("\nSTART----------\n\n")
            scoreFile.write("Difficulty: ")

            if difficulty==1:
                scoreFile.write("EASY;\n")
            elif difficulty==2:
                scoreFile.write("NORMAL;\n")
            elif difficulty==3:
                scoreFile.write("HARD;\n")
                    
            scoreFile.write("Score: "+str(self.score2)+";\n")
            scoreFile.write("Date: "+str(date.today())+"(P2)"+";\n")
            scoreFile.write("\nEND------------\n")
        

    def on_key_press(self, key, modifiers): 

        if (self.playerCount==1):
            #Singleplayer mode


            if key == arcade.key.LEFT or key == arcade.key.A:
                self.left_pressed = True
            elif key == arcade.key.RIGHT or key == arcade.key.D:
                self.right_pressed = True
            elif key == arcade.key.UP or key == arcade.key.W: #We need to set max height a player can move
                self.up_pressed = True
            elif key == arcade.key.DOWN or key == arcade.key.S:
                self.down_pressed = True
            if key == arcade.key.LSHIFT or key == arcade.key.RSHIFT:
                self.shift_pressed = True


        elif (self.playerCount==2):
            #Multiplayer mode


            #Player 1

            if key == arcade.key.LEFT:
                self.left_pressed = True
                
            elif key == arcade.key.RIGHT:
                self.right_pressed = True

            elif key == arcade.key.UP:
                self.up_pressed = True

            elif key == arcade.key.DOWN:
                self.down_pressed = True

            if key == arcade.key.RSHIFT:
                self.shift_pressed = True


            #Player 2

            if key == arcade.key.A:
                self.left_pressed2 = True

            elif key == arcade.key.D:
                self.right_pressed2 = True

            elif key == arcade.key.W: 
                self.up_pressed2 = True
            elif key == arcade.key.S:
                self.down_pressed2 = True

            if key == arcade.key.LSHIFT:
                self.shift_pressed2 = True

        self.updatePlayerSpeed()


        if key == arcade.key.ESCAPE:
            self.paused=not self.paused #pause-unpause

        if key == arcade.key.H and self.paused:
            self.saveGame()

            #gameOver()
            gameOverView = gameOverMenu(self.score1,self.score2)
            gameOverView.setup()
            self.window.show_view(gameOverView)
            

    def on_key_release(self, key, modifiers):
        
        if (self.playerCount==1):
            #Singleplayer
            
            if key == arcade.key.LEFT or key == arcade.key.A:
                self.left_pressed = False
            elif key == arcade.key.RIGHT or key == arcade.key.D:
                self.right_pressed = False
            elif key == arcade.key.UP or key == arcade.key.W: #We need to set max height a player can move
                self.up_pressed = False
            elif key == arcade.key.DOWN or key == arcade.key.S:
                self.down_pressed = False
            if key == arcade.key.LSHIFT or key == arcade.key.RSHIFT:
                self.shift_pressed = False

        elif (self.playerCount==2):
            #Multiplayer

            #Player1
            if key == arcade.key.LEFT:
                self.left_pressed = False
            elif key == arcade.key.RIGHT:
                self.right_pressed = False
            elif key == arcade.key.UP: #We need to set max height a player can move
                self.up_pressed = False
            elif key == arcade.key.DOWN:
                self.down_pressed = False

            if key == arcade.key.RSHIFT:
                self.shift_pressed = False


            #Player 2
            if key == arcade.key.A:
                self.left_pressed2 = False
            elif key == arcade.key.D:
                self.right_pressed2 = False
            elif key == arcade.key.W: #We need to set max height a player can move
                self.up_pressed2 = False
            elif key == arcade.key.S:
                self.down_pressed2 = False

            if key == arcade.key.LSHIFT:
                self.shift_pressed2 = False

        self.updatePlayerSpeed()
        
    def on_update(self,delta_time):
        # movement and game logic in here

        if not self.paused:


            

            #Background move
            if(self.backgroundMove<3200-20): ##For a smoother change I removed 20pixels
                
                if(self.coinBoost or self.coinBoost2):
                    #when boosted
                    self.backgroundMove+=12
                
                else:
                    self.backgroundMove+=1
            
            else:
                self.backgroundMove=0 #Background gets back to starting position

            

            for coin_engine in self.coin_engines:
                coin_engine.update()

            for meteor_engine in self.meteor_engines:
                meteor_engine.update()



            for coin in self.scene["Coins"]:
                coin.change_y = -PlayerSpeed * 2 * self.coinSpeedVarience


            for meteor in self.scene["Meteors"]:
            
                if(self.coinBoost or self.coinBoost2): #when coinBoost
                    meteor.change_y = -PlayerSpeed * 5

                else:
                    meteor.change_y = -PlayerSpeed * 2
            

            #When player1 collides with a meteor
            meteorDamage = arcade.check_for_collision_with_list(
                self.player_sprite1, self.scene["Meteors"]
            )

            for meteor in meteorDamage:
             
                #Remove meteor
                meteor.remove_from_sprite_lists()
             
                #Lose hp
                if self.PlayerHP>0: 
                    self.PlayerHP = self.PlayerHP - 1


            if playerCount==2:

            #When player2 collides with a meteor
                
                meteorDamage2 = arcade.check_for_collision_with_list(
                    self.player_sprite2, self.scene["Meteors"]
                )

                for meteor in meteorDamage2:

                    meteor.remove_from_sprite_lists()
                    
                    if self.PlayerHP2>0: 
                        self.PlayerHP2 = self.PlayerHP2 - 1

            

            #When player1 catches a coin

            coinCatch = arcade.check_for_collision_with_list(
                self.player_sprite1, self.scene["Coins"]
            )

            for coin in coinCatch:
                coin.remove_from_sprite_lists()

                self.coinBoost=True #Things move faster + Player1 gets scoreboost

            if playerCount==2:

            #When player2 catches a coin

                coinCatch2 = arcade.check_for_collision_with_list(
                    self.player_sprite2, self.scene["Coins"]
                )

                for coin in coinCatch2:

                    coin.remove_from_sprite_lists()
                    
                    self.coinBoost2=True


            #Remove meteors when out of view
            for chunk in self.scene["OuterWalls"]:
                self.meteorDestroy = self.meteorDestroy+arcade.check_for_collision_with_list( #there might be multiple collisions per frame
                    chunk, self.scene["Meteors"] 
                )
                

            for meteor in self.meteorDestroy:
                meteor.remove_from_sprite_lists()

            #Remove coin
            for chunk in self.scene["OuterWalls"]:
                self.coinDestroy = self.coinDestroy + arcade.check_for_collision_with_list(
                    chunk, self.scene["Coins"]
                )

            for coin in self.coinDestroy:
                coin.remove_from_sprite_lists()




            if playerCount==1:

                self.physics_engine.update()
                
                if self.PlayerHP<=0:

                    #save score to file
                    self.saveGame()
                    
                    #gameOver Menu
                    gameOverView = gameOverMenu(self.score1,self.score2)
                    gameOverView.setup()
                    self.window.show_view(gameOverView)


            else:

                if self.PlayerHP>0:
                    #keepTrack of last seen alive -- used for death "animation"
                    self.playerLastAlive=seconds


                if self.playerLastAlive+5>seconds:
                    self.physics_engine.update()
                    
                elif(self.player_sprite1 in self.player_list): 
                    #this doesn't seem to work
                    self.player_list.remove(self.player_sprite1)


                if self.PlayerHP2>0:
                    self.playerLastAlive2=seconds

                if self.playerLastAlive2+5>seconds:
                    self.physics_engine2.update()

                elif(self.player_sprite2 in self.player_list): 
                    #doesn't seem to work
                    self.player_list.remove(self.player_sprite2)


                if self.PlayerHP<=0 and self.PlayerHP2<=0:

                    #save score to file
                    self.saveGame()

                    gameOverView = gameOverMenu(self.score1,self.score2)
                    gameOverView.setup()
                    self.window.show_view(gameOverView)


                    
            ##Below we have mechanics to be done
            ##within specific second intervals.



            #get the frame we are currently at
            self.frameTrack=self.frameTrack+1

            seconds=self.frameTrack//60 #get the current second
            #1 second == 60 frames



            #change spaceship and background animation speed based on coinboost
            if (self.coinBoost or self.coinBoost2):
                self.animationBoost=5
            else:
                self.animationBoost=10


            #lower values of animationBoost => faster animation change
            #frame index is used for the spaceship animation

            if (self.frameTrack%self.animationBoost==0):
                if (self.frameIndex==1):
                    self.frameIndex=0
                else:
                    self.frameIndex=1




            if self.coinBoost == False and self.coinBoost2 == False:
                self.coinSec = seconds 
                #save the moment coinBoost was disabled for the last time
                #so that it gets disabled again 2 seconds after that time
            

            #update per second instead of per frame below
            if(self.timeTrack!=seconds):
                #previous value is not the same as the current value
                
                self.timeTrack=seconds 


                #coinBoost lasts 2 seconds
                if (self.timeTrack==self.coinSec+2):
                    self.coinBoost = False
                    self.coinBoost2 = False



                #every 5 seconds 
                if (self.timeTrack%5==0):


                    XrandomNumber=random.randrange(10,790) #used for x axis
                    self.coinSpeedVarience=random.randint(50,200) /100
                    

                    #on hard difficulty coin scale can get smaller
                    
                    if (difficulty==3):
                        coinScale=random.randrange(60,110)/1000
                    else:
                        coinScale=random.randrange(100,110)/1000


                #Spawn coins
                    coin=arcade.Sprite("assets/coin.png",0.1)
                    coin.center_x=XrandomNumber
                    coin.center_y=SCREEN_HEIGHT
                    coin.change_angle=random.randrange(-2,2) #rotation
                    coin.scale=coinScale

                    self.scene.add_sprite("Coins",coin)

                    for coin in self.scene["Coins"]:
                        if coin not in self.existingCoinList:
                            coin_engine = arcade.PhysicsEngineSimple(
                                coin, None
                            )
                            self.coin_engines.append(coin_engine)
                            self.existingCoinList.append(coin)


                #Every 1 second
                if (self.timeTrack%1==0):

                    
                    

                #Spawn Meteorites

                    #if difficulty == hard
                    if (difficulty==3):
                    
                        for i in range(5):
                            self.meteorSpawn()
                    
                    elif difficulty==2:
                    
                        for i in range(3):
                            self.meteorSpawn()
                    
                    elif difficulty==1:
                        self.meteorSpawn()
                
                
                    for meteor in self.scene["Meteors"]:
                
                        if meteor not in self.existingMeteorList:
                            #meteors without a physics engine

                            meteor_engine = arcade.PhysicsEngineSimple(
                                meteor, None
                            )
                
                            self.meteor_engines.append(meteor_engine)
                            self.existingMeteorList.append(meteor)
                    
            


class mainMenu(arcade.View):



    def __init__(self): 



        super().__init__()

        #mouse visible
        self.window.set_mouse_visible(True)
        

        self.scene = None
        
        self.background = arcade.load_texture("assets/space.png")
        self.logo = arcade.load_texture("assets/logo.png")

        self.frameTrack=0
        self.frameIndex=0



        ## Needed for the buttons
        self.manager=None
       
    def setup(self): 
        
        self.manager = arcade.gui.UIManager()
        self.manager.enable() #needs to get disabled when exiting the view
            #else you can still click the buttons.
        

        #~~~~~~~~~~~~~~~~Difficulty Buttons~~~~~~~~~~~~~~~~
        self.difficultyBox = arcade.gui.UIBoxLayout(vertical=False)

        easyButton = arcade.gui.UIFlatButton(text="Easy", width=100)
        self.difficultyBox.add(easyButton.with_space_around(right=20))


        mediumButton = arcade.gui.UIFlatButton(text="Medium", width=100)
        self.difficultyBox.add(mediumButton.with_space_around(right=20))
        
        
        hardButton = arcade.gui.UIFlatButton(text="Hard", width=100)
        self.difficultyBox.add(hardButton.with_space_around(right=20))


        @easyButton.event("on_click")
        def on_click_settings(event):
            global difficulty
            difficulty=1

        @mediumButton.event("on_click")
        def on_click_settings(event):
            global difficulty
            difficulty=2

        @hardButton.event("on_click")
        def on_click_settings(event):
            global difficulty
            difficulty=3

        #~~~~~~~~~~~~~~~~Difficulty Buttons~~~~~~~~~~~~~~~~




        #~~~~~~~~~~~~~~~~Buttons that do things~~~~~~~~~~~~~~~~
        self.v_box = arcade.gui.UIBoxLayout()


        playButton = arcade.gui.UIFlatButton(text="Start Game", width=200)
        self.v_box.add(playButton.with_space_around(bottom=20))

        playerCountButton = arcade.gui.UIFlatButton(text="Players: ", width=200)
        self.v_box.add(playerCountButton.with_space_around(bottom=20))

        scoreButton = arcade.gui.UIFlatButton(text="Score", width=200)
        self.v_box.add(scoreButton.with_space_around(bottom=20))

        creditsButton = arcade.gui.UIFlatButton(text="Credits", width=200)
        self.v_box.add(creditsButton.with_space_around(bottom=20))

        exitButton = arcade.gui.UIFlatButton(text="Exit", width=200)
        self.v_box.add(exitButton.with_space_around(bottom=20))

        @playButton.event("on_click")
        def on_click_settings(event):
            gameView=mainGameView()
            gameView.setup()
            self.window.show_view(gameView)

        @playerCountButton.event("on_click")
        def on_click_settings(event):
            global playerCount
            if playerCount==1:
                playerCount=2
            else: playerCount=1


        @scoreButton.event("on_click")
        def on_click_settings(event):
            currentView=scoreMenu()
            currentView.setup()
            self.window.show_view(currentView)

        @creditsButton.event("on_click")
        def on_click_settings(event):
            currentView=creditsMenu()
            currentView.setup()
            self.window.show_view(currentView)

        @exitButton.event("on_click")
        def on_click_settings(event):
            arcade.exit()

        #~~~~~~~~~~~~~~~~Buttons that do things~~~~~~~~~~~~~~~~

        
        
        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                align_x= 150,
                align_y= 0,
                anchor_x="left",
                anchor_y="center_y",
                child=self.v_box),
        )

        # Create a widget to hold the difficulty buttons widget, that will center the buttons

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                align_x= 70,
                align_y= 50,
                anchor_x="left",
                anchor_y="bottom",
                child=self.difficultyBox),
        )
        
        pass


    def on_hide_view(self): #when view is hidden disable the buttons
        self.manager.disable()


    def on_draw(self):

        self.clear()

        arcade.draw_lrwh_rectangle_textured(
            0, 0,
            SCREEN_WIDTH, 4000,
            self.background  #background
        )


        frame=frames[self.frameIndex] #Spacecraft
        frame.draw_sized(630, 380, frame.width*0.8, frame.height*0.8)

        arcade.draw_lrwh_rectangle_textured(0,20,800,800,self.logo) #Logo


        #~~~~~~~~~~~~~~~~Difficulty Buttons Interface~~~~~~~~~~~~~~~~

        arcade.draw_text(text="Difficulty",start_x=180,start_y=140,font_size=24,align="left",width=400)

        #Arrows above the buttons

        if difficulty==1:
            arcade.draw_text(text="l",start_x=120,start_y=108,font_size=24,align="left",width=400,color=(90,90,250))
            arcade.draw_text(text="v",start_x=118,start_y=106,font_size=19,align="left",width=400,color=(90,90,250))
        
        elif difficulty==2:
            arcade.draw_text(text="l",start_x=240,start_y=108,font_size=24,align="left",width=400,color=(90,90,250))
            arcade.draw_text(text="v",start_x=238,start_y=106,font_size=19,align="left",width=400,color=(90,90,250))

        elif difficulty==3:
            arcade.draw_text(text="l",start_x=360,start_y=108,font_size=24,align="left",width=400,color=(90,90,250))
            arcade.draw_text(text="v",start_x=358,start_y=106,font_size=19,align="left",width=400,color=(90,90,250))

        #~~~~~~~~~~~~~~~~Difficulty Buttons Interface~~~~~~~~~~~~~~~~


        
        self.manager.draw()

        #Player Count inside button "Players: "
        arcade.draw_text(text=str(playerCount),start_x=290,start_y=470,font_size=16,color=(250,250,250))

        #Tips bottom right
        arcade.draw_text(text="PAUSE: Esc key",start_x=550,start_y=43,font_size=12)
        arcade.draw_text(text="MOVE: Arrow keys or WASD",start_x=550,start_y=24,font_size=12)
        arcade.draw_text(text="BOOST: SHIFT key",start_x=550,start_y=5,font_size=12)

        #on_draw also updates per frame.

        self.frameTrack=self.frameTrack+1

        if (self.frameTrack%20==0):
            if (self.frameIndex==1):
                self.frameIndex=0
            else:
                self.frameIndex=1



class gameOverMenu(arcade.View):
    def __init__(self,score1,score2):  #Gets scores as arguments. score default is 0.

        super().__init__()

        self.window.set_mouse_visible(True)

        self.score1=score1
        self.score2=score2
        
        self.scene = None
        

        self.background = arcade.load_texture("assets/space.png")
        self.brokenSpaceCraft = arcade.load_texture("assets/spacecraft_destroyed.png")

        ## Needed for the buttons
        self.manager = None
        
    
    def setup(self): 
        self.manager = arcade.gui.UIManager()
        self.manager.enable()


        self.firstColumn = arcade.gui.UIBoxLayout(vertical=True)
        self.secondColumn = arcade.gui.UIBoxLayout(vertical=True)


        #~~~~~~~~~~~~~~~~First Column~~~~~~~~~~~~~~~~

        retryButton = arcade.gui.UIFlatButton(text="Play Again", width=200)
        self.firstColumn.add(retryButton.with_space_around(bottom=100))

        mainMenuButton = arcade.gui.UIFlatButton(text="Homescreen", width=200)
        self.firstColumn.add(mainMenuButton.with_space_around(bottom=100))



        @retryButton.event("on_click") #Difficulty is globally set.
        def on_click_settings(event):
            gameView=mainGameView() 
            gameView.setup()
            self.window.show_view(gameView)

        @mainMenuButton.event("on_click")
        def on_click_settings(event):
            currentView=mainMenu()
            currentView.setup()
            self.window.show_view(currentView)

        #~~~~~~~~~~~~~~~~First Column~~~~~~~~~~~~~~~~




        #~~~~~~~~~~~~~~~~Second Column~~~~~~~~~~~~~~~~

    
        scoreButton = arcade.gui.UIFlatButton(text="Scoreboard", width=200)
        self.secondColumn.add(scoreButton.with_space_around(bottom=100))

        exitButton = arcade.gui.UIFlatButton(text="Exit", width=200)
        self.secondColumn.add(exitButton.with_space_around(bottom=100))



        @scoreButton.event("on_click")
        def on_click_settings(event): #Difficulty is globally set.
            currentView=scoreMenu()
            currentView.setup()
            self.window.show_view(currentView)
        
        @exitButton.event("on_click")
        def on_click_settings(event):
            arcade.exit()

        #~~~~~~~~~~~~~~~~Second Column~~~~~~~~~~~~~~~~


        # Create a widget to hold the first column
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                align_x= 150,
                align_y= 0,
                anchor_x="left",
                anchor_y="bottom",
                child=self.firstColumn),
        )

        # Create a widget to hold the second column
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                align_x= -150,
                align_y= 0,
                anchor_x="right",
                anchor_y="bottom",
                child=self.secondColumn),
        )
        
        
        
        pass


    def on_hide_view(self):
        self.manager.disable()


    def on_draw(self):

        self.clear()

        arcade.draw_lrwh_rectangle_textured(
            0, 0,
            SCREEN_WIDTH, 4000,
            self.background
        )


        arcade.draw_lrwh_rectangle_textured(0,20,800,800,self.brokenSpaceCraft)

        #Buttons above broken spacecraft
        self.manager.draw()

        
        
        arcade.draw_text(text="GAME OVER",start_x=50,start_y=700,font_size=64,align="center",width=700,color=(230, 0, 0))



        #~~~~~~~~~~~~~~~~Show Score~~~~~~~~~~~~~~~~
        

        if playerCount==1:
            arcade.draw_ellipse_filled(400,380,350,100,(0,0,0,200))
            arcade.draw_text(text="Your score was "+str(self.score1),start_x=50,start_y=370,font_size=24,align="center",width=700,color=(50,50,200),bold=True)
        else:
            arcade.draw_ellipse_filled(400,400,400,150,(0,0,0,200))
            arcade.draw_text(text="Player1 score was "+str(self.score1),start_x=50,start_y=400,font_size=24,align="center",width=700,color=(50,50,200),bold=True)
            arcade.draw_text(text="Player2 score was "+str(self.score2),start_x=50,start_y=370,font_size=24,align="center",width=700,color=(50,50,200),bold=True)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


        #~~~~~~~~~~~~~~~~Show Tips~~~~~~~~~~~~~~~~

        arcade.draw_text(text="PAUSE: Esc key",start_x=550,start_y=43,font_size=12)
        arcade.draw_text(text="MOVE: Arrow keys or WASD",start_x=550,start_y=24,font_size=12)
        arcade.draw_text(text="BOOST: SHIFT key",start_x=550,start_y=5,font_size=12)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


        


          
class creditsMenu(arcade.View):

    def __init__(self): 

        super().__init__()
        
        self.scene = None

        self.background = arcade.load_texture("assets/space.png")

        self.logo = arcade.load_texture("assets/logo.png")


        self.manager=None
        ## Needed for the buttons
        





    def setup(self): 

        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        


        self.v_box = arcade.gui.UIBoxLayout()

        #~~~~~~~~~~~~~~~~Home Button~~~~~~~~~~~~~~~~

        homeButton = arcade.gui.UIFlatButton(text="Go Back", width=200)
        self.v_box.add(homeButton.with_space_around(bottom=20))

        

        @homeButton.event("on_click")
        def on_click_settings(event):
            currentView=mainMenu()
            currentView.setup()
            self.window.show_view(currentView)

        #~~~~~~~~~~~~~~~~Home Button~~~~~~~~~~~~~~~~



        # Create a widget to hold the home button

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                align_y= -5,
                anchor_x="center_x",
                anchor_y="bottom",
                child=self.v_box),
        )
        
        pass


    def on_hide_view(self):
        self.manager.disable()


    def on_draw(self):

        self.clear()


        arcade.draw_lrwh_rectangle_textured(
            0, 0,
            SCREEN_WIDTH, 4000,
            self.background
        )


        arcade.draw_rectangle_filled(400,400,800,800,(0,0,50,150)) #Transparent rectangle for effect

        arcade.draw_lrwh_rectangle_textured(150,0,800,800,self.logo) #Logo


        #~~~~~~~~~~~~~~~~Credits Text~~~~~~~~~~~~~~~~

        arcade.draw_text(text="This game was built by Alexander Petrache and Nikolaos Filopoulos",start_x=50,start_y=550,font_size=16,align="center",width=700)
        arcade.draw_text(text="During their 2nd Semester at the Vocational Institute of Peristeri",start_x=50,start_y=520,font_size=16,align="center",width=700)
        arcade.draw_text(text="As a project on the course 'Practical Application' ",start_x=50,start_y=490,font_size=16,align="center",width=700)
        arcade.draw_text(text="We built this using the Python and the library 'Arcade'.",start_x=50,start_y=460,font_size=16,align="center",width=700)
        
        arcade.draw_text(text="Time: Spring 2023",start_x=50,start_y=430,font_size=16,align="center",width=700)
        arcade.draw_text(text="All assets were handmade by us",start_x=50,start_y=400,font_size=16,align="center",width=700)
        arcade.draw_text(text="So don't use them without our written permission.",start_x=50,start_y=370,font_size=16,align="center",width=700)


        arcade.draw_text(text="Feel free to reach out to us for any questions,",start_x=50,start_y=170,font_size=16,align="center",width=700)
        arcade.draw_text(text="Regarding this project",start_x=50,start_y=140,font_size=16,align="center",width=700)
        arcade.draw_text(text="At hello@deadlyunicorn.dev",start_x=50,start_y=110,font_size=16,align="center",width=700)
        arcade.draw_text(text="We hope you enjoy the game!",start_x=50,start_y=80,font_size=16,align="center",width=700)

        #~~~~~~~~~~~~~~~~Credits Text~~~~~~~~~~~~~~~~


        self.manager.draw()





class scoreMenu(arcade.View):

    def __init__(self): 

        super().__init__()
        

        self.scene = None

        self.currentDifficulty=difficulty
        self.background = arcade.load_texture("assets/space.png")

        
        self.entryFound=False
        self.registeredDifficulty=None

        self.manager=None


        self.registeredScore=None
        self.registeredDate=None

    class Score:
        def __init__(self,difficulty,score,date):
            self.difficulty=difficulty
            self.score=score
            self.date=date   

    def setup(self): 


        ## Needed for the buttons
        self.manager = arcade.gui.UIManager()
        self.manager.enable()


        self.v_box = arcade.gui.UIBoxLayout()

        #~~~~~~~~~~~~~~~~Home Button~~~~~~~~~~~~~~~~

        homeButton = arcade.gui.UIFlatButton(text="Go Back", width=200)
        self.v_box.add(homeButton.with_space_around(bottom=20))

        @homeButton.event("on_click")
        def on_click_settings(event):
            currentView=mainMenu()
            currentView.setup()
            self.window.show_view(currentView)

        #~~~~~~~~~~~~~~~~Home Button~~~~~~~~~~~~~~~~


        self.manager.add(
            arcade.gui.UIAnchorWidget(
                align_y= -5,
                anchor_x="center_x",
                anchor_y="bottom",
                child=self.v_box),
        )


        #~~~~~~~~~~~~~~~~Difficulty Buttons~~~~~~~~~~~~~~~~

        self.difficultyBox = arcade.gui.UIBoxLayout(vertical=False)
        
        easyButton = arcade.gui.UIFlatButton(text="Easy", width=200)
        self.difficultyBox.add(easyButton.with_space_around(right=20))

        mediumButton = arcade.gui.UIFlatButton(text="Medium", width=200)
        self.difficultyBox.add(mediumButton.with_space_around(right=20))

        hardButton = arcade.gui.UIFlatButton(text="Hard", width=200)
        self.difficultyBox.add(hardButton.with_space_around(right=20))


        #The default scoreboard difficulty is the global one.
        #We can change the local difficulty used for score show.
        #If we play again, we will use the global one.

        @easyButton.event("on_click")
        def on_click_settings(event):
            self.currentDifficulty=1

        @mediumButton.event("on_click")
        def on_click_settings(event):
            self.currentDifficulty=2

        @hardButton.event("on_click")
        def on_click_settings(event):
            self.currentDifficulty=3

        #~~~~~~~~~~~~~~~~Difficulty Buttons~~~~~~~~~~~~~~~~


        self.manager.add(
            arcade.gui.UIAnchorWidget(
                align_y= 120,
                anchor_x="center_x",
                anchor_y="bottom",
                child=self.difficultyBox),
        )

        
        #~~~~~~~~~Read scores from file~~~~~~~~~~~~~~

        with open("AstralEscapeScore.txt") as file:

            easy=[]
            normal=[]
            hard=[] 
  
            


            for line in file:

                if self.entryFound: #When found a score entry
                    
                    if line.find("Difficulty:")!=-1:
                        diffFinIndex=len("Difficulty:")
                        endLineIndex=line.find(";")

                        self.registeredDifficulty=line[diffFinIndex:endLineIndex].strip()


                    elif line.find("Score:")!=-1:
                        
                        scoreFinIndex=len("Score:")
                        endLineIndex=line.find(";")
                        
                        self.registeredScore=line[scoreFinIndex:endLineIndex]
                    
                    
                    elif line.find("Date:")!=-1:
                        
                        dateFinIndex=len("Date:")
                        endLineIndex=line.find(";")
                        
                        self.registeredDate=line[dateFinIndex:endLineIndex]


                    elif line.find("END")!=-1:
                        
                        
                    #Save unsorted scoreboard entries
                        if self.registeredDifficulty=="EASY":

                            ##Using int in order to work correctly during sort()..
                            easy.append(self.Score(self.registeredDifficulty,int(self.registeredScore),self.registeredDate))

                        elif self.registeredDifficulty=="NORMAL":

                            normal.append(self.Score(self.registeredDifficulty,int(self.registeredScore),self.registeredDate))

                        elif self.registeredDifficulty=="HARD":

                            hard.append(self.Score(self.registeredDifficulty,int(self.registeredScore),self.registeredDate))


                        self.entryFound=False
                        

                elif line.find("START"):
                        self.entryFound=True


            #After have finished reading all lines

            self.easy_sorted    =sorted(easy,   key=lambda x:x.score,reverse=True)
            self.normal_sorted  =sorted(normal, key=lambda x:x.score,reverse=True)
            self.hard_sorted    =sorted(hard,   key=lambda x:x.score,reverse=True)

            #Clear some memory ?
            easy=[]
            normal=[]
            hard=[] 
                
        # It would be good to delete scores that are below top 10.
                    
        pass

    def on_hide_view(self):
        self.manager.disable()



    def on_draw(self):

        self.clear()


        arcade.draw_lrwh_rectangle_textured(
            0, 0,
            SCREEN_WIDTH, 4000,
            self.background
        )

        arcade.draw_rectangle_filled(400,400,800,800,(0,0,50,150)) #Transparent rectangle

        #Buttons
        self.manager.draw()


        #Display the difficulty of the currently shown scores 
        arcade.draw_text(text="Showing difficulty: ",start_x=0,start_y=85,font_size=16,align="center",width=700)


        #~~~~~~~~~Show current difficulty~~~~~~~~~~~~~~

        if self.currentDifficulty==1:
            arcade.draw_text(text="Easy",start_x=450,start_y=85,font_size=16)
            
        elif self.currentDifficulty==2:
            arcade.draw_text(text="Medium",start_x=450,start_y=85,font_size=16)

        elif self.currentDifficulty==3:
            arcade.draw_text(text="Hard",start_x=450,start_y=85,font_size=16)

        #~~~~~~~~~Show current difficulty~~~~~~~~~~~~~~



        if self.registeredDifficulty!=None: #If no entries were found

            if self.currentDifficulty==1:
                


                #When entries on Easy were found
                if (len(self.easy_sorted)>0):

                    arcade.draw_text(text="RANK",start_x=70,start_y=710,font_size=32)
                    arcade.draw_text(text="SCORE",start_x=70+260,start_y=710,font_size=32)
                    arcade.draw_text(text="DATE",start_x=70+520,start_y=710,font_size=32)


                    for x in range(10): #Display top 10
                        if(x>=len(self.easy_sorted)):
                            break
                        
                        arcade.draw_rectangle_filled(400,660-x*50,700,40,(50,0,120,150)) #Transparent rectangle 

                        #Score Rank, Score, Date
                        arcade.draw_text(text="#"+str(x+1),start_x=100,start_y=650-x*50,font_size=19)
                        arcade.draw_text(text=str(self.easy_sorted[x].score),align="right",start_x=220,start_y=650-x*50,font_size=19,width=200)
                        arcade.draw_text(text=str(self.easy_sorted[x].date),start_x=570,start_y=650-x*50,font_size=19)
                        #Score Rank, Score, Date
                
                #When entries on Easy were NOT found
                else:
                    arcade.draw_text(text="No entries found",start_x=50,start_y=700,font_size=16,align="center",width=700)


            elif self.currentDifficulty==2:

                if (len(self.normal_sorted)>0):

                    arcade.draw_text(text="RANK",start_x=70,start_y=710,font_size=32)
                    arcade.draw_text(text="SCORE",start_x=70+260,start_y=710,font_size=32)
                    arcade.draw_text(text="DATE",start_x=70+520,start_y=710,font_size=32)

                    for x in range(10):

                        if(x>=len(self.normal_sorted)):
                            break
                        
                        arcade.draw_rectangle_filled(400,660-x*50,700,40,(50,0,120,150))

                        #Score Rank, Score, Date
                        arcade.draw_text(text="#"+str(x+1),start_x=100,start_y=650-x*50,font_size=19)
                        arcade.draw_text(text=str(self.normal_sorted[x].score),align="right",start_x=220,start_y=650-x*50,font_size=19,width=200)
                        arcade.draw_text(text=str(self.normal_sorted[x].date),start_x=570,start_y=650-x*50,font_size=19)
                        #Score Rank, Score, Date
                
                else:
                    arcade.draw_text(text="No entries found",start_x=50,start_y=700,font_size=16,align="center",width=700)




            elif self.currentDifficulty==3:

                if (len(self.hard_sorted)>0):

                    arcade.draw_text(text="RANK",start_x=70,start_y=710,font_size=32)
                    arcade.draw_text(text="SCORE",start_x=70+260,start_y=710,font_size=32)
                    arcade.draw_text(text="DATE",start_x=70+520,start_y=710,font_size=32)

                    for x in range(10):
                    
                        if(x>=len(self.hard_sorted)):
                            break
                        
                        arcade.draw_rectangle_filled(400,660-x*50,700,40,(50,0,120,150))
                        
                        #Score Rank, Score, Date
                        arcade.draw_text(text="#"+str(x+1),start_x=100,start_y=650-x*50,font_size=19)
                        arcade.draw_text(text=str(self.hard_sorted[x].score),align="right",start_x=220,start_y=650-x*50,font_size=19,width=200)
                        arcade.draw_text(text=str(self.hard_sorted[x].date),start_x=570,start_y=650-x*50,font_size=19)
                        #Score Rank, Score, Date

                else:
                    arcade.draw_text(text="No entries found",start_x=50,start_y=700,font_size=16,align="center",width=700)

        
        else:
            arcade.draw_text(text="No entries found",start_x=50,start_y=700,font_size=16,align="center",width=700)






def main():

    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    
    currentView=mainMenu()
    currentView.setup()

    window.show_view(currentView)

    arcade.run()

if __name__ == "__main__":
    main()
    