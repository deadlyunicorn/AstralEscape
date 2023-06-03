import arcade
import arcade.gui
import glob
import random
from datetime import date

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

difficulty=1


class mainGameView(arcade.View):

    def __init__(self): 

        super().__init__()

        arcade.set_background_color(arcade.csscolor.BLACK)


        self.shapes = arcade.ShapeElementList()
        self.window.set_mouse_visible(False)

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
        
        self.background = None
        self.backgroundMove=0

        self.animationBoost = 10


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

        self.background=arcade.load_texture("assets/space.png")

        self.heartTexture=arcade.load_texture("assets/heart.png")


        
        pass

    
    def on_draw(self):

        self.clear()
        self.shapes.draw()
        arcade.draw_lrwh_rectangle_textured(0, -self.backgroundMove,
                                            SCREEN_WIDTH, 4000,
                                            self.background)

        frame=frames[self.frameIndex]
        frame.draw_sized(self.player_sprite.center_x, self.player_sprite.center_y, frame.width*0.1, frame.height*0.1)

        arcade.draw_text(("Score is: "+str(self.score)),0,750,font_size=14,align="center",width=800)


        arcade.draw_lrwh_rectangle_textured(800-69,748,20,18,self.heartTexture)
        arcade.draw_text(("x"+str(self.PlayerHP)),-20,750,font_size=14,align="right",width=800,font_name="calibri")

        


        self.scene.draw()

        #background
        

        

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

        if(self.backgroundMove<3200-20): ##For a smoother change
            if(self.coinBoost):
                self.backgroundMove+=12
            else:
                self.backgroundMove+=1
        else:
            self.backgroundMove=0

        

        for meteor_engine in self.meteor_engines:
            meteor_engine.update()





        for coin in self.scene["Coins"]:
          coin.change_y = -PlayerSpeed *2


        for meteor in self.scene["Meteors"]:
           
            if(self.coinBoost):meteor.change_y = -PlayerSpeed * 5
            else:meteor.change_y = -PlayerSpeed * 2
        # for coin in self.scene["Coins"]:
        #     coin.change_y = -PlayerSpeed

        

        meteorDamage = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["Meteors"]
        )

        for meteor in meteorDamage:
            meteor.remove_from_sprite_lists()
            self.PlayerHP = self.PlayerHP - 1


        coinCatch = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["Coins"]
        )

        for coin in coinCatch:
            coin.remove_from_sprite_lists()

            
            
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
            scoreFile=open("AstralEscapeScore.txt","a")

            scoreFile.write("\nSTART----------\n\n")
            scoreFile.write("Difficulty: ")
            if difficulty==1:
                scoreFile.write("EASY;\n")
            elif difficulty==2:
              scoreFile.write("NORMAL;\n")
            elif difficulty==3:
              scoreFile.write("HARD;\n")
                
            scoreFile.write("Score: "+str(self.score)+";\n")
            scoreFile.write("Date: "+str(date.today())+";\n")
            scoreFile.write("\nEND------------\n")

            mainMenuView = mainMenu()
            mainMenuView.setup()
            self.window.show_view(mainMenuView)



        self.frameTrack=self.frameTrack+1

        if (self.coinBoost):
            self.animationBoost=5
        else:
            self.animationBoost=10


        if (self.frameTrack%self.animationBoost==0):
            if (self.frameIndex==1):
                self.frameIndex=0
            else:
                self.frameIndex=1


        seconds=int(self.frameTrack/60)

        if (self.coinBoost and self.frameTrack%6==0):
            self.score=self.score+1
        elif(self.frameTrack%30==0):
            self.score=self.score+1

        if self.coinBoost == False:
            self.coinSec = seconds
        
        if(self.timeTrack!=seconds):

            if (self.timeTrack==self.coinSec+2):
                self.coinBoost = False

                

            

            self.timeTrack=seconds
            if (self.timeTrack%5==0):
                randomNumber=random.randrange(10,790)

                coinScale=random.randrange(100,110)/1000
                if (difficulty==3):
                    coinScale=random.randrange(60,110)/1000

                coin=arcade.Sprite("assets/coin.png",0.1)
                coin.center_x=randomNumber # will need to add some randomness here
                coin.center_y=SCREEN_HEIGHT
                coin.change_angle=random.randrange(-2,2)
                coin.scale=coinScale
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
                    randomScale=random.randrange(100,110)/1000

                    meteorSpawnNum = random.randrange(3)

                    if(meteorSpawnNum==1):
                        meteor=arcade.Sprite("assets/meteorite01.png",0.1)
                        meteor.center_x=randomNumber+random.randrange(-200,200) # will need to add some randomness here
                        meteor.center_y=SCREEN_HEIGHT+random.randrange(20,500)
                        meteor.change_angle=randomRadial
                        meteor.scale=randomScale
                        self.scene.add_sprite("Meteors",meteor)
                    elif(meteorSpawnNum==2):
                        meteor2=arcade.Sprite("assets/meteorite02.png",0.1)
                        meteor2.center_x=randomNumber+random.randrange(-200,200) # will need to add some randomness here
                        meteor2.center_y=SCREEN_HEIGHT+random.randrange(20,500)
                        meteor2.change_angle=randomRadial
                        meteor2.scale=randomScale


                        self.scene.add_sprite("Meteors",meteor2)
                    else:
                        meteor=arcade.Sprite("assets/meteorite01.png",0.1)
                        meteor.center_x=randomNumber+random.randrange(-200,200) # will need to add some randomness here
                        meteor.center_y=SCREEN_HEIGHT+random.randrange(20,500)
                        meteor.change_angle=randomRadial
                        meteor.scale=randomScale


                        self.scene.add_sprite("Meteors",meteor)

                        meteor2=arcade.Sprite("assets/meteorite02.png",0.1)
                        meteor2.center_x=randomNumber+random.randrange(-200,200) # will need to add some randomness here
                        meteor2.center_y=SCREEN_HEIGHT+random.randrange(20,500)
                        meteor2.change_angle=randomRadial
                        meteor2.scale=randomScale


                        self.scene.add_sprite("Meteors",meteor2)

                #if difficulty hard
                if (difficulty==3):
                    meteorSpawn()
                    meteorSpawn()
                    meteorSpawn()
                    meteorSpawn()
                    meteorSpawn()
                    meteorSpawn()
                elif difficulty==2:
                    meteorSpawn()
                    meteorSpawn()
                    meteorSpawn()
                elif difficulty==1:
                    meteorSpawn()
                
                

                

                
                

                
                for meteor in self.scene["Meteors"]:
                    if meteor not in self.existingMeteorList:
                        meteor_engine = arcade.PhysicsEngineSimple(
                            meteor, None
                        )
                        self.meteor_engines.append(meteor_engine)
                        self.existingMeteorList.append(meteor)

                
            


