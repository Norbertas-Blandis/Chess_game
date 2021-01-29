from tkinter import Tk, Canvas, PhotoImage, Button, messagebox



def configure_game():
	window.geometry("640x640")
	window.title("C H E S S")
	window.configure(bg="white")


class Team:

	def __init__(self, team_list, x_coord, y_coord, color, count, lives, button, alive_characters, in_danger, is_in_danger, castle):
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
		self.castle = castle
		self.did_pawn_transform = [0]*16


class Possible_moves:

	def __init__(self, free_x_list, free_y_list, taken_x, taken_y, attack_x, attack_y, out_x, out_y):
		self.free_x_list = free_x_list
		self.free_y_list = free_y_list
		self.taken_x = taken_x
		self.taken_y = taken_y
		self.attack_x = attack_x
		self.attack_y = attack_y
		self.out_x = out_x
		self.out_y = out_y


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

	#If can castle, split possible moves and possible castles
	if team.list[index] == "king":
		how_many_checks = len(possible_move_x) - len(possible_castles_x)
	else:
		how_many_checks = len(possible_move_x)

	#Looping through all possible moves and if click match, call move_player
	for i in range(how_many_checks):

		possible_move_coord_x = possible_move_x[i]*80
		possible_move_coord_y = possible_move_y[i]*80
		if(click_x > possible_move_coord_x and click_x < possible_move_coord_x+80):
			if(click_y > possible_move_coord_y and click_y < possible_move_coord_y+80):
				move_player(y, x, possible_move_y[i], possible_move_x[i], color, character, index)
	#If king was pressed additionally looping through possible castle moves
	if team.list[index] == "king":
		for i in range(how_many_checks, len(possible_move_x)):
			possible_move_coord_x = possible_move_x[i]*80
			possible_move_coord_y = possible_move_y[i]*80
			if(click_x > possible_move_coord_x and click_x < possible_move_coord_x+80):
				if(click_y > possible_move_coord_y and click_y < possible_move_coord_y+80):
					move_player(y, x, possible_move_y[i], possible_move_x[i], color, character, index) #Moving the king

					if(possible_move_x[i] > x):
						rook_x = 7
						new_rook_x = possible_move_x[i] - 1
					else:
						rook_x = 0
						new_rook_x = possible_move_x[i] + 1
					for z in range(16):
						if(team.x_coord[z] == rook_x and team.y_coord[z] == y):
							temp_index = z
					global did_castle
					did_castle = True
					team.castle = 1
					move_player(y, rook_x, possible_move_y[i], new_rook_x, color, "rook", temp_index) #Moving the rook

	#Looping through all possible attacks and if click match, call remove_player
	for i in range(len(possible_attack_x)):
		possible_attack_coord_x = possible_attack_x[i]*80
		possible_attack_coord_y = possible_attack_y[i]*80
		if(click_x > possible_attack_coord_x and click_x < possible_attack_coord_x+80):
			if(click_y > possible_attack_coord_y and click_y < possible_attack_coord_y+80):
				remove_player(team.y_coord[index], team.x_coord[index], possible_attack_y[i], possible_attack_x[i], color, character, index, team, opp_team)


def removing_unwanted_pieces():

	global possible_moves, possible_attacks

	#Deleting possible moves and attack squares
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
			#Ckecking if the game is over
			if(opp_team.list[i] == "king"):
				messagebox.showinfo("Congratulations!", "Congratulations! The "+color+" team has won!")
				window.destroy()
		else:
			recover_hidden_buttons(opp_team)

	#if the pawn reached other side of the board, choose new character for it
	if(team.count[index] > 0 and (team.y_coord[index] == 7 or team.y_coord[index] == 0) and team.did_pawn_transform[index] == 0):
		pawn_reached_end(index, team)

	move_player(old_y, old_x, new_y, new_x, color, character_type, index)

