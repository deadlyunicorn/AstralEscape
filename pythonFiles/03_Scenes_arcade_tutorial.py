import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = "TEST 1"

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

        # self.player_list = None
        # self.meter_list = None

        self.scene = None
        


    def setup(self): 
        
        #Initialize scene

        self.scene = arcade.Scene()

        self.scene.add_sprite_list("Rocket")## create a new list "Rocket"
        self.scene.add_sprite_list("Meteors") 


        self.player_list = arcade.SpriteList()
        self.meteor_list = arcade.SpriteList(); 


        self.player_sprite = arcade.Sprite("/run/media/deadlyunicorn/F462-7117/Apps/Python_Final_Project/pythonFiles/assets/spacecraft.png",0.4) #file location , Sprite Scaling (1 = 100%)
        self.player_sprite.center_x=400
        self.player_sprite.center_y=400

        self.scene.add_sprite("Rocket",self.player_sprite) ## add to the Rocket list , self.player_sprite
        # self.player_list.append(self.player_sprite)


        self.meteorA_sprite = arcade.Sprite("/run/media/deadlyunicorn/F462-7117/Apps/Python_Final_Project/pythonFiles/assets/meteorite01.png",0.1)
        self.meteorA_sprite.center_x=SCREEN_WIDTH/2 # will need to add some randomness here
        self.meteorA_sprite.center_y=SCREEN_HEIGHT

        self.meteorB_sprite = arcade.Sprite("/run/media/deadlyunicorn/F462-7117/Apps/Python_Final_Project/pythonFiles/assets/meteorite02.png",0.1)
        self.meteorB_sprite.center_x=SCREEN_WIDTH/2+50
        self.meteorB_sprite.center_y=SCREEN_HEIGHT

        self.scene.add_sprite("Meteor A",self.meteorA_sprite)
        self.scene.add_sprite("Meteor B",self.meteorB_sprite)


        # self.meteor_list.append(self.meteorA_sprite)
        # self.meteor_list.append(self.meteorB_sprite)


        
        pass

    
    def on_draw(self):

        self.clear()
        self.shapes.draw()
        

        # self.meteor_list.draw()
        # self.player_list.draw()

        self.scene.draw()

def main():

    window = MyGame()

    window.setup()

    arcade.run()

if __name__ == "__main__":
    main()
    
    
    
