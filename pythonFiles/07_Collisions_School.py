import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = "TEST 1"
wallHeight = (SCREEN_HEIGHT/2)+200

PlayerSpeed = 3

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

        self.PlayerHP = 5

        self.score = 0
        

        


    def setup(self): 
        

        self.scene = arcade.Scene()

        self.scene.add_sprite_list("Rocket")
        self.scene.add_sprite_list("Walls")
        self.scene.add_sprite_list("OuterWalls")

        self.scene.add_sprite_list("Coins")
        self.scene.add_sprite_list("Meteors")


        self.player_list = arcade.SpriteList()
        self.meteor_list = arcade.SpriteList(); 


        self.player_sprite = arcade.Sprite("/media/student/F462-7117/Apps/Python_Final_Project/pythonFiles/assets/spacecraft.png",0.4) #file location , Sprite Scaling (1 = 100%)
        self.player_sprite.center_x=400
        self.player_sprite.center_y=400

        self.scene.add_sprite("Rocket",self.player_sprite)


        # Adding walls
        for chunk in range(0,SCREEN_WIDTH+10,10): #wall is 50x50 1/5 = 0.2 
            wall =  arcade.Sprite("/media/student/F462-7117/Apps/Python_Final_Project/assets/test_invisible_wall.png",0.2) #file location , Sprite Scaling (1 = 100%)
            wall.center_x=chunk
            wall.center_y=0
            self.scene.add_sprite("OuterWalls",wall)

        for chunk in range(0,SCREEN_WIDTH+10,10): #wall is 50x50 1/5 = 0.2 
            wall =  arcade.Sprite("/media/student/F462-7117/Apps/Python_Final_Project/assets/test_invisible_wall.png",0.2) #file location , Sprite Scaling (1 = 100%)
            wall.center_x=chunk
            wall.center_y=wallHeight
            self.scene.add_sprite("Walls",wall)

        for chunk in range(0,SCREEN_WIDTH+10,10): #wall is 50x50 1/5 = 0.2 
            wall =  arcade.Sprite("/media/student/F462-7117/Apps/Python_Final_Project/assets/test_invisible_wall.png",0.2) #file location , Sprite Scaling (1 = 100%)
            wall.center_x=chunk
            wall.center_y=20
            self.scene.add_sprite("Walls",wall)

        for chunk in range(0,int(wallHeight),10): #wall is 50x50 1/5 = 0.2 
            wall =  arcade.Sprite("/media/student/F462-7117/Apps/Python_Final_Project/assets/test_invisible_wall.png",0.2) #file location , Sprite Scaling (1 = 100%)
            wall.center_x=20
            wall.center_y=chunk
            self.scene.add_sprite("Walls",wall)
          
        for chunk in range(0,int(wallHeight),10): #wall is 50x50 1/5 = 0.2 
            wall =  arcade.Sprite("/media/student/F462-7117/Apps/Python_Final_Project/assets/test_invisible_wall.png",0.2) #file location , Sprite Scaling (1 = 100%)
            wall.center_x=SCREEN_WIDTH-20
            wall.center_y=chunk
            self.scene.add_sprite("Walls",wall)

        self.coin_sprite = arcade.Sprite("/media/student/F462-7117/Apps/Python_Final_Project/assets/coin.png",0.1)
        self.coin_sprite.center_x=400
        self.coin_sprite.center_y=700

        self.scene.add_sprite("Coins",self.coin_sprite)


        self.meteorA_sprite = arcade.Sprite("/media/student/F462-7117/Apps/Python_Final_Project/assets/meteorite01.png",0.1)
        self.meteorA_sprite.center_x=SCREEN_WIDTH/2 # will need to add some randomness here
        self.meteorA_sprite.center_y=SCREEN_HEIGHT

        self.meteorB_sprite = arcade.Sprite("/media/student/F462-7117/Apps/Python_Final_Project/assets/meteorite02.png",0.1)
        self.meteorB_sprite.center_x=SCREEN_WIDTH/2+50
        self.meteorB_sprite.center_y=SCREEN_HEIGHT

        self.scene.add_sprite("Meteors",self.meteorA_sprite)
        self.scene.add_sprite("Meteors",self.meteorB_sprite)

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

        for meteor in self.scene["Meteors"]:
          meteor_engine = arcade.PhysicsEngineSimple(
              meteor, None
          )
          self.meteor_engines.append(meteor_engine)



        
        pass

    
    def on_draw(self):

        self.clear()
        self.shapes.draw()
        


        self.scene.draw()
        

    def updatePlayerSpeed(self):
        
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = PlayerSpeed
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -PlayerSpeed


        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PlayerSpeed 
        elif self.right_pressed and not self.left_pressed:
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
            meteor.change_y = -PlayerSpeed * 2
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

        if self.PlayerHP==3:
          arcade.get_window().close()#make it to go to game over screen when ==0




        

        
           
            
        # print (self.score)
            


    

          

def main():

    window = MyGame()

    window.setup()

    arcade.run()

if __name__ == "__main__":
    main()
    
    
    
