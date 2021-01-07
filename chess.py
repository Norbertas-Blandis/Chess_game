from tkinter import Tk, Canvas, PhotoImage, Button, messagebox



def configure_game():
	window.geometry("640x640")
	window.title("C H E S S")
	window.configure(bg="white")


class Team:

	def __init__(self, team_list, x_coord, y_coord, color, count, lives, button, alive_characters, in_danger, is_in_danger):
		self.list = team_list
		self.x_coord = x_coord
		self.y_coord = y_coord
		self.color = color
		self.count = count
		self.life = lives
		self.button = button
		self.alive_characters = alive_characters
		self.in_danger_buttons = in_danger
		self.is_in_danger = is_in_danger


class Possible_moves:

	def __init__(self, free_x_list, free_y_list, taken_x, taken_y, attack_x, attack_y):
		self.free_x_list = free_x_list
		self.free_y_list = free_y_list
		self.taken_x = taken_x
		self.taken_y = taken_y
		self.attack_x = attack_x
		self.attack_y = attack_y


def check_square_color(y, x):
	if(y%2==0 and x%2==0):
		temporary_image = "white"
	elif(y%2!=0 and x%2!=0):
		temporary_image = "white"
	else:
		temporary_image = "black"

	return temporary_image


def check_attack_color(x, y, team, color):

	for i in range(16):
		if(team.x_coord[i] == x and team.y_coord[i] == y):
			print("Match")
			if(team.list[i] == "pawn"):
				if(color == "black"):
					image = b_pawn_r
				else:
					image = w_pawn_r

			if(team.list[i] == "knight"):
				if(color == "black"):
					image = b_knight_r
				else:
					image = w_knight_r

			if(team.list[i] == "rook"):
				if(color == "black"):
					image = b_rook_r
				else:
					image = w_rook_r

			if(team.list[i] == "bishop"):
				if(color == "black"):
					image = b_bishop_r
				else:
					image = w_bishop_r

			if(team.list[i] == "queen"):
				if(color == "black"):
					image = b_queen_r
				else:
					image = w_queen_r

			if(team.list[i] == "king"):
				if(color == "black"):
					image = b_king_r
				else:
					image = w_king_r

	return image


def recover_hidden_buttons(opp_team):

	for i in range(16):

		if(opp_team.is_in_danger[i] == 1 and opp_team.life[i] == 1):
			print("Recovering buttons")
			game_canvas.itemconfigure(opp_team.button[i], state = "normal")
			window.update()
			opp_team.is_in_danger[i] = 0


def click_coordinates(event, possible_move_x, possible_move_y, y, x, color, character, index, team, possible_attack_x, possible_attack_y, opp_team):
	click_x, click_y = event.x, event.y

	#If the pawn was mooved for the first time, next move only 1 space
	if(character == "pawn" and team.count[index] == 0):
		team.count[index] += 1

	#Looping through all possible moves and if click match, call move_player
	for i in range(len(possible_move_x)):

		possible_move_coord_x = possible_move_x[i]*80
		possible_move_coord_y = possible_move_y[i]*80
		if(click_x > possible_move_coord_x and click_x < possible_move_coord_x+80):
			if(click_y > possible_move_coord_y and click_y < possible_move_coord_y+80):
				move_player(y, x, possible_move_y[i], possible_move_x[i], color, character, index)

	#Looping through all possible attacks and if click match, call remove_player
	for i in range(len(possible_attack_x)):

		possible_attack_coord_x = possible_attack_x[i]*80
		possible_attack_coord_y = possible_attack_y[i]*80
		if(click_x > possible_attack_coord_x and click_x < possible_attack_coord_x+80):
			if(click_y > possible_attack_coord_y and click_y < possible_attack_coord_y+80):
				remove_player(team.y_coord[index], team.x_coord[index], possible_attack_y[i], possible_attack_x[i], color, character, index, team, opp_team)