def move_player(old_y, old_x, new_y, new_x, color, character_type, index):

	global whose_turn, did_castle
	if not did_castle:
		whose_turn += 1

	print(old_x, old_y, " moves to ", new_x, new_y)

	"""print("Do need to clean choices: " + str(clean_pawn_choices))
	if clean_pawn_choices:
		choose_canvas.destroy()
		game_canvas.delete(choose_text)
		clean_pawn_choices = False"""

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

	#if the pawn reached other side of the board, choose new character for it
	if(team.count[index] > 0 and (team.y_coord[index] == 7 or team.y_coord[index] == 0) and team.did_pawn_transform[index] == 0):
		pawn_reached_end(index, team)

	#Calling a function to display new place for the piece
	if(color == "black"):
		display_character(new_y, new_x, image_1, image_2, character_type, color, index)
	elif(color == "white"):
		display_character(new_y, new_x, image_3, image_4, character_type, color, index)
	window.update()


def display_possible_moves(possible_moves, possible_attacks, character_move, team, opp_team):

	#Creating green squares for possible moves
	for i in range(len(character_move.free_x_list)):	
		if(check_square_color(character_move.free_x_list[i], character_move.free_y_list[i]) == "black"):
			temporary_image = green_b
		else:
			temporary_image = green_w

		possible_moves[i] = game_canvas.create_image(80*character_move.free_x_list[i], 80*character_move.free_y_list[i], image = temporary_image, anchor = "nw")
		window.update()

	#Creating red squares for attack moves
	print(len(possible_attacks), len(character_move.attack_x), len(character_move.attack_y))
	for i in range(len(possible_attacks)):

		#Temporarily hiding opp_team button, because it is in the way of red
		for z in range(16):
			if(opp_team.x_coord[z]==character_move.attack_x[i] and opp_team.y_coord[z]==character_move.attack_y[i]):
				opp_team.is_in_danger[z] = 1
				game_canvas.itemconfigure(opp_team.button[z], state = "hidden")

		temporary_image = check_attack_color(character_move.attack_x[i], character_move.attack_y[i], opp_team, opp_team.color)

		possible_attacks[i] = game_canvas.create_image(80*character_move.attack_x[i], 80*character_move.attack_y[i], image = temporary_image, anchor = "nw")
		window.update()


def change_character_type(change, team, index, image_1, image_2):

	removing_unwanted_pieces()

	#Removing choices gui
	choose_canvas.destroy()
	game_canvas.delete(choose_text)
	clean_pawn_choices = 0

	#Changing the character type
	team.list[index] = change
	team.did_pawn_transform[index] = 1
	game_canvas.delete(team.button[index])
	display_character(team.y_coord[index], team.x_coord[index], image_1, image_2, team.list[index], team.color, index)


def click_coordinates_pawn_transform(event, possible_change_buttons, team, index, possible_changes):

	for i in range(len(possible_changes)):

		if(possible_changes[i] == "pawn"):
			if(team.color == "black"):
				temporary_image = b_pawn_w
				image_2 = b_pawn_b
			else:
				temporary_image = w_pawn_w
				image_2 = w_pawn_b

		if(possible_changes[i] == "rook"):
			if(team.color == "black"):
				temporary_image = b_rook_w
				image_2 = b_rook_b
			else:
				temporary_image = w_rook_w
				image_2 = w_rook_b

		if(possible_changes[i] == "knight"):
			if(team.color == "black"):
				temporary_image = b_knight_w
				image_2 = b_knight_b
			else:
				temporary_image = w_knight_w
				image_2 = w_knight_b

		if(possible_changes[i] == "bishop"):
			if(team.color == "black"):
				temporary_image = b_bishop_w
				image_2 = b_bishop_b
			else:
				temporary_image = w_bishop_w
				image_2 = w_bishop_b

		if(possible_changes[i] == "queen"):
			if(team.color == "black"):
				temporary_image = b_queen_w
				image_2 = b_queen_b
			else:
				temporary_image = w_queen_w
				image_2 = w_queen_b

		temporary_coords = choose_canvas.coords(possible_change_buttons[i])
		print(event.x, temporary_coords[0], temporary_coords[0]+80)
		if(event.x > temporary_coords[0] and event.x < temporary_coords[0] + 80):
			print(possible_changes[i], "was chosen")
			change_character_type(possible_changes[i], team, index, temporary_image, image_2)


