from tkinter import Tk, Canvas, PhotoImage, Button

def configure_game():
	window.geometry("640x640")
	window.title("C H E S S")
	window.configure(bg="white")


def create_buttons():
	#Define the background canvas and list of buttons
	global board_buttons, game_canvas
	board_buttons=[None]*64 
	game_canvas = Canvas(window, height = "640", width = "640", bg = "orange")
	game_canvas.pack()

	#Place buttons on the canvas
	x_coord, y_coord = 40, 40
	for y in range(8):
		for x in range(8):
			if(y%2==0 and x%2==0):
				temporary_image = white_square
			elif(y%2!=0 and x%2!=0):
				temporary_image = white_square
			else:
				temporary_image = black_square
			temporary_button=Button(window, image = temporary_image, height = "80", width = "80", bg = "black")
			board_buttons[x]=game_canvas.create_window(x_coord, y_coord, window = temporary_button)
			window.update()
			x_coord = x_coord + 80
		x_coord = 40
		y_coord = y_coord + 80


def mainloop():
	create_buttons()

window = Tk()
white_square = PhotoImage(file = "white_square.png")
black_square = PhotoImage(file = "black_square.png")
configure_game()

mainloop()

window.mainloop()