def removing_unwanted_pieces():

	#Deleting possible moves and attack squares
	global possible_moves, possible_attacks
	for i in range(len(possible_moves)):
		game_canvas.delete(possible_moves[i])
	for i in range(len(possible_attacks)):
		game_canvas.delete(possible_attacks[i])
	window.update()
	possible_moves, possible_attacks = [], []


def remove_player(old_y, old_x, new_y, new_x, color, character_type, index, team, opp_team):

	removing_unwanted_pieces()

	#Deleting the player from the opposite team
	for i in range(16):
		if(new_x == opp_team.x_coord[i] and new_y == opp_team.y_coord[i]):
			game_canvas.delete(opp_team.button[i])
			opp_team.life[i] = 0
			opp_team.alive_characters -= 1
			opp_team.x_coord[i] = None
			opp_team.x_coord[i] = None
		else:
			recover_hidden_buttons(opp_team)



	move_player(old_y, old_x, new_y, new_x, color, character_type, index)


def move_player(old_y, old_x, new_y, new_x, color, character_type, index):

	global whose_turn
	whose_turn += 1

	print(old_x, old_y, " moves to ", new_x, new_y)

	removing_unwanted_pieces()

	#Changing the piece coordinates to new ones
	if(color == "black"):
		team = black_team
		opp_team = white_team
	else:
		team = white_team
		opp_team = black_team
	for i in range(16):
		if(team.x_coord[i]==old_x and team.y_coord[i]==old_y):
			game_canvas.delete(team.button[i])
			team.x_coord[i] = new_x
			team.y_coord[i] = new_y

	recover_hidden_buttons(opp_team)

	#Checking which character button should be created
	if(character_type == "pawn"):
		image_1 = b_pawn_w
		image_2 = b_pawn_b
		image_3 = w_pawn_w
		image_4 = w_pawn_b
	elif(character_type == "knight"):
		image_1 = b_knight_w
		image_2 = b_knight_b
		image_3 = w_knight_w
		image_4 = w_knight_b
	elif(character_type == "rook"):
		image_1 = b_rook_w
		image_2 = b_rook_b
		image_3 = w_rook_w
		image_4 = w_rook_b
	elif(character_type == "bishop"):
		image_1 = b_bishop_w
		image_2 = b_bishop_b
		image_3 = w_bishop_w
		image_4 = w_bishop_b
	elif(character_type == "queen"):
		image_1 = b_queen_w
		image_2 = b_queen_b
		image_3 = w_queen_w
		image_4 = w_queen_b
	elif(character_type == "king"):
		image_1 = b_king_w
		image_2 = b_king_b
		image_3 = w_king_w
		image_4 = w_king_b

	#Calling a function to display new place for the piece
	if(color == "black"):
		display_character(new_y, new_x, image_1, image_2, character_type, color, index)
	elif(color == "white"):
		display_character(new_y, new_x, image_3, image_4, character_type, color, index)
	window.update()


