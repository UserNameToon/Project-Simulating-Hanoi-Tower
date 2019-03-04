"""*****************************************************************************
Name:    Chanchatri Chaichanathong
course:  CMPT 103 43L
purpose: simulating Hanoi tower
ID:      3056450
*****************************************************************************"""

from graphics import *
from time     import sleep

'''**************************** VARIABLES ***********************************'''
uiWidth, uiHeight = 600, 500

'''**************************** FUNCTIONS ***********************************'''
# Purpose: this function start the program
# Parameters: none
# Return: none
def main():  
    '''initilization'''
    global win, msg_main, btn_quit, btn_reset, posts, disks, n_entry
    #creating ui with specific width and hight
    win = GraphWin("HANOI TOWERS (3)(C) 2018 Chanchatri Chaichanathong", 
                   uiWidth, uiHeight)
    posts = []
    disks = []
    #creating buttons 
    btn_quit = (button_create(10, 10, 60,25, 'QUIT', 'white'))
    btn_reset = (button_create(uiWidth - 60 , 10,60,25, 'RESET', 'white'))  
    btn_auto = button_create(uiWidth - 60, 70, 60,25, 'Auto', 'white')
    #creating text object to display main information
    msg_main = info_create(uiWidth/2, uiHeight -475, 'GREETINGS!') 
    
    line_create()
    #creating 'N' and entry box 
    numText = info_create(550, 50, 'N: ')
    #entry with 2 space is use to display input that is more then 9
    #program is set to accept minimum of 1 disk to 9 disks
    n_entry = Entry(Point(565, 50), 2)
    n_entry.setFill('white')
    n_entry.setText(2)
    n_entry.draw(win)
    
    #creating post and line under the posts
    create_posts() 
    making_disks()

    initialize_disk() 
    #display posts info
    show_post_info()
    
    counter = []
    '''main GUI loop'''
    while True:
        #bool is use to make sure that x and y coor only show when not click on any obj
        boolXY = False        

        #counter is use to keep track of the user clicked - if both clicks is valid, 
        #ie disks is smaller, disk exist, etc.., if validate, move the disks to 
        #destination post.
        if len(counter) == 2:
            #click on the same posts - result in invalid move
            if abs(counter[0] - counter[1]) == 0:
                msg_main.setText('Invalide move')
            else:
                validating(posts[counter[0]], posts[counter[1]])
                show_post_info()
            #reset the counter to zero
            counter = []
        try:
            point = win.getMouse()
        except:
            win.close()         
        
        #c is use as a counter of a post
        c = 0
        for p in posts:
            #if the post is click check which post is clicked on.
            if clicked_Check(point, p):
                boolXY = True
                #display the post info <- which post it is
                msg_main.setText('POST: '+ p[0])
                #if first click is on empty post
                if len(p[3]) == 0 and len(counter) == 0:
                    set_red(p[1]) 
                    
                    msg_main.setText('No Disk') 
                #if the first click is on a post that have disks                  
                elif len(p[3]) != 0 and len(counter) == 0:
                    #if post that have disk is click, check if the user click on
                    # the disk or the post - click is above where disks is in the post
                    if point.y < disks[ (p[3][-1]) - 1][1].getP1().getY():
                        set_green(p[1]) 
                        counter.append(c)
                        
                        msg_main.setText('Post: '+ str(p[0]) + ' -> ... ') 
                    #if click on the disk in the post
                    else:
                        #locate where the clicked disk is
                        for i in p[3]: 
                            for eachDisk in disks:
                                if eachDisk[0].getText() == i :
                                    if clicked_Check(point, eachDisk) and eachDisk[0].getText() == p[3][-1]:
                                        set_green(eachDisk[1]) 
                                        #syce with post number (0-2) therefore a|b|c = 65|66|67
                                        # - 65 will give the post location > use as
                                        #way to indentify post where the disk is at
                                        counter.append(ord(p[0]) - 65) 
                                        
                                        msg_main.setText('Disk: ' + str(i) + ' -> ... ') 
                                    #if disk is not the top disk
                                    elif clicked_Check(point, eachDisk) and eachDisk[0].getText() != p[3][-1]:
                                        set_red(eachDisk[1]) 
                                        msg_main.setText('Disk: ' + str(i) + ', is not the top disk')
                #if 2nd click is on the post
                else:                  
                    counter.append(c)
            #if not click on the posts, check if click on the disk
            else: 
                for eachPost in p[3]: 
                    for eachDisk in disks:
                        if eachDisk[0].getText() == eachPost :
                            if clicked_Check(point, eachDisk) and eachDisk[0].getText() == p[3][-1] and len(counter) == 0:
                                boolXY = True
                                set_green(eachDisk[1]) 
                                #syce with post number (0-2) therefore a|b|c = 65|66|67
                                # - 65 will give the post location
                                 #way to indentify post where the disk is at
                                counter.append(ord(p[0]) - 65) 
                                msg_main.setText('Disk: ' + str(eachPost) +  ' -> ... ') 
                             #if disk is not the top disk
                            elif clicked_Check(point, eachDisk) and eachDisk[0].getText() != p[3][-1]:
                                boolXY = True
                                set_red(eachDisk[1]) 
                                msg_main.setText('Disk: ' + str(eachPost) +  ', is not the top disk') 
            #inc counter that identify the posts
            c+=1
        #if click on the quit button, wait for second mouse click, and close window
        if clicked_Check(point, btn_quit):
            msg_main.setText('BYE BYE!')
            break
        #click reset
        elif clicked_Check(point, btn_reset):
            rest_posts()
            boolXY = True
        elif clicked_Check(point, btn_auto):
            if len(posts[0][3]) != 0:
                clicked_auto(btn_auto)
                boolXY = True
            else:
                msg_main.setText('Reset the disk') 
                boolXY = True
        #if not click on disk or post, display the x and y location
        if not boolXY:
            msg_main.setText('X: '  + str(point.getX()) +
                            ' Y: ' + str(point.getY())   )          
    win.getMouse() 
    win.close()  
