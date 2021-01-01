from tkinter import Tk, Canvas, PhotoImage, Button


def configure_game():
	window.geometry("640x640")
	window.title("C H E S S")
	window.configure(bg="white")


class Team:

	def __init__(self, team_list, x_coord, y_coord, color, count, lives):
		self.list = team_list
		self.x_coord = x_coord
		self.y_coord = y_coord
		self.color = color
		self.count = count
		self.lives = lives


def check_square_color(y, x):
	if(y%2==0 and x%2==0):
		temporary_image = "white"
	elif(y%2!=0 and x%2!=0):
		temporary_image = "white"
	else:
		temporary_image = "black"

	return temporary_image


def move_player(old_x, old_y, new_y, new_x):
	global possible_moves
	for x in range(len(possible_moves)):
		game_canvas.delete(possible_moves[x])
	window.update()
	possible_moves = []


def pawn_pressed_1(team, other_team, y, x, direction, z):

	global free_move
	new_y_coord = y

	#Checking if it is the first move
	if(team.count == 0):
		times = 2
	else:
		times = 1

	#Looking at all possible moves for the pawn
	for i in range(times):
		new_y_coord = new_y_coord + direction

		for j in range(16):

			if(new_y_coord==team.y_coord[z] and x==team.x_coord[z]):
				print("Space taken at ", x, new_y_coord)
				free_move = False
			elif(new_y_coord==other_team.y_coord[z] and x==other_team.x_coord[z]):
				print("Can attack at ", x, new_y_coord)
				free_move = False

		if not free_move:
			return None
		else:
			#If the space is free
			if(check_square_color(new_y_coord, x) == "black"):
				temporary_image = green_b
			else:
				temporary_image = green_w
			print("Free space at ", x, new_y_coord)
			temporary_button = Button(window, image=temporary_image, command=lambda:move_player(y, x, new_y_coord, x))
			possible_moves.append(game_canvas.create_window(40+x*80,40+new_y_coord*80, window = temporary_button))
			window.update()


def pawn_pressed(y, x):

	#Clearing current possible moves squares for new options when clicked
	global possible_moves
	if(len(possible_moves) != 0):
		for i in range(len(possible_moves)):
			game_canvas.delete(possible_moves[i])
		window.update()
		possible_moves = []	

	#Variables that show if the pawn has any free moves
	global free_move
	free_move = True

	#Looking if the selected pawn is white or black
	for z in range(16):
		if(y==black_team.y_coord[z] and x==black_team.x_coord[z]):
			pawn_pressed_1(black_team, white_team, y, x, 1, z)

		if(y==white_team.y_coord[z] and x==white_team.x_coord[z]):
			pawn_pressed_1(white_team, black_team, y, x, -1, z)

		#If there are no free moves, then quit searching for more moves
		if not free_move:
			break


def rook_pressed():
	print("Rook pressed")


def knight_pressed():
	print("Knight pressed")


def bishop_pressed():
	print("Bishop pressed")


def queen_pressed():
	print("Queen pressed")


def king_pressed():
	print("King pressed")


def create_buttons():
	#Define the background canvas and list of buttons
	global board_buttons, game_canvas, board_numbers
	board_numbers = [[0 for x in range(8)] for y in range(8)] 

	temporary_count = 0
	for y in range(8):
		for x in range(8):
			board_numbers[y][x] = temporary_count
			temporary_count += 1

	board_buttons = [None]*64 
	game_canvas = Canvas(window, height = "640", width = "640", bg = "orange")
	game_canvas.pack()

	#Place buttons on the canvas
	x_coord, y_coord = 0, 0
	for y in range(8):
		for x in range(8):

			if(check_square_color(y, x) == "white"):
				temporary_image = white_square
			else:
				temporary_image = black_square

			board_buttons[x]=game_canvas.create_image(x_coord, y_coord, image = temporary_image, anchor = "nw")
			window.update()
			x_coord = x_coord + 80
		x_coord = 0
		y_coord = y_coord + 80


def create_team(team):
	for x in range(8):
		team.list[x] = "private"
		team.x_coord[x] = x
		if(team.color == "black"):
			team.y_coord[x] = 1
		else:
			team.y_coord[x] = 6

	for x in range(8, 10):
		team.list[x] = "tower"
		if(team.color == "black"):
			team.y_coord[x] = 0
		else:
			team.y_coord[x] = 7
	team.x_coord[8] = 0
	team.x_coord[9] = 7


	for x in range(10, 12):
		team.list[x] = "horse"
		if(team.color == "black"):
			team.y_coord[x] = 0
		else:
			team.y_coord[x] = 7
	team.x_coord[10] = 1
	team.x_coord[11] = 6


	for x in range(12, 14):
		team.list[x] = "bishop"
		if(team.color == "black"):
			team.y_coord[x] = 0
		else:
			team.y_coord[x] = 7
	team.x_coord[12] = 2
	team.x_coord[13] = 5


	team.list[14] = "queen"
	if(team.color == "black"):
		team.y_coord[14] = 0
	else:
		team.y_coord[14] = 7
	team.x_coord[14] = 3


	team.list[15] = "king"
	if(team.color == "black"):
		team.y_coord[15] = 0
	else:
		team.y_coord[15] = 7
	team.x_coord[15] = 4