class mainMenu(arcade.View):



    def __init__(self): 



        super().__init__()

        self.window.set_mouse_visible(True)
        

        self.scene = None
        
        self.background = arcade.load_texture("assets/space.png")
        self.frameTrack=0
        self.frameIndex=0

        self.logo = arcade.load_texture("assets/logo.png")

        ## Needed for the buttons
        self.manager = arcade.gui.UIManager()
        self.manager.enable()


        self.difficultyBox = arcade.gui.UIBoxLayout(vertical=False)

        easyButton = arcade.gui.UIFlatButton(text="Easy", width=100)
        self.difficultyBox.add(easyButton.with_space_around(right=20))
        mediumButton = arcade.gui.UIFlatButton(text="Medium", width=100)
        self.difficultyBox.add(mediumButton.with_space_around(right=20))
        hardButton = arcade.gui.UIFlatButton(text="Hard", width=100)
        self.difficultyBox.add(hardButton.with_space_around(right=20))





        self.v_box = arcade.gui.UIBoxLayout()


        playButton = arcade.gui.UIFlatButton(text="Start Game", width=200)
        self.v_box.add(playButton.with_space_around(bottom=20))

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


        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                align_x= 150,
                align_y= 0,
                anchor_x="left",
                anchor_y="center_y",
                child=self.v_box),
        )

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                align_x= 70,
                align_y= 50,
                anchor_x="left",
                anchor_y="bottom",
                child=self.difficultyBox),
        )





    
    def setup(self): 
        
        
        
        pass

    
    def on_draw(self):



        self.clear()

        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, 4000,
                                            self.background)


        frame=frames[self.frameIndex]
        frame.draw_sized(600, 350, frame.width*0.8, frame.height*0.8)

        arcade.draw_lrwh_rectangle_textured(0,0,800,800,self.logo)

        arcade.draw_text(text="Difficulty",start_x=180,start_y=140,font_size=24,align="left",width=400)

        if difficulty==1:
            arcade.draw_text(text="l",start_x=120,start_y=108,font_size=24,align="left",width=400,color=(90,90,250))
            arcade.draw_text(text="v",start_x=118,start_y=106,font_size=19,align="left",width=400,color=(90,90,250))
        elif difficulty==2:
            arcade.draw_text(text="l",start_x=240,start_y=108,font_size=24,align="left",width=400,color=(90,90,250))
            arcade.draw_text(text="v",start_x=238,start_y=106,font_size=19,align="left",width=400,color=(90,90,250))

        elif difficulty==3:
            arcade.draw_text(text="l",start_x=360,start_y=108,font_size=24,align="left",width=400,color=(90,90,250))
            arcade.draw_text(text="v",start_x=358,start_y=106,font_size=19,align="left",width=400,color=(90,90,250))

        ## Button

        self.manager.draw()
        


        
    # def on_mouse_press(self, _x, _y, _button, _modifiers):
    #     gameView=mainGameView()
    #     gameView.setup()
    #     self.window.show_view(gameView)





    def on_update(self,delta_time):


        self.frameTrack=self.frameTrack+1

        if (self.frameTrack%20==0):
            if (self.frameIndex==1):
                self.frameIndex=0
            else:
                self.frameIndex=1




          
