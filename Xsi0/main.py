import pygame


def drawLines(display, color, width, height, lineWidth=1):
    pygame.draw.line(display, (0, 0, 0), (width * 0.75, 0), (width * 0.75, height), 5)
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


def verifCastig(map):
    for linie in range(3):
        if map[linie][0]!=0 and map[linie][0]==map[linie][1]==map[linie][2]:
            return map[linie][0]

    for coloana in range(3):
        if map[0][coloana] != 0 and map[0][coloana]==map[1][coloana]==map[2][coloana]:
            return map[0][coloana]

    if map[0][0] == map[1][1] == map[2][2] and map[0][0] != 0:
        return map[0][0]
    if map[0][2] == map[1][1] == map[2][0] and map[0][2] != 0:
        return map[0][2]
    return 0


# def selectSpot(poz,boxes):

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
    winnerFound=0
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and winnerFound==0:
                    count = 0
                    for box in boxes:
                        if box.collidepoint(event.pos):
                            if box not in clickedInThePast:
                                rect = redSquare.get_rect()
                                rect.width = box.width
                                rect.height = box.height
                                rect.center = box.center
                                if turn % 2 == 1:
                                    imagesToDisplay.append((rect, 1))
                                    map[count // 3][count % 3] = 1
                                else:
                                    imagesToDisplay.append((rect, 2))
                                    map[count // 3][count % 3] = 2
                                castigator = verifCastig(map)
                                if castigator == 1:
                                    print("Jucatorul a castigat!")
                                    winnerFound=1
                                elif castigator == 2:
                                    print("Calculatorul a castigat!")
                                    winnerFound = 1
                                elif castigator == 0 and turn >= 9:
                                    print("Remiza!")
                                    winnerFound = 1
                                turn += 1
                                clickedInThePast.append(box)
                        count += 1

        mainDisplay.fill(grey)

        drawLines(mainDisplay, faintGreen, displayWidth, displayHeight, 5)
        for (image, imageType) in imagesToDisplay:
            if imageType == 1:
                imgX = pygame.transform.scale(x, (image.width, image.height))
                mainDisplay.blit(imgX, image)
            else:
                imgZero = pygame.transform.scale(z, (image.width, image.height))
                mainDisplay.blit(imgZero, image)
        pygame.display.update()
        clock.tick(60)


generateMap()
