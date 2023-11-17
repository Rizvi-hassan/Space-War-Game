import pygame
import random

#gamewindow initialisation
pygame.init()
screenWidth = 400
screenHeight = 600
fps = 60
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()


#variables
white = (255, 255, 255)
black = (0, 0, 0)
purple = (11, 6, 30)
violet = (97, 49, 125)
yellow = (250, 231, 22)
running = True
pause = True
gameOver = False
tscale = 10
Time = 0
tick = 1
click = 0
blink = 0
score = 0
health = 50
enemyHealth = 50
life = 3
playBtn = []
stars = []
bullets = []
enimyBullets = []
enimies = []
gameImages = {}
font = pygame.font.SysFont('valorax', 20);
gameImages['enimy'] = pygame.transform.scale(pygame.image.load('images/enimy.png').convert_alpha(), (574//(tscale), 434//(tscale)))
gameImages['fire'] = pygame.transform.scale(pygame.image.load('images/fire.png').convert_alpha(), (274//40, 912//40))
gameImages['warrior'] = pygame.transform.scale(pygame.image.load('images/warrior.png').convert_alpha(), (622//tscale, 411//tscale))
gameImages['attack'] = pygame.transform.scale(pygame.transform.rotate(pygame.image.load('images/attack.png'), 180), (328//60, 1713//90))
gameImages['head'] = pygame.image.load('images/heading.png')
gameImages['play'] = pygame.transform.scale(pygame.image.load('images/play.png'), (787//5, 317//5))
gameImages['heart'] = pygame.transform.scale(pygame.image.load('images/fill-heart.png'), (505//20, 495//20))
gameImages['dead'] = pygame.transform.scale(pygame.image.load('images/empty-heart.png'), (505//20, 495//20))
warriorX = screenWidth//2 - gameImages['warrior'].get_width()//2 -1
warriorY = screenHeight - gameImages['warrior'].get_height()
# print( screenHeight - gameImages['warrior'].get_height())
# warriorX = 149
# warriorY = 468


posy = screenHeight
while(posy > 4):
    posx = screenWidth
    while(posx > 4):
        rad = random.randint(1, 2)
        stars.append([posx+random.randint(-10, 10), posy + random.randint(-10, 10), rad])
        posx -= random.randint(25, 30)
    posy -= random.randint(25, 30)

def writeText(text, x, y, color):
    write = font.render(text, True, color)
    screen.blit(write, [x, y])

#to print stars
def printScreen():
    global life
    #to display hearts
    x = screenWidth - gameImages['heart'].get_width() - 10
    for i in range(life):
        screen.blit(gameImages['heart'], (x, 0))
        x = x - gameImages['heart'].get_width()
    for i in range(3-life):
        screen.blit(gameImages['dead'], (x, 0))
        x = x - gameImages['heart'].get_width()
        
    # to write scores
    writeText('Score: '+str(score), 0, 0, yellow)
    for x, y, radius in stars:
        pygame.draw.circle(screen, white, (x, y), radius)

    # to move the stars and remove the stars which moved out of frame
    speed = 3
    for i in stars:
        i[1] += speed
        if i[1] > screenHeight:
            del stars[stars.index(i)]

    #to display warrior`s health
    writeText(str(health), warriorX+25, warriorY-10, yellow)
            
    # to generate new stars at the top of the screen
    if stars[len(stars)-1][1] in list(range(25, 30)):
        newStars()

    # to move enimies
    enimySpeed = 1
    for i, j, k in enimies:
        screen.blit(i, tuple(j))
        writeText(str(k), j[0]+24, j[1], yellow)
        j[1] += enimySpeed
        if j[0]-warriorX != 0 and j[0] in list(range(0, screenWidth - i.get_width())):
            if j[0]-warriorX < 0:
                j[0] = j[0]+1  
            else:
                j[0] = j[0]-1
        if j[1] >= screenHeight:
            life -= 1
            del enimies[enimies.index([i, j, k])]

    #to change bullets position
    for i, j in bullets:
        screen.blit(i, tuple(j))
        j[1] -= 5
        if j[1] < 0:
            del bullets[bullets.index([i, j])]

    #to change enimy bullets position
    for i, j in enimyBullets:
        screen.blit(i, tuple(j))
        j[1] += 5
        if j[1] > screenHeight:
            del enimyBullets[enimyBullets.index([i, j])]

#to add new stars at the top
def newStars():
    posx = 4
    while(posx < screenWidth):
        posy = 4
        rad = random.randint(1, 2)
        stars.append([posx+random.randint(-20, 20), posy + random.randint(-10, 10), rad])
        posx += random.randint(25, 30)
    

#function to move worrior
def moveWorrior(key):
    global warriorX, warriorY
    shift = 4
    limitR = screenWidth - gameImages['warrior'].get_width()
    if not pause:
        if key[pygame.K_RIGHT] and warriorX+shift <= limitR:
            warriorX += shift
        elif key[pygame.K_LEFT] and warriorX-shift >= 0:
            warriorX -= shift

#function to spawn enimy
def spawnEnimy():
    limitR = screenWidth - gameImages['enimy'].get_width()
    enimies.append([gameImages['enimy'], [random.randint(0, limitR), -gameImages['enimy'].get_height()], enemyHealth])
# spawnEnimy()

#to make warrior fire
def attact(key):
    global bullets
    sep = gameImages['warrior'].get_width() // 2
    if not pause:
        if key[pygame.K_UP]:
            bullets.append([gameImages['fire'], [warriorX+sep - 14, warriorY]])
            bullets.append([gameImages['fire'], [warriorX+sep + 6, warriorY]])

#enimy will fire from this function
def enemyAttack():
    global enimyBullets
    if not pause:
        for i in enimies:
            if abs(warriorX - i[1][0]) < 10:
                sep = i[0].get_width() // 2
                enimyBullets.append([gameImages['attack'], [i[1][0] + sep + 8, i[1][1] ]])
                enimyBullets.append([gameImages['attack'], [i[1][0] + sep - 12, i[1][1] ]])

def collide():
    # collide for enimy
    global score, health, gameOver
    for i, j in bullets:
        for k, l, m in enimies:
            if j[0] in range(l[0], l[0]+k.get_width()) and j[1] in range(l[1], l[1]+k.get_height()):
                enimies[enimies.index([k, l, m])][2] -= 1
                del bullets[bullets.index([i, j])]
                if m == 1:
                    del enimies[enimies.index([k, l, m-1])]
                    score += 100

    for i, j in enimyBullets:
        if j[0] in range(warriorX, warriorX+gameImages['warrior'].get_width()) and j[1] in range(warriorY, warriorY+gameImages['warrior'].get_height() ):
            health -= 1
            del enimyBullets[enimyBullets.index([i, j])]
            if health <= -1:
                gameOver = True
    


def mainMenu():
    global score
    global playBtn
    for x, y, radius in stars:
        pygame.draw.circle(screen, white, (x, y), radius)

    pygame.draw.rect(screen, purple, (50, 150, 300, 250))
    screen.blit(gameImages['head'], (50, 110))
    screen.blit(gameImages['play'], (screenWidth//2 - gameImages['play'].get_width()//2, 270))
    playBtn = [screenWidth//2 - gameImages['play'].get_width()//2, 270]
    writeText('SCORE: --' if score == 0 else 'SCORE: '+str(score), 100, 350, violet)


#loop of the game which controls all work flow. It is called every 60 Times a second
def gameLoop():
    global pause
    printScreen()
    screen.blit(gameImages['warrior'], (warriorX, warriorY))
    moveWorrior(pygame.key.get_pressed())
    collide()
    if gameOver:
        pause = True


while running:
    # global gameOver, pause, score, health 
    if life == 0:
        gameOver = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not gameOver:
                pause = not pause
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if pos[0] in list(range(playBtn[0], gameImages['play'].get_width() + playBtn[0])) and pos[1] in list(range(playBtn[1], gameImages['play'].get_height() + playBtn[1])):
                life = 3
                score = 0
                health = 50
                gameOver = False
                pause = False
                enimies = []
                bullets = []
                enimyBullets = []
                


    if not pause:
        screen.fill(black)
        gameLoop()
    
        if int(Time) % 10 == 0 and tick != int(Time):
            tick = int(Time)
            spawnEnimy()
        
        click+=1;
        if click > 5:
            click = 0
            attact(pygame.key.get_pressed())
            enemyAttack()

        blink += 1
        if blink > 10:
            blink = 0
    
    else:
        mainMenu()

    pygame.display.update()
    
    Time += 1 / fps ;
    clock.tick(fps)

pygame.quit()