def pawn_reached_end(index, team):

	global clean_pawn_choices
	clean_pawn_choices = 1
	print(clean_pawn_choices)

	#Creating a list of possible changes 
	possible_changes = []
	for i in range(16):
		if(i == index):
			for z in range(16):
				if(team.life[z] == 0):

					is_same = False
					for j in possible_changes:
						if(j == team.list[z]):
							is_same = True
					if not is_same:
						possible_changes.append(team.list[z])


	print("Can change character type to: ")
	print(possible_changes)

	#Creating a new canvas for choosing new character
	canvas_length = 80*len(possible_changes)
	canvas_heigth = 80
	global choose_canvas, choose_text
	choose_canvas = Canvas(window, height = canvas_heigth, width = canvas_length, bg = "red")
	choose_canvas.grid(column = 0, row = 0, padx = 10, pady = 10)
	choose_text = game_canvas.create_text(300, 265, fill = "blue", font = "Times 15 italic bold", text = "Which character would you like your pawn to transform to?")

	#Creating choose buttons
	possible_change_buttons = [None]*len(possible_changes)
	for i in range(len(possible_changes)):

		if(possible_changes[i] == "pawn"):
			if(team.color == "black"):
				temporary_image = b_pawn_w
				image_2 = b_pawn_b
			else:
				temporary_image = w_pawn_w
				image_2 = w_pawn_b

		if(possible_changes[i] == "rook"):
			if(team.color == "black"):
				temporary_image = b_rook_w
				image_2 = b_rook_b
			else:
				temporary_image = w_rook_w
				image_2 = w_rook_b

		if(possible_changes[i] == "knight"):
			if(team.color == "black"):
				temporary_image = b_knight_w
				image_2 = b_knight_b
			else:
				temporary_image = w_knight_w
				image_2 = w_knight_b

		if(possible_changes[i] == "bishop"):
			if(team.color == "black"):
				temporary_image = b_bishop_w
				image_2 = b_bishop_b
			else:
				temporary_image = w_bishop_w
				image_2 = w_bishop_b

		if(possible_changes[i] == "queen"):
			if(team.color == "black"):
				temporary_image = b_queen_w
				image_2 = b_queen_b
			else:
				temporary_image = w_queen_w
				image_2 = w_queen_b

		"""temporary_button = Button(window, image = temporary_image, height = "80", width = "80", command = lambda:change_character_type(possible_changes[i], team, index, temporary_image, image_2))
		possible_change_buttons[i] = choose_canvas.create_window(40+80*i, 40, window = temporary_button)
		window.update()"""

		possible_change_buttons[i] = choose_canvas.create_image(80*i+2, 2, image = temporary_image, anchor = "nw")

	#Binding key press to check if possible move was pressed
	choose_canvas.bind("<Button-1>", lambda event: click_coordinates_pawn_transform(event, possible_change_buttons, team, index, possible_changes))


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


def pawn_pressed(y, x, color, index, team, opp_team):

	print("Pawn pressed")

	#If the right player order
	if(color == "white"):
		opp_color = "black"
	else:
		opp_color = "white"
	if((whose_turn%2 == 0 and color == "black") or (whose_turn%2 != 0 and color == "white")):
		messagebox.showinfo("Not your move", opp_color.title()+ " team is on the move")
		return None

	#Cleaning possible pawn transformations if needed
	global clean_pawn_choices
	if(clean_pawn_choices == 1):
		choose_canvas.destroy()
		game_canvas.delete(choose_text)
		clean_pawn_choices = 0

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


