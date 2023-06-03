import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = "TEST 1"

PlayerSpeed = 5 

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
        self.meteor_physics_engine = None

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        


    def setup(self): 
        

        self.scene = arcade.Scene()

        self.scene.add_sprite_list("Rocket")
        self.scene.add_sprite_list("Coins")
        self.scene.add_sprite_list("Meteors")


        self.player_sprite = arcade.Sprite("/run/media/deadlyunicorn/F462-7117/Apps/Python_Final_Project/pythonFiles/assets/spacecraft.png",0.4) #file location , Sprite Scaling (1 = 100%)
        self.player_sprite.center_x=400
        self.player_sprite.center_y=400

        self.scene.add_sprite("Rocket",self.player_sprite)

        self.coin_sprite = arcade.Sprite("/run/media/deadlyunicorn/F462-7117/Apps/Python_Final_Project/pythonFiles/assets/coin.png",0.1)
        self.coin_sprite.center_x=400
        self.coin_sprite.center_y=700

        self.scene.add_sprite("Coins",self.coin_sprite)


        self.meteorA_sprite = arcade.Sprite("/run/media/deadlyunicorn/F462-7117/Apps/Python_Final_Project/pythonFiles/assets/meteorite01.png",0.1)
        self.meteorA_sprite.center_x=SCREEN_WIDTH/2 # will need to add some randomness here
        self.meteorA_sprite.center_y=SCREEN_HEIGHT

        self.meteorB_sprite = arcade.Sprite("/run/media/deadlyunicorn/F462-7117/Apps/Python_Final_Project/pythonFiles/assets/meteorite02.png",0.1)
        self.meteorB_sprite.center_x=SCREEN_WIDTH/2+50
        self.meteorB_sprite.center_y=SCREEN_HEIGHT

        self.scene.add_sprite("Meteors",self.meteorA_sprite)
        self.scene.add_sprite("Meteors",self.meteorB_sprite)

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.scene.get_sprite_list("Meteors")
        )

        self.meteor_physics_engine = arcade.PhysicsEngineSimple(
            self.scene["Meteors"], self.player_sprite
        )

        for meteor_sprite in self.scene["Meteors"]:
          meteor_sprite.change_y = -PlayerSpeed 


     



        
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

        #handle vertical and horizontal motion differently
        # don't use only elif

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

        for meteor_sprite in self.scene["Meteors"]:
          meteor_sprite.change_y = -PlayerSpeed 
        
        self.meteor_physics_engine.update()

    

          

def main():

    window = MyGame()

    window.setup()

    arcade.run()

if __name__ == "__main__":
    main()
    
    
    
