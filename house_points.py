import sys
import os
import pygame
import time

title_height = 150

gryfindor = 0
ravenclaw = 1
hufflepuff = 2
slytherin = 3
house_points = [0, 0, 0, 0]
house_point_files = ["./gryfindor_points.txt", "./ravenclaw_points.txt", "./hufflepuff_points.txt", "./slytherin_points.txt"]


selection_indicator_pos = 0 # will be 1-4 for gryfindor, ravenclaw, hufflepuff, slytherin

pygame.init()
pygame.font.init()

#get current screen info (resolution)
screenInfo = pygame.display.Info()
screenWidth = 1000#int(screenInfo.current_w)
screenHeight = 500#int(screenInfo.current_h)

screenWidth = int(screenInfo.current_w)
screenHeight = int(screenInfo.current_h)

modify_house_points = ""


house_buffer = 25
house_width = int((screenWidth/4 - 2*house_buffer))
house_width = int((screenWidth - house_buffer*5) / 4)

#so our circles are good, the indicater height will match house_width column size
selection_indicator_height = 50

gryfindor_x = house_buffer
ravenclaw_x = house_buffer + house_width + house_buffer
hufflepuff_x = house_buffer + house_width + house_buffer + house_width + house_buffer
slytherin_x = house_buffer + house_width + house_buffer + house_width + house_buffer + house_width + house_buffer
house_x_pos = [gryfindor_x, ravenclaw_x, hufflepuff_x, slytherin_x]
house_colors = [(255,0,0), (0, 0, 255), (255,255,0), (0,255,0)]


#populate house points if they don't exist
for index,txt_file in enumerate(house_point_files):
	if(os.path.isfile(txt_file) == False):
		f = open(txt_file, "w")
		f.write('150\n')
		f.close()

#set starting point for next window to 0,0 (top left corner of screen)
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)
content_window = pygame.display.set_mode((screenWidth, screenHeight), pygame.NOFRAME)


#get maximum font sizem for width/height constraint
def getMaxCharSize(width, height, text = '3'):
	#90% of width
	#width = width*0.9
	size = 10;
	while(True):
		x = pygame.font.Font(None, size).size(text)[0]
		y = pygame.font.Font(None, size).size(text)[1]
		if(x < width and y < height):
			size += 10
		else:
			#woah woah woah...back it up
			size -= 10
			break
	x = pygame.font.Font(None, size).size(text)[0]
	y = pygame.font.Font(None, size).size(text)[1]
	return size


def blitWindow(label, center = True, pos = (0, 0)):
	#make window white
	#window.fill((255,255,255))
	if(center):
		textpos = label.get_rect(centerx=screenWidth/2)
	else:
		textpos = pos
	content_window.blit(label, textpos)
	pygame.display.update()

#display title
def displayTitle():
	title = "House Points"
	size = getMaxCharSize(screenWidth, title_height, title)
	myfont = pygame.font.Font(None, size)
	label = myfont.render(title, 1, (255,255,255))
	blitWindow(label)


#read house point files in and store house points
def getHousePoints():
	global house_points
	#iterate over house point files
	for index,txt_file in enumerate(house_point_files):
		f = open(txt_file, "r") #open file
		house_points[index] = float(f.readline()) #read amount into house_points
		f.close()#close file

#display house points in teh window
def displayHousePoints():
	print(house_points)
	#clear current display of stuff first
	pygame.draw.rect(content_window, (0,0,0), (0, title_height+selection_indicator_height, screenWidth, (screenHeight - (title_height+selection_indicator_height))), 0)
	max_points = max(house_points)
	#make sure max_points isn't 0
	if(max_points == 0):
		max_points = 1
	#iterate over house points and draw bar/point value to screen.
	for index, points in enumerate(house_points):
		#convert double to int
		points = int(points)
		#calculate max font size for house numerical value
		size = getMaxCharSize(house_width, house_width, str(points))
		#generate font
		font = pygame.font.SysFont(None, size)
		#calculate height of house points bar
		height = (points/max_points) * (screenHeight - title_height - selection_indicator_height)
		#calculate y position for house points
		y = screenHeight - height
		#draw recangle for house
		pygame.draw.rect(content_window, house_colors[index], (house_x_pos[index],y,house_width,height), 0)
		#create label to note how many house points house has
		label = font.render(str(points), 1, (255,255,255))
		#draw house point label on top of bar
		content_window.blit(label, (house_x_pos[index], (screenHeight-house_width)))
	#update display to commit all house point bars and point values to screen
	pygame.display.update()
	