def rook_pressed(y, x, color, index, team, opp_team):

	#Looking if the right player turn
	if(color == "white"):
		opp_color = "black"
	else:
		opp_color = "white"
	if((whose_turn%2 == 0 and color == "black") or (whose_turn%2 != 0 and color == "white")):
		messagebox.showinfo("Not your move", opp_color.title()+ " team is on the move")
		return None

	#Cleaning possible pawn transformations if needed
	global clean_pawn_choices
	if(clean_pawn_choices == 1):
		choose_canvas.destroy()
		game_canvas.delete(choose_text)
		clean_pawn_choices = 0

	#If it is the queen, do not clear the board
	if(team.list[index] != "queen"):
		removing_unwanted_pieces()
		recover_hidden_buttons(opp_team)

	#Finding out exactly which piece was pressed
	if(color == "black"):
		direction = [1, 1, -1, -1] #1-down, 2-right, 3-up, 4-right
	else:
		direction = [1, 1, -1, -1] #1-down, 2-right, 3-up, 4-right

	#Do not know why, but sometimes x, y are false, so converting them
	x, y = team.x_coord[index], team.y_coord[index]
	if(team.list[index] != "queen"):
		print("Rook pressed at", x, y)
	else:
		print("Queen pressed at", x, y)

	rook_moves = Possible_moves([], [], [], [], [], [], [], [])

	#Looping through all possible directions
	for z in range(len(direction)):

		is_free = True
		temporary_x_coord, temporary_y_coord = x, y

		#Deciding whether the x or y coordinate will change
		if(z % 2 == 0):
			add_to_y = direction[z]
			add_to_x = 0
		else:
			add_to_y = 0
			add_to_x = direction[z]

		#Looping through possible move options until a problem encountered
		while is_free:

			temporary_y_coord += add_to_y
			temporary_x_coord += add_to_x

			for z in range(16):
				if(temporary_y_coord==team.y_coord[z] and temporary_x_coord==team.x_coord[z]):
					if(team.life[z] == 1):
						#print("Space taken at", temporary_x_coord, temporary_y_coord)
						rook_moves.taken_x = temporary_x_coord
						rook_moves.taken_y = temporary_y_coord
						is_free = False

				if(temporary_y_coord==opp_team.y_coord[z] and temporary_x_coord==opp_team.x_coord[z]):
					if(opp_team.life[z] == 1):
						#print("Can attack at", temporary_x_coord, temporary_y_coord)
						rook_moves.attack_x.append(temporary_x_coord)
						rook_moves.attack_y.append(temporary_y_coord)
						is_free = False

				if(temporary_y_coord>7 or temporary_y_coord<0 or temporary_x_coord>7 or temporary_x_coord<0):
					#print("Out of bounds")
					is_free = False

			if is_free:
				print("Space free at", temporary_x_coord, temporary_y_coord)
				rook_moves.free_x_list.append(temporary_x_coord)
				rook_moves.free_y_list.append(temporary_y_coord)

	#If queen, add more possible moves
	if(team.list[index] == "queen"):
		for i in range(len(rook_moves.free_x_list)):
			queen_move.free_x_list.append(rook_moves.free_x_list[i])
			queen_move.free_y_list.append(rook_moves.free_y_list[i])
		for i in range(len(rook_moves.attack_x)):
			queen_move.attack_x.append(rook_moves.attack_x[i])
			queen_move.attack_y.append(rook_moves.attack_y[i])

	#Adding possible moves and attack to seperate lists
	global possible_moves, possible_attacks
	if(team.list[index] == "queen"):
		pass
		possible_moves = [None]*len(queen_move.free_x_list)
		possible_attacks = [None]*len(queen_move.attack_x)
	else:
		possible_moves = [None]*len(rook_moves.free_x_list)
		possible_attacks = [None]*len(rook_moves.attack_x)

	#Binding key press to check if possible move was pressed
	if(team.list[index] == "queen"):
		game_canvas.bind("<Button-1>", lambda event: click_coordinates(event, queen_move.free_x_list, queen_move.free_y_list, y, x, color, "queen", index, team, queen_move.attack_x, queen_move.attack_y, opp_team))
		display_possible_moves(possible_moves, possible_attacks, queen_move, team, opp_team)
	else:
		game_canvas.bind("<Button-1>", lambda event: click_coordinates(event, rook_moves.free_x_list, rook_moves.free_y_list, y, x, color, "rook", index, team, rook_moves.attack_x, rook_moves.attack_y, opp_team))
		display_possible_moves(possible_moves, possible_attacks, rook_moves, team, opp_team)


