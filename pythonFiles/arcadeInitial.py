import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = "TEST 1"

class MyGame(arcade.Window): ##define Class MyGame as a subclass of arcade window

    def __init__(self):

        #Δημιουργία παραθύρου
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        #Χρώμα παρασκηνίου παραθύρου
        arcade.set_background_color(arcade.csscolor.BLACK)

    


    #RESTART 
    def setup(self):
        pass

    
    #Μάλλον κάνει render το παιχνίδι
    def on_draw(self):
        self.clear()


def main():

    window = MyGame()

    window.setup()

    arcade.run()

if __name__ == "__main__":
    main()
    
    
    
