import pygame, sys, csv, time

pygame.init()
windowSize = (800, 600)
screen = pygame.display.set_mode(windowSize)
pygame.display.set_caption("Post Corona")

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
GREY = (220, 220, 220)
YELLOW = (255, 255, 237)
RED = (255, 0, 0)
i = 0  #question Number
j = 0  #board tile Number


class Message():
    def __init__(self,
                 text,
                 fontSize,
                 fontStyle="arialunicodettf",
                 textColour=BLACK,
                 backgroundColour=WHITE):
        font = pygame.font.SysFont(fontStyle, fontSize)
        self.myText = font.render(text, 1, textColour, backgroundColour)
        self.width, self.height = self.myText.get_size(
        )[0], self.myText.get_size()[1]

    def blit(self, screen, pos):
        self.x = windowSize[0] // 2 - self.width // 2 if pos[
            0] == "horizontalCentre" else pos[0]
        self.y = windowSize[1] // 2 - self.height // 2 if pos[
            1] == "verticalCentre" else pos[1]
        screen.blit(self.myText, (self.x, self.y))


class Button():
    def __init__(self,
                 color,
                 text='',
                 textColour=BLACK,
                 fontSize=48,
                 width=None,
                 height=None,
                 widthScale=1):
        self.color = color
        self.text = text
        self.textColour = textColour
        self.fontSize = fontSize

        self.widthScale = widthScale
        if self.text != '':  #We want text displayed on our button
            arialFont = pygame.font.SysFont("arialunicodettf", fontSize)
            text = arialFont.render(self.text, 1, self.textColour)
            self.width, self.height = arialFont.size(self.text)
            self.width *= self.widthScale
        else:
            self.width, self.height = width, height

    def draw(self, x, y):
        self.x = x
        self.y = y

        pygame.draw.rect(screen, self.color,
                         (self.x, self.y, int(self.width), int(self.height)),
                         0)

        if self.text != '':  #We want text displayed on our button
            arialFont = pygame.font.SysFont("arialunicodettf", self.fontSize)
            text = arialFont.render(self.text, 1, self.textColour)
            screen.blit(
                text,
                (int(self.x + (self.width // 2 - text.get_width() // 2)),
                 int(self.y + (self.height // 2 - text.get_height() // 2))))

    def isMouseHover(self, mousePos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if mousePos[0] > self.x and mousePos[0] < self.x + self.width:
            if mousePos[1] > self.y and mousePos[1] < self.y + self.height:
                return True
        return False


class UserInput():
    def __init__(self,
                 x,
                 y,
                 fontSize=24,
                 numeric=False,
                 textColour=BLACK,
                 backgroundColour=WHITE):
        self.x = x
        self.y = y
        self.fontSize = fontSize
        self.numeric = numeric
        self.textColour = textColour
        self.backgroundColour = backgroundColour

    def updateSearchBox(self, searchBoxWidth, searchBoxHeight, screen, textObj,
                        screenBeforeUserInput):
        screen.blit(screenBeforeUserInput, (0, 0))
        pygame.draw.rect(screen, self.backgroundColour,
                         [self.x, self.y, searchBoxWidth, searchBoxHeight])
        screen.blit(textObj, (self.x, self.y))

    def takeUserInput(self, screen):
        screenBeforeUserInput = screen.copy()

        text = ""
        arialFont = pygame.font.SysFont("arialunicodettf", self.fontSize)
        textObj = arialFont.render(text, 1, self.textColour)

        #initial empty text field area
        searchBoxWidth, searchBoxHeight = arialFont.size(" ")
        self.updateSearchBox(searchBoxWidth, searchBoxHeight, screen, textObj,
                             screenBeforeUserInput)

        typing = True
        while typing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if ((event.unicode.isalpha()
                         or event.key == pygame.K_SPACE)
                            and not self.numeric) or event.unicode.isnumeric():
                        text += event.unicode  #add the character
                        textObj = arialFont.render(text, 1, self.textColour)

                        searchBoxWidth, searchBoxHeight = arialFont.size(text)
                        self.updateSearchBox(searchBoxWidth, searchBoxHeight,
                                             screen, textObj,
                                             screenBeforeUserInput)

                    elif event.key == pygame.K_BACKSPACE and len(
                            text
                    ) != 0:  #you can only delete if there is text to delete
                        text = text[:-1]  #delete the last character
                        textObj = arialFont.render(text, 1, self.textColour)

                        searchBoxWidth, searchBoxHeight = arialFont.size(text)
                        self.updateSearchBox(searchBoxWidth, searchBoxHeight,
                                             screen, textObj,
                                             screenBeforeUserInput)
                    elif event.key == pygame.K_RETURN:
                        typing = False
            pygame.display.update()
        return text


class Image():
    def __init__(self, filename, size=None):
        #We cannot initialise position yet because it may depend on the size of the image
        self.image = pygame.image.load(filename)

        #User has ordered manual scaling
        if size == None:  #if the size was not specified, then use the default values for size
            self.width, self.height = self.image.get_rect().size
        else:  #the file size was specified, so scale the image to the correct size
            self.width = size[0]
            self.height = size[1]
            self.image = pygame.transform.scale(self.image,
                                                (self.width, self.height))

    def blit(self, screen, pos):
        self.x = pos[0]
        self.y = pos[1]
        screen.blit(self.image, (self.x, self.y))


clock = pygame.time.Clock()


def titleScreen():
    screen.fill(GREY)
    playButton = Button(WHITE, "Play", BLUE, 40)
    playButton.draw(30, 100)

    while True:
        clock.tick(20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePosition = pygame.mouse.get_pos()
                # if user clicked on playButton
                if playButton.isMouseHover(mousePosition):
                    mainScreen()
        pygame.display.update()


coordinates = [(59, 40), (122, 171), (155, 335), (348, 333), (376, 168),
               (398, 67), (508, 77), (566, 167), (572, 263), (541, 401),
               (613, 518), (746, 516)]


def mainScreen():
    screen.fill(WHITE)
    boardImage = Image("board.png")
    boardImage.blit(screen, pos=(0, 0))

    questionButton = Button(WHITE, "New Question", RED, 40)
    questionButton.draw(200, 400)

    character = Message("Me", 24)
    character.blit(screen, coordinates[j])

    while True:
        if j > 5:
            break
        # print(pygame.mouse.get_pos())
        clock.tick(20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePosition = pygame.mouse.get_pos()
                # if user clicked on playButton
                if questionButton.isMouseHover(mousePosition):
                    questionScreen()
        pygame.display.update()

    screen.fill(WHITE)
    character = Message("Good Job", 24)
    character.blit(screen, (400, 300))


def getQuestion():
    with open("questions.csv", "r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        questions = []
        answers = []
        for line in csv_reader:
            questions.append(line["Question"])
            answers.append(line["Answer"])

    return (questions[i], answers[i])


def questionScreen():
    screen.fill((230, 230, 250))
    question, answer = getQuestion()

    questionMessage = Message(question, 24)
    questionMessage.blit(screen, ("horizontalCentre", 100))

    answerInput = UserInput(400, 300)
    userAnswer = answerInput.takeUserInput(screen)

    global i
    if userAnswer == answer:  #correct answer
        text = f"{userAnswer} is correct!"
        global j
        j += 1  #move character forward
    else:  #incorrect answer
        text = f"Oops, the correct answer is {answer}"
    i += 1  #next question

    questionMessage = Message(text, 24)
    questionMessage.blit(screen, ("horizontalCentre", 50))
    pygame.display.update()
    time.sleep(2)
    mainScreen()


if __name__ == "__main__":
    pygame.mixer.music.load('music.wav')
    pygame.mixer.music.play(-1)
    titleScreen()