def knight_pressed(y, x, color, index, team, opp_team):

	print("Knight pressed")

	if(color == "white"):
		opp_color = "black"
	else:
		opp_color = "white"
	if((whose_turn%2 == 0 and color == "black") or (whose_turn%2 != 0 and color == "white")):
		messagebox.showinfo("Not your move", opp_color.title()+ " team is on the move")
		return None

	#Cleaning possible pawn transformations if needed
	global clean_pawn_choices
	if(clean_pawn_choices == 1):
		choose_canvas.destroy()
		game_canvas.delete(choose_text)
		clean_pawn_choices = 0

	removing_unwanted_pieces()

	recover_hidden_buttons(opp_team)

	direction = [(1, 2), (2, 1), (1, -2), (-2, 1)] #(x, y) [down, right, up, left]

	knight_move = Possible_moves([], [], [], [], [], [], [], [])

	#Looping through all possible directions
	for z in range(4):
		direct = direction[z]

		#Determining which direction the piece goes
		if(direct[0] == 1):
			check_x_twice = True
			check_y_twice = False
		else:
			check_x_twice = False
			check_y_twice = True

		#Ckecking all team and opp_team pieces
		for i in range(16):
			if check_x_twice: #If the piece goes up or down

				if(y+direct[1] == team.y_coord[i] and x+1 == team.x_coord[i]):
					knight_move.taken_x.append(team.x_coord[i])
					knight_move.taken_y.append(team.y_coord[i])
					print("Space taken at", team.x_coord[i], team.y_coord[i])
				elif(y+direct[1] == team.y_coord[i] and x-1 == team.x_coord[i]):
					knight_move.taken_x.append(team.x_coord[i])
					knight_move.taken_y.append(team.y_coord[i])
					print("Space taken at", team.x_coord[i], team.y_coord[i])

				if(y+direct[1] == opp_team.y_coord[i] and x+1 == opp_team.x_coord[i]):
					knight_move.attack_x.append(opp_team.x_coord[i])
					knight_move.attack_y.append(opp_team.y_coord[i])
					print("Can attack at", opp_team.x_coord[i], opp_team.y_coord[i])
				elif(y+direct[1] == opp_team.y_coord[i] and x-1 == opp_team.x_coord[i]):
					knight_move.attack_x.append(opp_team.x_coord[i])
					knight_move.attack_y.append(opp_team.y_coord[i])
					print("Can attack at", opp_team.x_coord[i], opp_team.y_coord[i])


			else: #If the piece goes left or right

				if(y+1 == team.y_coord[i] and x+direct[0] == team.x_coord[i]):
					knight_move.taken_x.append(team.x_coord[i])
					knight_move.taken_y.append(team.y_coord[i])
					print("Space taken at", team.x_coord[i], team.y_coord[i])
				elif(y-1 == team.y_coord[i] and x+direct[0] == team.x_coord[i]):
					knight_move.taken_x.append(team.x_coord[i])
					knight_move.taken_y.append(team.y_coord[i])
					print("Space taken at", team.x_coord[i], team.y_coord[i])

				if(y+1 == opp_team.y_coord[i] and x+direct[0] == opp_team.x_coord[i]):
					knight_move.attack_x.append(opp_team.x_coord[i])
					knight_move.attack_y.append(opp_team.y_coord[i])
					print("Can attack at", opp_team.x_coord[i], opp_team.y_coord[i])
				elif(y-1 == opp_team.y_coord[i] and x+direct[0] == opp_team.x_coord[i]):
					knight_move.attack_x.append(opp_team.x_coord[i])
					knight_move.attack_y.append(opp_team.y_coord[i])
					print("Can attack at", opp_team.x_coord[i], opp_team.y_coord[i])

		#Max amount of moves knight can have
		if check_x_twice:
			for z in range(2):

				if(z == 0):
					new_x = x + 1
				else:
					new_x = x - 1

				if(y+direct[1] not in knight_move.taken_y or new_x not in knight_move.taken_x):
					if(y+direct[1] not in knight_move.attack_y or new_x not in knight_move.attack_x):
						knight_move.free_x_list.append(new_x)
						knight_move.free_y_list.append(y+direct[1])

		else:
			for z in range(2):

				if(z == 0):
					new_y = y + 1
				else:
					new_y = y - 1

				if(new_y not in knight_move.taken_y or x+direct[0] not in knight_move.taken_x):
					if(new_y not in knight_move.attack_y or x+direct[0] not in knight_move.attack_x):
						knight_move.free_x_list.append(x+direct[0])
						knight_move.free_y_list.append(new_y)

	#Adding possible moves and attack to seperate lists
	global possible_moves, possible_attacks
	possible_moves = [None]*len(knight_move.free_x_list)
	possible_attacks = [None]*len(knight_move.attack_x)

	#Binding key press to check if possible move was pressed
	game_canvas.bind("<Button-1>", lambda event: click_coordinates(event, knight_move.free_x_list, knight_move.free_y_list, y, x, color, "knight", index, team, knight_move.attack_x, knight_move.attack_y, opp_team))

	display_possible_moves(possible_moves, possible_attacks, knight_move, team, opp_team)


