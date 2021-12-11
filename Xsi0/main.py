import numpy.random
import pygame
from pygame import font


def drawLines(display, color, width, height, lineWidth=1):
    pygame.draw.line(display, (0, 0, 0), (width * 0.75, 0), (width * 0.75, height), 5)
    rightWidth = 0.25 * width
    width -= 0.25 * width  # loc de settings
    paddingX = 0.15 * width
    paddingY = 0.10 * height
    topMargin = paddingY
    leftMargin = paddingX
    rightMargin = width - paddingX
    bottomMargin = height - paddingY
    mapHeight = bottomMargin - topMargin
    mapWidth = rightMargin - leftMargin

    pygame.draw.line(display, color, (leftMargin, mapHeight / 3 + topMargin), (rightMargin, mapHeight / 3 + topMargin),
                     lineWidth)
    pygame.draw.line(display, color, (leftMargin, (mapHeight * 2) / 3 + topMargin),
                     (rightMargin, (mapHeight * 2) / 3 + topMargin), lineWidth)
    pygame.draw.line(display, color, (mapWidth / 3 + leftMargin, topMargin), (mapWidth / 3 + leftMargin, bottomMargin),
                     lineWidth)
    pygame.draw.line(display, color, ((mapWidth * 2) / 3 + leftMargin, topMargin),
                     ((mapWidth * 2) / 3 + leftMargin, bottomMargin), lineWidth)


def addClickBoxes(width, height):
    width -= 0.25 * width  # loc de settings
    paddingX = 0.15 * width
    paddingY = 0.10 * height
    topMargin = paddingY
    leftMargin = paddingX
    rightMargin = width - paddingX
    bottomMargin = height - paddingY
    mapHeight = bottomMargin - topMargin
    mapWidth = rightMargin - leftMargin
    res = [pygame.Rect(leftMargin, topMargin, mapWidth / 3, mapHeight / 3),
           pygame.Rect(mapWidth / 3 + leftMargin, topMargin, mapWidth / 3, mapHeight / 3),
           pygame.Rect(mapWidth * 2 / 3 + leftMargin, topMargin, mapWidth / 3, mapHeight / 3),
           pygame.Rect(leftMargin, mapHeight / 3 + topMargin, mapWidth / 3, mapHeight / 3),
           pygame.Rect(mapWidth / 3 + leftMargin, mapHeight / 3 + topMargin, mapWidth / 3, mapHeight / 3),
           pygame.Rect(mapWidth * 2 / 3 + leftMargin, mapHeight / 3 + topMargin, mapWidth / 3, mapHeight / 3),
           pygame.Rect(leftMargin, mapHeight * 2 / 3 + topMargin, mapWidth / 3, mapHeight / 3),
           pygame.Rect(mapWidth / 3 + leftMargin, mapHeight * 2 / 3 + topMargin, mapWidth / 3, mapHeight / 3),
           pygame.Rect(mapWidth * 2 / 3 + leftMargin, mapHeight * 2 / 3 + topMargin, mapWidth / 3, mapHeight / 3)]
    return res


def verifStareCastig(map):
    for linie in range(3):
        if map[linie][0] != 0 and map[linie][0] == map[linie][1] == map[linie][2]:
            return map[linie][0]

    for coloana in range(3):
        if map[0][coloana] != 0 and map[0][coloana] == map[1][coloana] == map[2][coloana]:
            return map[0][coloana]

    if map[0][0] == map[1][1] == map[2][2] and map[0][0] != 0:
        return map[0][0]
    if map[0][2] == map[1][1] == map[2][0] and map[0][2] != 0:
        return map[0][2]
    return 0