def pawn_pressed_1(team, opp_team, y, x, direction, z, index):

	global free_move
	new_y_coord, new_x_coord = [], []

	removing_unwanted_pieces()

	recover_hidden_buttons(opp_team)

	#Checking if it is the first move
	if(team.count[index] == 0):
		times = 2
	else:
		times = 1


	possible_attack_x, possible_attack_y, is_taken = [], [], 0
	#Looking at all possible moves for the pawn
	for i in range(times):
		new_x_coord.append(x)

		if(i == 0):
			new_y_coord.append(y + direction)
		else:
			print(new_y_coord[i-1])
			new_y_coord.append(new_y_coord[i-1] + direction)

		#Looping through all pieces and checking if another one is encountered
		for z in range(16):
			if(new_y_coord[i]==opp_team.y_coord[z] and x==opp_team.x_coord[z]):
				if(times == 2 and i == 0): #Makes sure pawn cannot jump on the first move
					is_taken = 1
					print("Space taken at ", x, new_y_coord[i])

			elif(new_y_coord[i] == opp_team.y_coord[z] and i == 0):
				if(x+1 == opp_team.x_coord[z]):
					print("Can attack at ", opp_team.x_coord[z], new_y_coord[i])
					possible_attacks.append(None)
					possible_attack_x.append(opp_team.x_coord[z])
					possible_attack_y.append(opp_team.y_coord[z])

				if(x-1 == opp_team.x_coord[z] and i == 0):
					print("Can attack at ", opp_team.x_coord[z], new_y_coord[i])
					possible_attacks.append(None)
					possible_attack_x.append(opp_team.x_coord[z])
					possible_attack_y.append(opp_team.y_coord[z])

			elif(new_y_coord[i]>7 or new_y_coord[i]<0 or new_x_coord[i]>7 or new_x_coord[i]<0):
				print("Out of bounds")

		if not free_move: #If the pawn cannot move exit the function
			break


	#Binding key press to check if possible move was pressed
	game_canvas.bind("<Button-1>", lambda event: click_coordinates(event, new_x_coord, new_y_coord, y, x, team.color, "pawn", index, team, possible_attack_x, possible_attack_y, opp_team))

	if is_taken == 1:
		times -= 1

	#Creating green squares for possible moves
	for i in range(times):
		if(check_square_color(new_x_coord[i], new_y_coord[i]) == "black"):
			temporary_image = green_b
		else:
			temporary_image = green_w

		possible_moves.append(game_canvas.create_image(80*new_x_coord[i], 80*new_y_coord[i], image = temporary_image, anchor = "nw"))
		window.update()

	#Creating red squares for attack moves
	for i in range(len(possible_attacks)):
		#Temporarily hiding opp_team button, because it is in the way of red
		for z in range(16):
			if(opp_team.x_coord[z]==possible_attack_x[i] and opp_team.y_coord[z]==possible_attack_y[i]):
				opp_team.is_in_danger[z] = 1
				game_canvas.itemconfigure(opp_team.button[z], state = "hidden")

		temporary_image = check_attack_color(possible_attack_x[i], possible_attack_y[i], opp_team, opp_team.color)

		possible_attacks[i] = game_canvas.create_image(80*possible_attack_x[i], 80*possible_attack_y[i], image = temporary_image, anchor = "nw")
		window.update()


def pawn_pressed(y, x, color, index):

	print("Pawn pressed")

	if(color == "white"):
		opp_color = "black"
	else:
		opp_color = "white"
	if((whose_turn%2 == 0 and color == "black") or (whose_turn%2 != 0 and color == "white")):
		messagebox.showinfo("Not your move", opp_color.title()+ " team is on the move")
		return None


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
			team = black_team
			opp_team = white_team
			pawn_pressed_1(black_team, white_team, y, x, 1, z, index)

		if(y==white_team.y_coord[z] and x==white_team.x_coord[z]):
			team = white_team
			opp_team = black_team
			pawn_pressed_1(white_team, black_team, y, x, -1, z, index)

		#If there are no free moves, then quit searching for more moves
		if not free_move:
			break


def rook_possible_moves(i, temporary_y_coord, temporary_x_coord, team, opp_team, direction):

	rook_move = Possible_moves([], [], None, None, [], [])

	#Figuring out if the rook moves vertically or horizontally
	is_free = True
	if direction == "y":
		add_to_y = i
		add_to_x = 0
	else:
		add_to_y = 0
		add_to_x = i

	#Looping through possible move options until a problem encountered
	while is_free:
		temporary_y_coord += add_to_y
		temporary_x_coord += add_to_x
		for z in range(16):
			if(temporary_y_coord==team.y_coord[z] and temporary_x_coord==team.x_coord[z]):
				if(team.life[z] == 1):
					#print("Space taken at", temporary_x_coord, temporary_y_coord)
					rook_move.taken_x = temporary_x_coord
					rook_move.taken_y = temporary_y_coord
					is_free = False
					break

			if(temporary_y_coord==opp_team.y_coord[z] and temporary_x_coord==opp_team.x_coord[z]):
				if(opp_team.life[z] == 1):
					#print("Can attack at", temporary_x_coord, temporary_y_coord)
					rook_move.attack_x.append(temporary_x_coord)
					rook_move.attack_y.append(temporary_y_coord)
					is_free = False
					break

			if(temporary_y_coord>7 or temporary_y_coord<0 or temporary_x_coord>7 or temporary_x_coord<0):
				#print("Out of bounds")
				is_free = False
				break

		if is_free:
			print("Space free at", temporary_x_coord, temporary_y_coord)
			rook_move.free_x_list.append(temporary_x_coord)
			rook_move.free_y_list.append(temporary_y_coord)

	return rook_move


