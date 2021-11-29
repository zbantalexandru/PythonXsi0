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
           pygame.Rect(mapHeight / 3 + leftMargin, topMargin, mapWidth / 3, mapHeight / 3),
           pygame.Rect(mapHeight * 2 / 3 + leftMargin, topMargin, mapWidth / 3, mapHeight / 3),
           pygame.Rect(leftMargin, mapHeight / 3 + topMargin, mapWidth / 3, mapHeight / 3),
           pygame.Rect(mapHeight / 3 + leftMargin, mapHeight / 3 + topMargin, mapWidth / 3, mapHeight / 3),
           pygame.Rect(mapHeight * 2 / 3 + leftMargin, mapHeight / 3 + topMargin, mapWidth / 3, mapHeight / 3),
           pygame.Rect(leftMargin, mapHeight * 2 / 3 + topMargin, mapWidth / 3, mapHeight / 3),
           pygame.Rect(mapHeight / 3 + leftMargin, mapHeight * 2 / 3 + topMargin, mapWidth / 3, mapHeight / 3),
           pygame.Rect(mapHeight * 2 / 3 + leftMargin, mapHeight * 2 / 3 + topMargin, mapWidth / 3, mapHeight / 3)]
    return res


# def selectSpot(poz,boxes):

def generateMap():
    pygame.init()
    displayWidth = 400
    displayHeight = 600

    mainDisplay = pygame.display.set_mode((displayWidth, displayHeight))
    pygame.display.set_caption('Tic Tac Toe')

    clock = pygame.time.Clock()
    crashed = False

    grey = (107, 107, 107)
    faintGreen = (80, 179, 82)

    redSquare = pygame.image.load('redSquare.png')
    cellHeight = (displayHeight * 0.8) / 3
    cellWidth = ((displayWidth * 0.75) * 0.7) / 3
    pygame.transform.scale(redSquare, (cellHeight, cellWidth))

    boxes = addClickBoxes(displayWidth, displayHeight)
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    count = 0
                    for box in boxes:
                        count += 1
                        if box.collidepoint(event.pos):
                            #     selectSpot(count,boxes)

                            print("am dat click in casuta ", count)

        mainDisplay.fill(grey)

        drawLines(mainDisplay, faintGreen, displayWidth, displayHeight, 5)
        mainDisplay.blit(redSquare, (100, 100))
        pygame.display.update()
        clock.tick(60)


generateMap()