class creditsMenu(arcade.View):

    def __init__(self): 

        super().__init__()
        

        self.scene = None
        
        self.background = arcade.load_texture("assets/space.png")

        self.logo = arcade.load_texture("assets/logo.png")

        ## Needed for the buttons
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        


        self.v_box = arcade.gui.UIBoxLayout()


        homeButton = arcade.gui.UIFlatButton(text="Go Back", width=200)
        self.v_box.add(homeButton.with_space_around(bottom=20))

        

        @homeButton.event("on_click")
        def on_click_settings(event):
            currentView=mainMenu()
            currentView.setup()
            self.window.show_view(currentView)


        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                align_y= -5,
                anchor_x="center_x",
                anchor_y="bottom",
                child=self.v_box),
        )





    def setup(self): 
        
        pass

    
    def on_draw(self):



        self.clear()


        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, 4000,
                                            self.background)


        arcade.draw_rectangle_filled(400,400,800,800,(0,0,50,150))


        arcade.draw_lrwh_rectangle_textured(150,0,800,800,self.logo)



        arcade.draw_text(text="This game was built by Alexander Petrache and Nikolaos Filopoulos",start_x=50,start_y=550,font_size=16,align="center",width=700)
        arcade.draw_text(text="During their 2nd Semester at the Vocational Institute of Peristeri",start_x=50,start_y=520,font_size=16,align="center",width=700)
        arcade.draw_text(text="As a project on the course 'Practical Application' ",start_x=50,start_y=490,font_size=16,align="center",width=700)
        arcade.draw_text(text="We built this using the Python and the library 'Arcade'.",start_x=50,start_y=460,font_size=16,align="center",width=700)
        
        arcade.draw_text(text="Time: Spring 2023",start_x=50,start_y=430,font_size=16,align="center",width=700)
        arcade.draw_text(text="All assets were handmade by us",start_x=50,start_y=400,font_size=16,align="center",width=700)
        arcade.draw_text(text="So don't use them without our written permission.",start_x=50,start_y=370,font_size=16,align="center",width=700)


        arcade.draw_text(text="Feel free to reach out to us for any questions,",start_x=50,start_y=170,font_size=16,align="center",width=700)
        arcade.draw_text(text="Regarding this project.",start_x=50,start_y=140,font_size=16,align="center",width=700)
        arcade.draw_text(text="We hope you enjoy the game!",start_x=50,start_y=110,font_size=16,align="center",width=700)

        ## Button

        self.manager.draw()