def rook_pressed(y, x, color, index):

	if(whose_turn == 0 and color == "black"):
		return None

	removing_unwanted_pieces()

	#Finding out exactly which piece was pressed
	if(color == "black"):
		team = black_team
		opp_team = white_team
		direction = [1, 1, -1, -1] #1-down, 2-right, 3-up, 4-right
	else:
		team = white_team
		opp_team = black_team
		direction = [1, 1, -1, -1] #1-down, 2-right, 3-up, 4-right

	recover_hidden_buttons(opp_team)

	#Do not know why, but sometimes x, y are false, so converting them
	x, y = team.x_coord[index], team.y_coord[index]
	print("Rook pressed at", x, y)

	#Creating a list and adding to it objects that contain move info
	rook_moves = []
	print("Checking downwards")
	rook_moves.append(rook_possible_moves(direction[0], y, x, team, opp_team, "y"))
	print()
	print("Checking to the right")
	rook_moves.append(rook_possible_moves(direction[1], y, x, team, opp_team, "x"))
	print()
	print("Checking upwards")
	rook_moves.append(rook_possible_moves(direction[2], y, x, team, opp_team, "y"))
	print()
	print("Checking to the left")
	rook_moves.append(rook_possible_moves(direction[3], y, x, team, opp_team, "x"))
	print()

	#Adding possible moves coordinates to new lists
	possible_move_x, possible_move_y = [], []
	possible_attack_x, possible_attack_y = [], []
	for i in range(len(rook_moves)):

		#Adding possible free moves to the list
		if(len(rook_moves[i].free_x_list) > 0):
			for z in range(len(rook_moves[i].free_x_list)):
				possible_moves.append(None)
				possible_move_x.append(rook_moves[i].free_x_list[z])
				possible_move_y.append(rook_moves[i].free_y_list[z])

		#Adding possible attack moves to the list
		if(len(rook_moves[i].attack_x) > 0):
			for z in range(len(rook_moves[i].attack_x)):
				possible_attacks.append(None)
				possible_attack_x.append(rook_moves[i].attack_x[z])
				possible_attack_y.append(rook_moves[i].attack_y[z])


	#Binding key press to check if possible move was pressed
	game_canvas.bind("<Button-1>", lambda event: click_coordinates(event, possible_move_x, possible_move_y, y, x, color, "rook", index, team, possible_attack_x, possible_attack_y, opp_team))

	#Creating green squares for possible moves
	for i in range(len(possible_moves)):	
		if(check_square_color(possible_move_x[i], possible_move_y[i]) == "black"):
			temporary_image = green_b
		else:
			temporary_image = green_w

		possible_moves[i] = game_canvas.create_image(80*possible_move_x[i], 80*possible_move_y[i], image = temporary_image, anchor = "nw")
		window.update()

	#Creating red squares for attack moves
	for i in range(len(possible_attacks)):

		#Temporarily hiding opp_team button, because it is in the way of red
		for z in range(16):
			if(opp_team.x_coord[z]==possible_attack_x[i] and opp_team.y_coord[z]==possible_attack_y[i]):
				opp_team.is_in_danger[z] = 1
				game_canvas.itemconfigure(opp_team.button[z], state = "hidden")

		temporary_image = check_attack_color(possible_attack_x[i], possible_attack_y[i], opp_team, opp_team.color)

		possible_attacks[i] = game_canvas.create_image(80*possible_attack_x[i], 80*possible_attack_y[i], image = temporary_image, anchor = "nw")
		window.update()


def knight_pressed(y, x, color, index):
	if(color == "black"):
		direction = 1
		team = black_team
	else:
		direction = -1
		team = white_team
	print("Knight pressed")