def moveIndicator(key):
	global selection_indicator_pos
	global modify_house_points
	print(key)
	if(key == pygame.K_LEFT):
		selection_indicator_pos -= 1
		if(selection_indicator_pos < 1):
			selection_indicator_pos = 4
	elif(key == pygame.K_RIGHT):
		selection_indicator_pos += 1
		if(selection_indicator_pos > 4):
			selection_indicator_pos = 1
	#if position not set...don't do anything
	if(selection_indicator_pos < 1):
		return
	#0-9
	if(key >= 256 and key <= 265 or key >= 48 and key <= 57):
		#this is 0-9
		if(key > 60):
			number = key - 256 #convert key to numerical value
		else:
			number = key - 48#convert key to numerical value
		#validate modify house points has + or - in the front
		if(len(modify_house_points) > 0):
			if(modify_house_points[0] == "-" or modify_house_points[0] == "+"):
				modify_house_points += str(number) #concatentate current modify with new number
		

	#+/-
	if(key == pygame.K_KP_PLUS or key == pygame.K_PLUS):
		print("key+")
		if(len(modify_house_points) == 0):
			modify_house_points = "+"
	if(key == pygame.K_KP_MINUS or key == pygame.K_MINUS):
		print("key-")
		if(len(modify_house_points) == 0):
			modify_house_points = "-"
	#detect return key
	if(key == pygame.K_RETURN or key == pygame.K_KP_ENTER):
		print("return pressed -- modify house points")
		if(len(modify_house_points) > 1):
			modify_value = int(modify_house_points[1:len(modify_house_points)])
			print("value: " + str(modify_value))
			updateAndSaveNewHousePoints()
			
	#detect backspace
	if(key == pygame.K_BACKSPACE):
		print("backspace")
		modify_house_points = modify_house_points[0:len(modify_house_points)-1]
	
	print(modify_house_points)
	if(selection_indicator_pos > 0 and selection_indicator_pos < 5):
		drawInidicator(selection_indicator_pos)
		drawModifyHousePoints()

def updateAndSaveNewHousePoints():
	global house_points
	global modify_house_points
	global selection_indicator_pos
	#first increment or decrement points
	sign = modify_house_points[0]
	amount = int(modify_house_points[1:len(modify_house_points)])
	if(sign == "+"):
		#increment
		house_points[selection_indicator_pos-1] += amount
	else:
		#decrement
		house_points[selection_indicator_pos-1] -= amount

	#update house points to make sure none are negative
	for index, points in enumerate(house_points):
		if(points < 0):
			house_points[index] = 0

	#reset position of indicator
	selection_indicator_pos = 0
	#reset value to house points
	modify_house_points = ""
	#erase update indicators
	clearIndicator()
	#redraw house points
	displayHousePoints()
	#overwrite new values to files
	saveHousePointsToFiles()

#update house point files to new values
def saveHousePointsToFiles():
	#erase files -- gonna just re-write them
	for txt_file in house_point_files:
		os.remove(txt_file)
	#iterate over files and write new value
	for index,txt_file in enumerate(house_point_files):
		#open file for writting
		f = open(txt_file, "w")
		#write new value in integer form
		f.write(str(int(house_points[index])) + '\n')
		#clost file
		f.close()

#giver user feedback based on what they're typing
def drawModifyHousePoints():
	global modify_house_points
	print("house points: " + str(modify_house_points))
	
	font_size = getMaxCharSize(screenWidth, selection_indicator_height, modify_house_points)
	font = pygame.font.SysFont(None, font_size)
	label = font.render(modify_house_points, 1, (255,255,255))
	content_window.blit(label, (0, title_height))
	pygame.display.update()
	


def drawInidicator(position):
	x_pos = house_x_pos[position-1]
	color = house_colors[position-1]
	clearIndicator()
	pygame.draw.circle(content_window, color, (x_pos+house_width/2, title_height+selection_indicator_height/2), selection_indicator_height/2)
	pygame.display.update()

def clearIndicator():
	pygame.draw.rect(content_window, (0,0,0), (0, title_height, screenWidth, selection_indicator_height), 0)
	pygame.display.update()

def mainLoop():
	#fps = 30
	#clock = pygame.time.Clock()
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

			if(event.type == pygame.KEYUP):
				#key = pygame.key.get_pressed()
				moveIndicator(event.key)


if __name__ == "__main__":
	content_window.fill((0,0,0))
	pygame.display.update()
	#populate points
	getHousePoints()
	#display bars
	displayHousePoints()
	#display title
	displayTitle()
	#run indefinite main loop
	mainLoop()
