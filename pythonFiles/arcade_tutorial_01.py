import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = "TEST 1"

##setup() -> will restart the process or take us to a next level
##resetting with __init__ will reset the current level/retry

class MyGame(arcade.Window):

    def __init__(self):

        #Δημιουργία παραθύρου
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        #Χρώμα παρασκηνίου παραθύρου
        arcade.set_background_color(arcade.csscolor.BLACK)


        #Δημιουργία λίστα με σχήματα
        self.shapes = arcade.ShapeElementList()

        #Χρώματα για χρήση στα σχήματα
        color1 = (188, 155, 189)
        color2 = (165, 205, 212)

        #Ακραία σημεία παραθύρου
        points = (0, 0), (SCREEN_WIDTH, 0), (SCREEN_WIDTH, SCREEN_HEIGHT), (0, SCREEN_HEIGHT)

        #Χρώματα στα παραπάνω ακραία σημεία
        colors = (color1, color2, color2, color2)

        #Δημιουργία του ορθογωνίου που θα καλύψει όλο το παράθυρο
        rect = arcade.create_rectangle_filled_with_colors(points, colors)

        #Εισαγωγή του ορθογωνίου στην λίστα
        self.shapes.append(rect)

    #RESTART 
    def setup(self):
        pass

    
    #Μάλλον κάνει render το παιχνίδι
    def on_draw(self):
        self.clear()

        #Εμφάνιση όλων των σχημάτων της λίστας
        self.shapes.draw()


def main():

    window = MyGame()

    window.setup()

    arcade.run()

if __name__ == "__main__":
    main()
    
    
    