def bishop_pressed(y, x, color, index):
	if(color == "black"):
		direction = 1
		team = black_team
	else:
		direction = -1
		team = white_team
	print("Bishop pressed")


def queen_pressed(y, x, color, index):
	if(color == "black"):
		direction = 1
		team = black_team
	else:
		direction = -1
		team = white_team
	print("Queen pressed")


def king_pressed(y, x, color, index):
	if(color == "black"):
		direction = 1
		team = black_team
	else:
		direction = -1
		team = white_team
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
		team.list[x] = "pawn"
		team.x_coord[x] = x
		if(team.color == "black"):
			team.y_coord[x] = 1
		else:
			team.y_coord[x] = 6

	for x in range(8, 10):
		team.list[x] = "rook"
		if(team.color == "black"):
			team.y_coord[x] = 0
		else:
			team.y_coord[x] = 7
	team.x_coord[8] = 0
	team.x_coord[9] = 7


	for x in range(10, 12):
		team.list[x] = "knight"
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


def display_character(y, x, image_1, image_2, character_type, color, index):

	#Converting coordinates into pixels in the canvas
	temporary_x_coord = 40 + x*80
	temporary_y_coord = 40 + y*80

	#Check wether the background is white or black
	if(check_square_color(y, x) == "white"):
		temporary_image = image_1
	else:
		temporary_image = image_2

	#Checking which character button should be created
	if(character_type == "pawn"):
		temporary_command = pawn_pressed
	elif(character_type == "knight"):
		temporary_command = knight_pressed
	elif(character_type == "rook"):
		temporary_command = rook_pressed
	elif(character_type == "bishop"):
		temporary_command = bishop_pressed
	elif(character_type == "queen"):
		temporary_command = queen_pressed
	elif(character_type == "king"):
		temporary_command = king_pressed

	#Creating the button
	temporary_button = Button(window, image = temporary_image, height = "80", width = "80", command = lambda:temporary_command(y, x, color, index))

	#Adding the created button to the team class
	if(color == "black"):
		team = black_team
	else:
		team = white_team
	for i in range(16):
		if(team.x_coord[i]==x and team.y_coord[i]==y):
			team.button[i] = game_canvas.create_window(temporary_x_coord, temporary_y_coord, window = temporary_button)
	window.update()


def display_team(team):
	#If the figure is the rook calling the display character function
	for i in range(len(team.list)):
		if(team.list[i]=="rook"):
			x = team.x_coord[i]
			y = team.y_coord[i]
			if(team.color == "black"):
				display_character(y, x, b_rook_w, b_rook_b, team.list[i], team.color, i)
			elif(team.color == "white"):
				display_character(y, x, w_rook_w, w_rook_b, team.list[i], team.color, i)

	#If the figure is the pawn calling the display character function
	for i in range(len(team.list)):
		if(team.list[i]=="pawn"):
			x = team.x_coord[i]
			y = team.y_coord[i]
			if(team.color == "black"):
				display_character(y, x, b_pawn_w, b_pawn_b, team.list[i], team.color, i)
			elif(team.color == "white"):
				display_character(y, x, w_pawn_w, w_pawn_b, team.list[i], team.color, i)

	#If the figure is the knight calling the display character function
	for i in range(len(team.list)):
		if(team.list[i]=="knight"):
			x = team.x_coord[i]
			y = team.y_coord[i]
			if(team.color == "black"):
				display_character(y, x, b_knight_w, b_knight_b, team.list[i], team.color, i)
			elif(team.color == "white"):
				display_character(y, x, w_knight_w, w_knight_b, team.list[i], team.color, i)

	#If the figure is the bishop calling the display character function
	for i in range(len(team.list)):
		if(team.list[i]=="bishop"):
			x = team.x_coord[i]
			y = team.y_coord[i]
			if(team.color == "black"):
				display_character(y, x, b_bishop_w, b_bishop_b, team.list[i], team.color, i)
			elif(team.color == "white"):
				display_character(y, x, w_bishop_w, w_bishop_b, team.list[i], team.color, i)

	#If the figure is the queen calling the display character function
	for i in range(len(team.list)):
		if(team.list[i]=="queen"):
			x = team.x_coord[i]
			y = team.y_coord[i]
			if(team.color == "black"):
				display_character(y, x, b_queen_w, b_queen_b, team.list[i], team.color, i)
			elif(team.color == "white"):
				display_character(y, x, w_queen_w, w_queen_b, team.list[i], team.color, i)

	#If the figure is the king calling the display character function
	for i in range(len(team.list)):
		if(team.list[i]=="king"):
			x = team.x_coord[i]
			y = team.y_coord[i]
			if(team.color == "black"):
				display_character(y, x, b_king_w, b_king_b, team.list[i], team.color, i)
			elif(team.color == "white"):
				display_character(y, x, w_king_w, w_king_b, team.list[i], team.color, i)