def bishop_pressed(y, x, color, index, team, opp_team):

	if(team.list[index] == "queen"):
		print("Queen was pressed")
	else:
		print("Bishop pressed")

	#If the right player pressed the button
	if(color == "white"):
		opp_color = "black"
	else:
		opp_color = "white"
	if((whose_turn%2 == 0 and color == "black") or (whose_turn%2 != 0 and color == "white")):
		messagebox.showinfo("Not your move", opp_color.title()+ " team is on the move")
		return None

	#Cleaning possible pawn transformations if needed
	global clean_pawn_choices
	if(clean_pawn_choices == 1):
		choose_canvas.destroy()
		game_canvas.delete(choose_text)
		clean_pawn_choices = 0

	removing_unwanted_pieces()

	recover_hidden_buttons(opp_team)

	#Defining key variables
	direction = [(-1, 1), (1, 1), (1, -1), (-1, -1)] #[downleft, downright, upright, upleft]
	bishop_move = Possible_moves([], [], [], [], [], [], [], [])

	#Looping through all directions
	for z in range(len(direction)):
		temporary_addition = direction[z]
		is_free = True
		temporary_x_coord, temporary_y_coord = x, y

		#Checking spaces in the direction if the space is not taken
		while is_free:

			temporary_x_coord += temporary_addition[0]
			temporary_y_coord += temporary_addition[1]

			print(temporary_x_coord, temporary_y_coord)

			#Looking at all team mates and opposition
			for j in range(16):
				if(temporary_x_coord == team.x_coord[j] and temporary_y_coord == team.y_coord[j]):
					print("Space taken at", temporary_x_coord, temporary_y_coord)
					is_free = False

				if(temporary_x_coord == opp_team.x_coord[j] and temporary_y_coord == opp_team.y_coord[j]):
					print("Can attack at", temporary_x_coord, temporary_y_coord)
					bishop_move.attack_x.append(temporary_x_coord)
					bishop_move.attack_y.append(temporary_y_coord)
					is_free = False

				if(temporary_y_coord > 7 or temporary_y_coord < 0 or temporary_x_coord > 7 or temporary_x_coord < 0):
					is_free = False

			if is_free:
				bishop_move.free_x_list.append(temporary_x_coord)
				bishop_move.free_y_list.append(temporary_y_coord)

	#Adding possible moves and attack to seperate lists
	global possible_moves, possible_attacks
	possible_moves = [None]*len(bishop_move.free_x_list)
	possible_attacks = [None]*len(bishop_move.attack_x)

	if(team.list[index] == "queen"):
		global queen_move
		queen_move = bishop_move
	else:
		#Binding key press to check if possible move was pressed
		game_canvas.bind("<Button-1>", lambda event: click_coordinates(event, bishop_move.free_x_list, bishop_move.free_y_list, y, x, color, "bishop", index, team, bishop_move.attack_x, bishop_move.attack_y, opp_team))
		display_possible_moves(possible_moves, possible_attacks, bishop_move, team, opp_team)


def queen_pressed(y, x, color, index, team, opp_team):

	print("Queen pressed")

	removing_unwanted_pieces()

	recover_hidden_buttons(opp_team)

	#Calling both rook and bishop functions
	bishop_pressed(y, x, color, index, team, opp_team)

	rook_pressed(y, x, color, index, team, opp_team)