'''************************* HELPER FUNCTION ********************************''' 
# Purpose: this function validate the move
# Parameters: 1st post obj, 2nd post obj, text obj
# Return: none
def validating(post1,post2):    
    #click from post with disk to empty posts
    if len(post1[3]) != 0 and len(post2[3]) == 0 :  
        post2[3].append(post1[3].pop())
        move_disks(post1,post2)  
        set_green(post2[1]) 
        msg_main.setText( 'Post: '+ post1[0] + ' -> ' + 'Post: '+ post2[0])
    #post2 have disk bigger disk from post1 - both posts have disk
    elif len(post1[3]) != 0 and post2[3][-1] > post1[3][-1]:
        post2[3].append(post1[3].pop())
        move_disks(post1,post2)
        set_green(post2[1]) 
        msg_main.setText('Post: '+ post1[0] + ' -> ' + 'Post: '+ post2[0])        
    #otherwise its a invalide move
    elif len(post1[3]) != 0 and post2[3][-1] < post1[3][-1]:
        set_red(post2[1]) 
        msg_main.setText('Invalid move')
        
# Purpose: this function move disk from 1st post to 2nd post
# Parameters: 1st post obj, 2nd post obj
# Return: none
def move_disks(post1, post2 ): 
    #pass in posts list position
    #move for post1 - post2: posts[chr, rec, text, list]
    for eachDisk in disks:                  
        if eachDisk[0].getText() == post2[3][-1]:  
            eachDisk[1].move( (post2[1].getP1().getX() - eachDisk[1].getCenter().getX()) + 5,
                       (325- (10 * (len(post2[3]) -1))) - eachDisk[1].getP2().getY())
            eachDisk[0].move( (post2[1].getP1().getX() - eachDisk[0].getAnchor().getX()) + 5,
                     (325- (10 * (len(post2[3]) -1))) - eachDisk[0].getAnchor().getY() - 5)

# Purpose: this function check if any of the rec obj is clicked
# Parameters: point, rectangle object: button or posts
# Return: boolean
def clicked_Check(point, button):
    return (button[1].getP1().getX() <= point.x <= button[1].getP2().getX() and
        button[1].getP1().getY() <= point.y <= button[1].getP2().getY())

# Purpose: this function set up for auto move 
# Parameters: rec obj
# Return: none
def clicked_auto(btn_auto):
    N = int(n_entry.getText())
    moveList = Hanoi_moves(N, '0', '1', '2')             
    for i in moveList:
        validating(posts[int(i[0])],posts[ int(i[1])]) 
        sleep(0.5)

# Purpose: this function product seequences of moves, this fuction came from in 
# class notes. 
def Hanoi_moves(height, src, dest, tmp, moves=[]):
    if height >= 1:
        moves = Hanoi_moves(height-1, src, tmp, dest, moves)
        #print("Move disk from", fromPole, "to", toPole)
        moves.append( (src, dest) )
        moves = Hanoi_moves(height-1, tmp, dest, src, moves)
    return moves
'''************************** Initialization Fuctions ***********************'''
# Purpose: this function initialize the game, set the disks into the post
# Parameters: none
# Return: none
def initialize_disk():
    for eachPost in posts: 
        if len(eachPost[3]) != 0:        
            for ele in eachPost[3]:
                for eachDisk in disks:                  
                    if eachDisk[0].getText() == ele:
                        #move disk to the post location
                        eachDisk[1].move( (eachPost[1].getP1().getX() - eachDisk[1].getCenter().getX()) + 5,
                                   (325- (10 * (len(eachPost[3]) - ele))) - eachDisk[1].getP2().getY())
                        eachDisk[0].move( (eachPost[1].getP1().getX() - eachDisk[0].getAnchor().getX()) + 5,
                                 (325- (10 * (len(eachPost[3]) - ele))) - eachDisk[0].getAnchor().getY() - 5)                        
                        eachDisk[1].setFill('yellow')
                        eachDisk[1].draw(win)
                        eachDisk[0].draw(win)     
                        