def display_character(y, x, image_1, image_2, character_type):

	#Converting coordinates into pixels in the canvas
	temporary_x_coord = 40 + x*80
	temporary_y_coord = 40 + y*80

	#Check wether the background is white or black
	if(check_square_color(y, x) == "white"):
		temporary_image = image_1
	else:
		temporary_image = image_2

	#Checking which character button should be created
	if(character_type == "private"):
		temporary_command = pawn_pressed
	elif(character_type == "horse"):
		temporary_command = knight_pressed
	elif(character_type == "tower"):
		temporary_command = rook_pressed
	elif(character_type == "bishop"):
		temporary_command = bishop_pressed
	elif(character_type == "queen"):
		temporary_command = queen_pressed
	elif(character_type == "king"):
		temporary_command = king_pressed

	#Creating and displaying the button
	temporary_button = Button(window, image = temporary_image, height = "80", width = "80", command = lambda:temporary_command(y, x))
	board_button=game_canvas.create_window(temporary_x_coord, temporary_y_coord, window = temporary_button)
	window.update()


def display_team(team):
	#If the figure is the rook calling the display character function
	for i in range(len(team.list)):
		if(team.list[i]=="tower"):
			x = team.x_coord[i]
			y = team.y_coord[i]
			if(team.color == "black"):
				display_character(y, x, b_rook_w, b_rook_b, team.list[i])
			elif(team.color == "white"):
				display_character(y, x, w_rook_w, w_rook_b, team.list[i])

	#If the figure is the pawn calling the display character function
	for i in range(len(team.list)):
		if(team.list[i]=="private"):
			x = team.x_coord[i]
			y = team.y_coord[i]
			if(team.color == "black"):
				display_character(y, x, b_pawn_w, b_pawn_b, team.list[i])
			elif(team.color == "white"):
				display_character(y, x, w_pawn_w, w_pawn_b, team.list[i])

	#If the figure is the knight calling the display character function
	for i in range(len(team.list)):
		if(team.list[i]=="horse"):
			x = team.x_coord[i]
			y = team.y_coord[i]
			if(team.color == "black"):
				display_character(y, x, b_knight_w, b_knight_b, team.list[i])
			elif(team.color == "white"):
				display_character(y, x, w_knight_w, w_knight_b, team.list[i])

	#If the figure is the bishop calling the display character function
	for i in range(len(team.list)):
		if(team.list[i]=="bishop"):
			x = team.x_coord[i]
			y = team.y_coord[i]
			if(team.color == "black"):
				display_character(y, x, b_bishop_w, b_bishop_b, team.list[i])
			elif(team.color == "white"):
				display_character(y, x, w_bishop_w, w_bishop_b, team.list[i])

	#If the figure is the queen calling the display character function
	for i in range(len(team.list)):
		if(team.list[i]=="queen"):
			x = team.x_coord[i]
			y = team.y_coord[i]
			if(team.color == "black"):
				display_character(y, x, b_queen_w, b_queen_b, team.list[i])
			elif(team.color == "white"):
				display_character(y, x, w_queen_w, w_queen_b, team.list[i])

	#If the figure is the king calling the display character function
	for i in range(len(team.list)):
		if(team.list[i]=="king"):
			x = team.x_coord[i]
			y = team.y_coord[i]
			if(team.color == "black"):
				display_character(y, x, b_king_w, b_king_b, team.list[i])
			elif(team.color == "white"):
				display_character(y, x, w_king_w, w_king_b, team.list[i])


def mainloop():

	#Create the background game canvas
	create_buttons()

	#Create white and black teams
	create_team(black_team)
	create_team(white_team)

	#Display white and black teams
	display_team(black_team)
	display_team(white_team)


window = Tk()

#Defining team variables
black_team = Team([None]*16, [None]*16, [None]*16, "black", 0, [1]*16)
white_team = Team([None]*16, [None]*16, [None]*16, "white", 0, [1]*16)
possible_moves = []

#Upload background images
white_square = PhotoImage(file = "white_square.png")
black_square = PhotoImage(file = "black_square.png")
green_b = PhotoImage(file = "green_b.png")
green_w = PhotoImage(file = "green_w.png")

#Upload rooks
b_rook_b = PhotoImage(file = "b_rook_b.png")
b_rook_w = PhotoImage(file = "b_rook_w.png")
w_rook_b = PhotoImage(file = "w_rook_b.png")
w_rook_w = PhotoImage(file = "w_rook_w.png")

#Upload pawns
b_pawn_b = PhotoImage(file = "b_pawn_b.png")
b_pawn_w = PhotoImage(file = "b_pawn_w.png")
w_pawn_b = PhotoImage(file = "w_pawn_b.png")
w_pawn_w = PhotoImage(file = "w_pawn_w.png")

#Upload knights
b_knight_b = PhotoImage(file = "b_knight_b.png")
b_knight_w = PhotoImage(file = "b_knight_w.png")
w_knight_b = PhotoImage(file = "w_knight_b.png")
w_knight_w = PhotoImage(file = "w_knight_w.png")

#Upload bishops
b_bishop_b = PhotoImage(file = "b_bishop_b.png")
b_bishop_w = PhotoImage(file = "b_bishop_w.png")
w_bishop_b = PhotoImage(file = "w_bishop_b.png")
w_bishop_w = PhotoImage(file = "w_bishop_w.png")

#Upload queens
b_queen_b = PhotoImage(file = "b_queen_b.png")
b_queen_w = PhotoImage(file = "b_queen_w.png")
w_queen_b = PhotoImage(file = "w_queen_b.png")
w_queen_w = PhotoImage(file = "w_queen_w.png")

#Upload kings
b_king_b = PhotoImage(file = "b_king_b.png")
b_king_w = PhotoImage(file = "b_king_w.png")
w_king_b = PhotoImage(file = "w_king_b.png")
w_king_w = PhotoImage(file = "w_king_w.png")


configure_game()
mainloop()

window.mainloop()