def king_pressed(y, x, color, index, team, opp_team):

	print("King pressed")

	removing_unwanted_pieces()

	recover_hidden_buttons(opp_team)

	#If the right player pressed the button
	if(color == "white"):
		opp_color = "black"
	else:
		opp_color = "white"
	if((whose_turn%2 == 0 and color == "black") or (whose_turn%2 != 0 and color == "white")):
		messagebox.showinfo("Not your move", opp_color.title()+ " team is on the move")
		return None

	#Cleaning possible pawn transformations if needed
	global clean_pawn_choices
	if(clean_pawn_choices == 1):
		choose_canvas.destroy()
		game_canvas.delete(choose_text)
		clean_pawn_choices = 0

	direction = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)] #[down, downright, right, ... , downleft] anticlockwise

	king_move = Possible_moves([], [], [], [], [], [], [], [])

	#Looping through all moving directions
	for i in direction:

		is_free = True
		temporary_x_coord, temporary_y_coord = x, y
		temporary_x_coord += i[0]
		temporary_y_coord += i[1]

		for z in range(16):
			if(temporary_x_coord == opp_team.x_coord[z] and temporary_y_coord == opp_team.y_coord[z]):
				king_move.attack_x.append(temporary_x_coord)
				king_move.attack_y.append(temporary_y_coord)
				is_free = False
			if(temporary_x_coord == team.x_coord[z] and temporary_y_coord == team.y_coord[z]):
				is_free = False
			if(temporary_x_coord > 7 or temporary_x_coord < 0 or temporary_y_coord > 7 or temporary_y_coord < 0):
				is_free = False

		if is_free:
			king_move.free_x_list.append(temporary_x_coord)
			king_move.free_y_list.append(temporary_y_coord)

	#Adding possible moves and attack to seperate lists
	global possible_moves, possible_attacks, possible_castles_x, possible_castles_y
	possible_castles_x, possible_castles_y = [], []

	#Looking if the king can castle
	if(team.count[index] == 0):
		for i in range(16):
			if(team.list[i] == "rook" and team.castle == 0):
				can_castle = True
				if(team.x_coord[index] > team.x_coord[i]):
					start_coord = team.x_coord[i]+1
					end_coord = team.x_coord[index]
				else:
					start_coord = team.x_coord[index]+1
					end_coord = team.x_coord[i]
				for z in range(start_coord, end_coord):
					print(z)
					for j in range(16):
						if(team.x_coord[j] == z and team.y_coord[j] == team.y_coord[index]):
							print("Taken by their own")
							can_castle = False
						if(opp_team.x_coord[j] == z and opp_team.y_coord[j] == team.y_coord[index]):
							print("Taken by the enemy")
							can_castle = False	

				#If can castle, add it to possible move list	
				if can_castle:
					if team.x_coord[index] > team.x_coord[i]:
						king_move.free_x_list.append(team.x_coord[index] - 2)
						possible_castles_x.append(team.x_coord[index] - 2)
					else:
						king_move.free_x_list.append(team.x_coord[index] + 2)
						possible_castles_x.append(team.x_coord[index] + 2)

					king_move.free_y_list.append(team.y_coord[index])
					possible_castles_y.append(team.y_coord[index])
					print("Can castle at", team.x_coord[i], team.y_coord[i])

	possible_moves = [None]*len(king_move.free_x_list)
	possible_attacks = [None]*len(king_move.attack_x)

	#Binding key press to check if possible move was pressed
	game_canvas.bind("<Button-1>", lambda event: click_coordinates(event, king_move.free_x_list, king_move.free_y_list, y, x, color, "king", index, team, king_move.attack_x, king_move.attack_y, opp_team))

	display_possible_moves(possible_moves, possible_attacks, king_move, team, opp_team)


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
	game_canvas.grid(column = 0, row = 0)

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


	#Finding out exactly which piece was pressed
	if(color == "black"):
		team = black_team
		opp_team = white_team
	else:
		team = white_team
		opp_team = black_team

	#Creating the button
	temporary_button = Button(window, image = temporary_image, height = "80", width = "80", command = lambda:temporary_command(y, x, color, index, team, opp_team))

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
black_team = Team([None]*16, [None]*16, [None]*16, "black", [0]*16, [1]*16, [None]*16, 16, [None]*16, [0]*16, 0)
white_team = Team([None]*16, [None]*16, [None]*16, "white", [0]*16, [1]*16, [None]*16, 16, [None]*16, [0]*16, 0)
possible_moves, possible_attacks = [], []
click_x, click_y = 0, 0
whose_turn = 0 #even-white, odd-black
clean_pawn_choices = 0 #Decide if need to clean pawn transform choices
did_castle = False

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