# Purpose: this function create a list of post, where each post will have a 
# string identifier, a rectangle obj, a text obj, and a list of disk
# Parameters: none
# Return: none   
def create_posts():
    #bottom of post is at y = 345
    x,y, width, height, color = 145, 175,10,150, 'brown'
    for i in range(1,4):
        plist = []
        if i == 1: #set where the disk begin. 
            for j in range(int(n_entry.getText()), 0, -1):
                plist.append(j)
        posts.append([ chr(64 + i),     
                       rec_create(x+((x+5) * (i-1)), y, width, height, color),
                       info_create((x + 5) * i ,345, chr(64 + i) ),
                       plist ] )
       

# Purpose: this function show the info under each posts
# Parameters: none
# Return: none
def show_post_info():      
    for eachPost in posts:    
        eachPost[2].setText(eachPost[0] +'\n' + str(eachPost[3]))

# Purpose: this function clear the list of disks in each post initalize new 
# setting and disk number
# Parameters: none
# Return: none
def rest_posts():
    plist = []
    global disks
    for eachPost in posts:
        eachPost[3].clear()
    if int(n_entry.getText()) > 0 and int(n_entry.getText()) <= 9 :
        for j in range(int(n_entry.getText()), 0, -1):
            plist.append(j) 
            posts[0][3] = plist
            #remove the current disk
            for eachDisk in disks:
                eachDisk[0].undraw()
                eachDisk[1].undraw()
            #empty disk
            disks = []
            #create new disks, draw disks in post 1, update post info
            making_disks()
            initialize_disk()
            show_post_info()
            Hanoi_reset() 
    else:
        msg_main.setText('invalid input, Enter number between 1-9')    
    
# Purpose: this function change the info display when the reset btn is clicked
# Parameters: none
# Return: none
def Hanoi_reset():
    try:
        if int(n_entry.getText()) == 0: 
            msg_main.setText('RESET\nINVALIDATE INPUT')
        else: 
            msg_main.setText('RESET\nN: ' + str(int(n_entry.getText()))) 
    except:
        msg_main.setText('RESET\nINVALIDATE INPUT')

# Purpose: this function create button with text inside
# Parameters: coordinate: x,y | width, height, color
# Return: list of text obj, rectangle obj
def button_create(x, y, width, height, text, color):
    newBtn = rec_create(x, y, width, height, color)
    newText = info_create(x+width//2, y+height//2, text) 
    return [ newText, newBtn]

# Purpose: this function create a rectangle
# Parameters:  coordinate: x,y | width, height, color
# Return: rectangle obj
def rec_create(x, y, width, height, color):
    newRec = Rectangle(Point(x, y), Point(x+width, y+height))
    newRec.setFill(color)
    newRec.draw(win)
    return newRec

# Purpose: this function display informations
# Parameters: coordinate: x,y | string
# Return: text object
def info_create(x, y, text):
    reText = Text(Point(x,y), text)
    reText.draw(win)
    return reText

# Purpose: this function create a line under the posts
# Parameters: none
# Return: none
def line_create():
    botLine = Line(Point(10, 325), Point(590,325))
    botLine.draw(win)   

# Purpose: this function create disks with a set value up to 10 disks
# Parameters: none
# Return: none
def making_disks():
    #when drawing each disks get the lenght of the disk and the center point of the post
    #upon click post or the disk(if valid) will return info about the post position/ disk
    #position, use move base on that    
    # max range is 62|10|62 = 134
    rangeX = 10
    for i in range(10,0,-1): #[ [(80,0),(120,15)] , [ (72,15),(128,30)], ... ]
        box = Rectangle(Point(0 + (5 * i), 100 - (i * 10) ), Point(134 - (5 * i), 110 - (i * 10)))        
        text1 = Text(box.getCenter(), 11-i)
        text1.setSize(7)
        disks.append([text1, box])

'''*************************** Color and stuff ******************************'''
# Purpose: this function change the color of the posts to red if move is invalide
# Parameters:post obj
# Return: none
def set_red(p):
    color = p.config['fill']
    p.setFill('red')
    sleep(0.5)
    p.setFill(color) 

# Purpose: this function change the color of the posts to green if move is valide
# Parameters:post obj
# Return: none    
def set_green(p):
    color = p.config['fill']
    p.setFill('green')
    sleep(0.5)
    p.setFill(color) 