class scoreMenu(arcade.View):

    def __init__(self): 

        super().__init__()
        

        self.scene = None

        self.currentDifficulty=1
        self.background = arcade.load_texture("assets/space.png")

        
        self.entryFound=False
        self.registeredDifficulty=None

        

    def setup(self): 


        ## Needed for the buttons
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.v_box = arcade.gui.UIBoxLayout()

        homeButton = arcade.gui.UIFlatButton(text="Go Back", width=200)
        self.v_box.add(homeButton.with_space_around(bottom=20))

        @homeButton.event("on_click")
        def on_click_settings(event):
            currentView=mainMenu()
            currentView.setup()
            self.window.show_view(currentView)

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                align_y= -5,
                anchor_x="center_x",
                anchor_y="bottom",
                child=self.v_box),
        )

        self.difficultyBox = arcade.gui.UIBoxLayout(vertical=False)
        
        easyButton = arcade.gui.UIFlatButton(text="Easy", width=200)
        self.difficultyBox.add(easyButton.with_space_around(right=20))

        @easyButton.event("on_click")
        def on_click_settings(event):
            self.currentDifficulty=1

        mediumButton = arcade.gui.UIFlatButton(text="Medium", width=200)
        self.difficultyBox.add(mediumButton.with_space_around(right=20))

        @mediumButton.event("on_click")
        def on_click_settings(event):
            self.currentDifficulty=2

        hardButton = arcade.gui.UIFlatButton(text="Hard", width=200)
        self.difficultyBox.add(hardButton.with_space_around(right=20))

        @hardButton.event("on_click")
        def on_click_settings(event):
            self.currentDifficulty=3

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                align_y= 120,
                anchor_x="center_x",
                anchor_y="bottom",
                child=self.difficultyBox),
        )

        


        with open("AstralEscapeScore.txt") as file:

            easy=[]
            normal=[]
            hard=[] 
  
            self.registeredScore=None
            self.registeredDate=None


            for line in file:

                if self.entryFound:
                    if line.find("Difficulty:")!=-1:
                        diffFinIndex=len("Difficulty:")
                        endLineIndex=line.find(";")
                        self.registeredDifficulty=line[diffFinIndex:endLineIndex]
                    elif line.find("Score:")!=-1:
                        scoreFinIndex=len("Score:")
                        endLineIndex=line.find(";")
                        self.registeredScore=line[scoreFinIndex:endLineIndex]
                    elif line.find("Date:")!=-1:
                        dateFinIndex=len("Date:")
                        endLineIndex=line.find(";")
                        self.registeredDate=line[dateFinIndex:endLineIndex]
                    elif line.find("END")!=-1:
                        
                        self.entryFound=False
                        
                        if self.registeredDifficulty.strip()=="EASY":
                            easy.append(Score(self.registeredDifficulty,int(self.registeredScore),self.registeredDate))
                        elif self.registeredDifficulty.strip()=="NORMAL":
                            normal.append(Score(self.registeredDifficulty,int(self.registeredScore),self.registeredDate))
                        elif self.registeredDifficulty.strip()=="HARD":
                            hard.append(Score(self.registeredDifficulty,int(self.registeredScore),self.registeredDate))
                            ##Using int in order to work during sort()
                            

                elif line.find("START"):
                        self.entryFound=True


            self.easy_sorted=sorted(easy,key=lambda x:x.score,reverse=True)
            self.normal_sorted=sorted(normal,key=lambda x:x.score,reverse=True)
            self.hard_sorted=sorted(hard,key=lambda x:x.score,reverse=True)
                
                
                    
   
        
        pass

    
    def on_draw(self):


        self.clear()


        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, 4000,
                                            self.background)


        arcade.draw_rectangle_filled(400,400,800,800,(0,0,50,150))




        arcade.draw_text(text="Showing difficulty: ",start_x=0,start_y=85,font_size=16,align="center",width=700)
        ## Button

        self.manager.draw()

        if self.currentDifficulty==1:
            arcade.draw_text(text="Easy",start_x=450,start_y=85,font_size=16)

            
        elif self.currentDifficulty==2:
            arcade.draw_text(text="Medium",start_x=450,start_y=85,font_size=16)
        elif self.currentDifficulty==3:
            arcade.draw_text(text="Hard",start_x=450,start_y=85,font_size=16)

        if self.registeredDifficulty!=None:

            if self.currentDifficulty==1:
                
                if (len(self.easy_sorted)>0):
                    arcade.draw_text(text="RANK",start_x=70,start_y=710,font_size=32)
                    arcade.draw_text(text="SCORE",start_x=70+260,start_y=710,font_size=32)
                    arcade.draw_text(text="DATE",start_x=70+520,start_y=710,font_size=32)

                    for x in range(10):
                        if(x>=len(self.easy_sorted)):
                            break
                        
                        arcade.draw_rectangle_filled(400,660-x*50,700,40,(50,0,120,150))
                        arcade.draw_text(text="#"+str(x+1),start_x=100,start_y=650-x*50,font_size=19)
                        arcade.draw_text(text=str(self.easy_sorted[x].score),align="right",start_x=220,start_y=650-x*50,font_size=19,width=200)
                        arcade.draw_text(text=str(self.easy_sorted[x].date),start_x=570,start_y=650-x*50,font_size=19)
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
                        arcade.draw_text(text="#"+str(x+1),start_x=100,start_y=650-x*50,font_size=19)
                        arcade.draw_text(text=str(self.normal_sorted[x].score),align="right",start_x=220,start_y=650-x*50,font_size=19,width=200)
                        arcade.draw_text(text=str(self.normal_sorted[x].date),start_x=570,start_y=650-x*50,font_size=19)
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
                        arcade.draw_text(text="#"+str(x+1),start_x=100,start_y=650-x*50,font_size=19)
                        arcade.draw_text(text=str(self.hard_sorted[x].score),align="right",start_x=220,start_y=650-x*50,font_size=19,width=200)
                        arcade.draw_text(text=str(self.hard_sorted[x].date),start_x=570,start_y=650-x*50,font_size=19)
                else:
                    arcade.draw_text(text="No entries found",start_x=50,start_y=700,font_size=16,align="center",width=700)

        
        else:
            arcade.draw_text(text="No entries found",start_x=50,start_y=700,font_size=16,align="center",width=700)



        

class Score:
    def __init__(self,difficulty,score,date):
        self.difficulty=difficulty
        self.score=score
        self.date=date



def main():



    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    
    startingView=mainMenu()
    # gameView=mainGameView()

    window.show_view(mainMenu())
    startingView.setup()

    arcade.run()

if __name__ == "__main__":
    main()
    
    
    