def addZero(boxes, map, indBox, imagesToDisplay, redSquare, clickedInThePast):
    contBox = 0
    map[indBox // 3][indBox % 3] = 2
    for box in boxes:
        if contBox == indBox:
            rect = redSquare.get_rect()
            rect.width = box.width
            rect.height = box.height
            rect.center = box.center
            imagesToDisplay.append((rect, 2))
            clickedInThePast.append(box)
        contBox += 1
    return -1


# def selectSpot(poz,boxes):
def randomSelect(map):
    emptySpaces = []
    for linia in range(3):
        for coloana in range(3):
            if map[linia][coloana] == 0:
                emptySpaces.append(int(3 * linia + coloana))
    if (len(emptySpaces) > 0):
        indAles = numpy.random.randint(0, len(emptySpaces) - 1)
        return emptySpaces[indAles]


def cautCastigator(map):
    castigator = verifStareCastig(map)
    winnerFound = 0
    if castigator == 1:
        print("Jucatorul a castigat!")
        winnerFound = 1
    elif castigator == 2:
        print("Calculatorul a castigat!")
        winnerFound = 2
    elif castigator == 0 and len(availablePositions(map)) == 0:
        winnerFound = 3
        print("Remiza!")
    return winnerFound


def availablePositions(map):
    res = []
    for linie in range(3):
        for coloana in range(3):
            if map[linie][coloana] == 0:
                res.append((linie, coloana))
    return res


def needsMove(map, player):
    for linie in range(3):
        takenSpots = 0
        emptyLine = -1
        emptyCol = -1
        for coloana in range(3):
            if (map[linie][coloana] == player):
                takenSpots += 1
            elif (map[linie][coloana] == 0):
                emptyLine = linie
                emptyCol = coloana

        if takenSpots == 2 and emptyCol != -1:
            return (emptyLine, emptyCol)
    # testez pe fiecare linie daca pot pierde/pot castiga

    for coloana in range(3):
        takenSpots = 0
        emptyLine = -1
        emptyCol = -1
        for linie in range(3):
            if (map[linie][coloana] == player):
                takenSpots += 1
            elif (map[linie][coloana] == 0):
                emptyLine = linie
                emptyCol = coloana

        if takenSpots == 2 and emptyCol != -1:
            return (emptyLine, emptyCol)
    # testez pe fiecare coloana daca pot pierde/pot castiga

    takenSpots = 0
    lin = -1
    col = -1
    for ind in range(3):
        if map[ind][ind] == player:
            takenSpots += 1
        elif map[ind][ind] == 0:
            lin = ind
            col = ind
    if takenSpots == 2 and lin != -1:
        return (lin, col)
    # diag principala
    takenSpots = 0
    lin = -1
    col = -1
    for ind in range(3):
        if map[ind][2 - ind] == player:
            takenSpots += 1
        elif map[ind][2 - ind] == 0:
            lin = ind
            col = ind
    if takenSpots == 2 and lin != -1:
        return (lin, col)
    # diagSecundara
    return (-1, -1)


def takeCorner(map):
    empty = []
    if map[0][0] == 0:
        empty.append((0, 0))
    if map[0][2] == 0:
        empty.append((0, 2))
    if map[2][0] == 0:
        empty.append((2, 0))
    if map[2][2] == 0:
        empty.append((2, 2))
    if len(empty) > 0:
        indice = numpy.random.randint(0, len(empty))
        return empty[indice]
    else:
        return (-1, -1)


def takeCenter(map):
    if map[1][1] == 0:
        return (1, 1)
    else:
        return (-1, -1)


def takeSides(map):
    empty = []
    if map[0][1] == 0:
        empty.append((0, 1))
    if map[1][0] == 0:
        empty.append((1, 0))
    if map[1][2] == 0:
        empty.append((1, 2))
    if map[2][1] == 0:
        empty.append((2, 1))
    if len(empty) > 0:
        indice = numpy.random.randint(0, len(empty))
        return empty[indice]
    else:
        return (-1, -1)


def optimalSelect(map):
    (linie, coloana) = needsMove(map, 2)
    if (linie, coloana) != (-1, -1):
        print("linieAI")
        map[linie][coloana] = 1
        return linie * 3 + coloana
    (linie, coloana) = needsMove(map, 1)
    if (linie, coloana) != (-1, -1):
        print("linieJucator")
        map[linie][coloana] = 1
        return linie * 3 + coloana
    (linie, coloana) = takeSides(map)
    if (linie, coloana) != (-1, -1):
        print("Lateral")
        map[linie][coloana] = 1
        return linie * 3 + coloana
    (linie, coloana) = takeCorner(map)
    if (linie, coloana) != (-1, -1):
        print("Colt")
        map[linie][coloana] = 1
        return linie * 3 + coloana
    (linie, coloana) = takeCenter(map)
    if (linie, coloana) != (-1, -1):
        print("Centru")
        map[linie][coloana] = 1
        return linie * 3 + coloana


def semiRandomSelect(map):
    if len(availablePositions(map)) % 4 == 0:
        return findBestMove(map)
    else:
        print("random")
        return randomSelect(map)


def displayScore(score, mainDisplay, width, height):
    rightWidth = 0.25 * width
    width -= 0.25 * width  # loc de settings
    paddingX = 0.15 * rightWidth
    paddingY = 0.20 * height

    scoreString = str(score)
    scoreTest = 'Score: ' + scoreString
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    textsurface = myfont.render(scoreTest, False, (0, 0, 0))
    mainDisplay.blit(textsurface, (paddingX + width, paddingY))


def displayPlayAgain(mainDisplay, width, height):
    res = []
    rightWidth = 0.25 * width
    width -= 0.25 * width  # loc de settings
    paddingX = 0.15 * rightWidth
    paddingY = 0.50 * height

    playAgainText = 'Doriti sa mai jucati?'
    myfont = pygame.font.SysFont('Comic Sans MS', 15)
    textsurface = myfont.render(playAgainText, False, (0, 0, 0))
    mainDisplay.blit(textsurface, (paddingX + width, paddingY))
    Yes = 'Da'
    myfont = pygame.font.SysFont('Comic Sans MS', 25)
    textsurface = myfont.render(Yes, False, (0, 0, 0))
    rectDa = textsurface.get_rect()
    mainDisplay.blit(textsurface, (paddingX / 2 + width, paddingY + 0.25 * paddingY))
    No = 'Nu'
    myfont = pygame.font.SysFont('Comic Sans MS', 25)
    textsurface = myfont.render(No, False, (0, 0, 0))
    rectNu = textsurface.get_rect()
    mainDisplay.blit(textsurface, (paddingX + rightWidth * 0.55 + width, paddingY + 0.25 * paddingY))
    res.append(pygame.Rect(paddingX / 2 + width, paddingY + 0.25 * paddingY, rectDa.width,
                           rectDa.height))
    res.append(pygame.Rect(paddingX + rightWidth * 0.55 + width, paddingY + 0.25 * paddingY, rectNu.width,
                           rectNu.height))
    return res

def giveScoreForComputer(statusJoc):
    if statusJoc==2:
        return 100
    elif statusJoc==1:
        return -500
    return 0

def statusJoc(map):
    castigator = verifStareCastig(map)
    if castigator == 1:
        return 1
    elif castigator == 2:
        return 2
    elif castigator == 0 and len(availablePositions(map)) == 0:
        return 3
    return 0

def minmax(map, depth, computer):
    stopJoc = statusJoc(map)
    if stopJoc != 0:  # cineva a castigat
        return giveScoreForComputer(stopJoc)-depth

    if computer:  # maximizez pentru calculator
        bestVal = -numpy.inf
        emptySpots = availablePositions(map)
        for (x, y) in emptySpots:
            map[x][y] = 2
            val = minmax(map, depth + 1, False)
            bestVal = max(bestVal, val)
            map[x][y] = 0
    else:  # minimizez pentru player
        bestVal = numpy.inf
        emptySpots = availablePositions(map)
        for (x, y) in emptySpots:
            map[x][y] = 1
            val = minmax(map, depth + 1, True)
            bestVal = min(bestVal, val)
            map[x][y] = 0
    return bestVal-depth

def findBestMove(map):
    bestval=-1000
    bestmove=(-1,-1)

    emptySpaces=availablePositions(map)
    for (x,y)in emptySpaces:
        map[x][y]=2
        res=minmax(map,0,True)
        map[x][y]=0
        if res>bestval:
            bestval=res
            bestmove=(x,y)
    (a,b)=bestmove
    return a*3+b
def generateMap():
    pygame.init()
    displayWidth = 800
    displayHeight = 600

    mainDisplay = pygame.display.set_mode((displayWidth, displayHeight))
    pygame.display.set_caption('Tic Tac Toe')

    clock = pygame.time.Clock()
    crashed = False

    grey = (107, 107, 107)
    faintGreen = (80, 179, 82)

    redSquare = pygame.image.load('redSquare.png').convert()
    x = pygame.image.load('x.png').convert()
    z = pygame.image.load('0.png').convert()
    # print(redSquare.get_width(),redSquare.get_height())
    cellHeight = (displayHeight * 0.8) / 3
    cellWidth = ((displayWidth * 0.75) * 0.7) / 3
    pygame.transform.scale(redSquare, (cellHeight, cellWidth))
    pygame.transform.scale(x, (cellHeight, cellWidth))
    pygame.transform.scale(z, (cellHeight, cellWidth))
    # print(redSquare.get_width(),redSquare.get_height())

    boxes = addClickBoxes(displayWidth, displayHeight)
    imagesToDisplay = []
    clickedInThePast = []
    turn = 1
    map = [[0, 0, 0],
           [0, 0, 0],
           [0, 0, 0]]
    stopJoc = 0
    score = 0
    responseBoxes = []
    waitForAnswer = 0
    justRestarted = 0
    while not crashed:
        justRestarted = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and stopJoc == 0 and turn % 2 == 1:
                    count = 0
                    for box in boxes:
                        if box.collidepoint(event.pos):
                            if box not in clickedInThePast:
                                rect = redSquare.get_rect()
                                rect.width = box.width
                                rect.height = box.height
                                rect.center = box.center
                                imagesToDisplay.append((rect, 1))
                                map[count // 3][count % 3] = 1
                                turn += 1
                                stopJoc = cautCastigator(map)
                                clickedInThePast.append(box)
                        count += 1
            if event.type == pygame.MOUSEBUTTONDOWN and stopJoc == 3:
                if event.button == 1:
                    count = 1
                    for box in responseBoxes:
                        if box.collidepoint(event.pos):
                            if count == 1:
                                print("O noua runda incepe!")
                                map = [[0, 0, 0],
                                       [0, 0, 0],
                                       [0, 0, 0]]
                                clickedInThePast = []
                                imagesToDisplay = []
                                turn = 1
                                justRestarted = 1
                                stopJoc = 0
                            else:
                                print("Nu")
                                crashed = True
                                stopJoc = 0
                                break
                        count += 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_r:
                    print("Am dat restart la joc")
                    map = [[0, 0, 0],
                           [0, 0, 0],
                           [0, 0, 0]]
                    clickedInThePast = []
                    imagesToDisplay = []
                    turn = 1
                    justRestarted = 1
                    score = 0
                    stopJoc = 0
                    responseBoxes = []
        if turn % 2 == 0 and turn <= 8 and stopJoc == 0 and justRestarted == 0:
            # spot = randomSelect(map)  # pune random
            # spot = semiRandomSelect(map)  # pune random1/2 istet 1/2
            # spot = optimalSelect(map)  # pune istet(facut de mine)

            spot=findBestMove(map)#pune istet (minmax)

            print(spot)
            rect = addZero(boxes, map, spot, imagesToDisplay, redSquare, clickedInThePast)
            turn += 1
            stopJoc = cautCastigator(map)

        mainDisplay.fill(grey)
        if stopJoc == 1:
            score += 100
            stopJoc = 3
        if stopJoc == 2:
            score -= 50
            stopJoc = 3
        if stopJoc == 3:
            responseBoxes = displayPlayAgain(mainDisplay, displayWidth, displayHeight)

        displayScore(score, mainDisplay, displayWidth, displayHeight)
        drawLines(mainDisplay, faintGreen, displayWidth, displayHeight, 5)
        for (image, imageType) in imagesToDisplay:
            if imageType == 1:
                imgX = pygame.transform.scale(x, (image.width, image.height))
                mainDisplay.blit(imgX, image)
            else:
                imgZero = pygame.transform.scale(z, (image.width, image.height))
                mainDisplay.blit(imgZero, image)

        # if stopJoc != 0:
        #     waitForAnswer = 1
        # if waitForAnswer == 1:
        #     count = 0
        #     print("Astept raspunsul")
        #     # search for click to accept next turn
        #     while waitForAnswer == 1:
        #         for event in pygame.event.get():
        #             if event.type == pygame.QUIT:
        #                 waitForAnswer = 0
        #                 crashed = True
        #             if event.type == pygame.MOUSEBUTTONDOWN:
        #                 if event.button == 1:
        #                     for box in responseBoxes:
        #                         count += 1
        #                         if box.collidepoint(event.pos):
        #                             if count == 1:  # DA
        #                                 print("Da")
        #                                 waitForAnswer = 0
        #                                 print("Am dat restart la joc")
        #                                 map = [[0, 0, 0],
        #                                        [0, 0, 0],
        #                                        [0, 0, 0]]
        #                                 clickedInThePast = []
        #                                 imagesToDisplay = []
        #                                 turn = 1
        #                                 justRestarted = 1
        #                                 waitForAnswer = 0
        #                             else:  # NU
        #                                 print("Nu")
        #                                 waitForAnswer = 0

        pygame.display.update()
        clock.tick(60)


generateMap()