def mainloop():

	#Create the background game canvas
	create_buttons()

	game_canvas.bind("<Button-1>", click_coordinates)

	#Create white and black teams
	create_team(black_team)
	create_team(white_team)

	#Display white and black teams
	display_team(black_team)
	display_team(white_team)



window = Tk()

#Defining team variables
black_team = Team([None]*16, [None]*16, [None]*16, "black", [0]*16, [1]*16, [None]*16, 16, [None]*16, [0]*16)
white_team = Team([None]*16, [None]*16, [None]*16, "white", [0]*16, [1]*16, [None]*16, 16, [None]*16, [0]*16)
possible_moves, possible_attacks = [], []
click_x, click_y = 0, 0
whose_turn = 0 #even-white, odd-black

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
b_rook_r = PhotoImage(file = "b_rook_r.png")
w_rook_r = PhotoImage(file = "w_rook_r.png")

#Upload pawns
b_pawn_b = PhotoImage(file = "b_pawn_b.png")
b_pawn_w = PhotoImage(file = "b_pawn_w.png")
w_pawn_b = PhotoImage(file = "w_pawn_b.png")
w_pawn_w = PhotoImage(file = "w_pawn_w.png")
b_pawn_r = PhotoImage(file = "b_pawn_r.png")
w_pawn_r = PhotoImage(file = "w_pawn_r.png")

#Upload knights
b_knight_b = PhotoImage(file = "b_knight_b.png")
b_knight_w = PhotoImage(file = "b_knight_w.png")
w_knight_b = PhotoImage(file = "w_knight_b.png")
w_knight_w = PhotoImage(file = "w_knight_w.png")
b_knight_r = PhotoImage(file = "b_knight_r.png")
w_knight_r = PhotoImage(file = "w_knight_r.png")

#Upload bishops
b_bishop_b = PhotoImage(file = "b_bishop_b.png")
b_bishop_w = PhotoImage(file = "b_bishop_w.png")
w_bishop_b = PhotoImage(file = "w_bishop_b.png")
w_bishop_w = PhotoImage(file = "w_bishop_w.png")
b_bishop_r = PhotoImage(file = "b_bishop_r.png")
w_bishop_r = PhotoImage(file = "w_bishop_r.png")

#Upload queens
b_queen_b = PhotoImage(file = "b_queen_b.png")
b_queen_w = PhotoImage(file = "b_queen_w.png")
w_queen_b = PhotoImage(file = "w_queen_b.png")
w_queen_w = PhotoImage(file = "w_queen_w.png")
b_queen_r = PhotoImage(file = "b_queen_r.png")
w_queen_r = PhotoImage(file = "w_queen_r.png")

#Upload kings
b_king_b = PhotoImage(file = "b_king_b.png")
b_king_w = PhotoImage(file = "b_king_w.png")
w_king_b = PhotoImage(file = "w_king_b.png")
w_king_w = PhotoImage(file = "w_king_w.png")
b_king_r = PhotoImage(file = "b_king_r.png")
w_king_r = PhotoImage(file = "w_king_r.png")


configure_game()
mainloop()

window.mainloop()