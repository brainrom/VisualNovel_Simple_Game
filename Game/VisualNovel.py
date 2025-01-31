import pygame
from pygame import mixer

# Классы для визуальной реализации игры. Не считаются основными.
class ButtonClassic:
    def __init__(self, screen, x, y, width, height, buttonText, font, size, color):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = pygame.font.Font(font, size)
        self.__fillColors = {
            'normal': '#1a1a1a',
            'hover': '#333333',
            'pressed': '#000000',
        }
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.buttonSurf = self.font.render(buttonText, True, color)
        self._clicked = False 

    def draw(self):
        action = False
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.__fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.__fillColors['hover'])
            if pygame.mouse.get_pressed()[0] == 1:
                self.buttonSurface.fill(self.__fillColors['pressed'])
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        self.screen.blit(self.buttonSurface, self.buttonRect)
        return action

class ButtonImage:
    def __init__(self, screen, x, y, width, height, image_path, image_path_hover, scale):
        self.screen = screen
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(pygame.image.load(image_path), (int(width * scale), int(height * scale)))
        self.image_hover = pygame.transform.scale(pygame.image.load(image_path_hover), (int(width * scale), int(height * scale)))
        self.buff_image = self.image
        self.__rect = self.image.get_rect()
        self.__rect.topleft = (x, y)
        self._clicked = False

    def draw(self):
        action = False
        mousePos = pygame.mouse.get_pos()
        if self.__rect.collidepoint(mousePos):
            self.image = self.image_hover
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        else:
            self.image = self.buff_image
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        self.screen.blit(self.image, (self.__rect.x, self.__rect.y))
        return action

class Label:
    def __init__(self, screen,  x, y, text, font, size, color):
        self.screen = screen
        self.x = x
        self.y = y
        self.text = text
        self.font = pygame.font.Font(font, size)
        self.color = color

    def draw(self):
        text_surface = self.font.render(self.text, True, self.color)
        self.screen.blit(text_surface, (self.x, self.y))

class WrappedLabel:
    def __init__(self, screen,  x, y, w, h, text, font, size, color):
        self.screen = screen
        self.rect = pygame.Rect(x,y,w,h)
        self.text = text
        self.font = pygame.font.Font(font, size)
        self.color = color

    def draw(self): # Wrapping logic are mainly taken from https://www.pygame.org/wiki/TextWrap
        text = self.text
        rect = self.rect
        y = rect.top
        lineSpacing = -2
        fontHeight = self.font.size("Tg")[1]

        while text:
            i = 1
            # determine if the row of text will be outside our area
            if y + fontHeight>rect.bottom:
                break
            # determine maximum width of line
            while self.font.size(text[:i])[0]<rect.width and i<len(text):
                i += 1
            # if we've wrapped the text, then adjust the wrap to the last word
            if i<len(text):
                i = text.rfind(" ", 0, i) + 1
            # render the line and blit it to the surface
            image = self.font.render(text[:i], True, self.color)

            self.screen.blit(image, (rect.left, y))
            y += fontHeight + lineSpacing
            # remove the text we just blitted
            text = text[i:]

class MyRectangle:
    def __init__(self, screen, x, y, width, height, color_text, color_r, text, font, size):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color_rect = color_r
        self.font = pygame.font.Font(font, size)
        self.Surface = pygame.Surface((self.width, self.height))
        self.Rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.Surf = self.font.render(text, True, color_text)

    def draw(self):
        self.Surface.fill(self.color_rect)
        self.Surface.blit(self.Surf, [
            self.Rect.width/2 - self.Surf.get_rect().width/2,
            self.Rect.height/2 - self.Surf.get_rect().height/2
        ])
        self.screen.blit(self.Surface, self.Rect)

class Music: # класс для "загрузки", вкл и выкл музыки в игре
    def __init__(self):
        self.dict_music = {}

    def addMusic(self, key, path):
        self.dict_music[key] = path

    def getMusic(self, key):
        return self.dict_music[key]

    def Play(self, path, music_volums, volume, how_long):
        mixer.music.load(path)
        mixer.music.set_volume(music_volums[volume])
        mixer.music.play(how_long)
    def Pause(self):
        mixer.music.pause()
    def Unpause(self):
        mixer.music.unpause()

class Sprites: # класс для "загрузки" картинок в игре
    def __init__(self):
        self.dict_sprites = {}

    def addSprite(self, key, path):
        self.dict_sprites[key] = path

    def getSprite(self, key):
        return self.dict_sprites.get(key)
    
class LoadFile: # класс для чтения текста из файлов
    def __init__(self, path):
        self.file_path = path
    
    def load_file(self):
        f = open(self.file_path, "r", encoding="utf-8")
        textList = []
        for i in f.readlines():
            if i.find(": ") != -1:
                str_line = i.split(": ")
                textList.append(str_line)
            else:
                str_line = i.split(" ")
                textList.append(str_line)
        f.close()
        return textList     
        
class Programm: # основной класс с информацией по игре и инициализирующий необходимые материалы (музыка, картинки)
    def __init__(self, m_vol, m_on):
        self._WIDTH = 1920
        self._HEIGHT = 1080
        self.SCREEN = pygame.display.set_mode((self._WIDTH, self._HEIGHT), pygame.FULLSCREEN)
        self.__TITLE_WIN = "Murder on the Orient Express"
        self._TITLE_GAME = "         Убийство в \n«Восточном экспрессе»"
        self._MINI_TITLE_GAME = "   по одноименному роману\n            Агаты Кристи"
        self._FONT = "images/font/Jost-Light.ttf"
        self._color_font = (255, 215, 0)
        self._MUSIC = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        self._MUSIC_I = m_vol 
        self._MUSIC_ON = m_on
        self.sprites = Sprites()
        self.music = Music()

        self._book_repos = "book"

        self.sprites.addSprite("main_menu_bg", "images/backgrounds/main_bg.png")
        self.sprites.addSprite("main_menu", "images/system/main_menu.png")
        self.sprites.addSprite("settings", "images/system/game_menu.png")
        self.sprites.addSprite("btn_left_normal", "images/button/page_button_left_idle.png")
        self.sprites.addSprite("btn_left_hover", "images/button/page_button_left_hover.png")
        self.sprites.addSprite("btn_right_normal", "images/button/page_button_right_idle.png")
        self.sprites.addSprite("btn_right_hover", "images/button/page_button_right_hover.png")
        self.sprites.addSprite("choice_normal", "images/button/choice_idle_background.png")
        self.sprites.addSprite("choice_hover", "images/button/choice_hover_background.png")
        self.sprites.addSprite("frame", "images/system/frame.png")
        self.sprites.addSprite("divider_up", "images/system/dividerUp.png")
        self.sprites.addSprite("divider_down", "images/system/dividerDown.png")
        self.sprites.addSprite("namebox", "images/system/namebox.png")

        self.sprites.addSprite("railway_station", "images/backgrounds/railway.png")
        self.sprites.addSprite("restaurant", "images/backgrounds/restaurant.png")
        self.sprites.addSprite("restaurant2", "images/backgrounds/restaurant2.png")
        self.sprites.addSprite("train1", "images/backgrounds/train1.png")
        self.sprites.addSprite("train2", "images/backgrounds/train2.png")
        self.sprites.addSprite("train3", "images/backgrounds/train3.png")
        self.sprites.addSprite("train4", "images/backgrounds/train4.png")
        self.sprites.addSprite("train5", "images/backgrounds/train5.png")
        self.sprites.addSprite("universe", "images/backgrounds/uni.png")
        self.sprites.addSprite("hotel", "images/backgrounds/hotel_rest.png")

        self.sprites.addSprite("Пуаро", "Characters/Puaro.png")
        self.sprites.addSprite("Доктор Константин", "Characters/test_man.png")
        self.sprites.addSprite("Бук", "Characters/test_man.png")
        self.sprites.addSprite("Дебенхэм", "Characters/test_woman.png")
        self.sprites.addSprite("Арбэтнот", "Characters/test_man.png")
        self.sprites.addSprite("Маккуин", "Characters/test_man.png")
        self.sprites.addSprite("Фоскарелли", "Characters/test_man.png")
        self.sprites.addSprite("Рэтчетт", "Characters/test_man.png")
        self.sprites.addSprite("Мастермэн", "Characters/test_man.png")
        self.sprites.addSprite("Мишель", "Characters/test_man.png")
        self.sprites.addSprite("Княгиня Драгомирова", "Characters/test_woman.png")
        self.sprites.addSprite("Шмидт", "Characters/test_woman.png")
        self.sprites.addSprite("Граф Андрени", "Characters/test_man.png")
        self.sprites.addSprite("Графиня Андрени", "Characters/test_woman.png")
        self.sprites.addSprite("Ольсон", "Characters/test_woman.png")
        self.sprites.addSprite("Миссис Хаббард", "Characters/test_woman.png")
        self.sprites.addSprite("Хардман", "Characters/test_man.png")
        
        self.music.addMusic("main_music", "music/Night on the Docks - Trumpet.mp3")
        self.music.addMusic("railway_ambient", "music/railway.mp3")
        self.music.addMusic("backbay", "music/Backbay Lounge.mp3")
        self.music.addMusic("just_soon", "music/Just As Soon.mp3")
        self.music.addMusic("restaurant_ambient", "music/restaurant_ambient.mp3")
        self.music.addMusic("boiled", "music/Hard Boiled.mp3")
        self.music.addMusic("cool_side", "music/On the Cool Side.mp3")
        self.music.addMusic("walking", "music/Walking Along.mp3")
        self.music.addMusic("ground", "music/On the Ground.mp3")
        self.music.addMusic("vibes", "music/Cool Vibes.mp3")
                
    def main(self): #вызов главного меню игры (начальное окно)
        pygame.init()
        pygame.display.set_caption(self.__TITLE_WIN)

        menu = Menu(self.music.getMusic("main_music"), self.sprites.getSprite("main_menu_bg"), 
                            self.sprites.getSprite("main_menu"), self.sprites.getSprite("settings"), 
                            self.sprites.getSprite("btn_left_normal"), self.sprites.getSprite("btn_left_hover"), 
                            self.sprites.getSprite("btn_right_normal"), self.sprites.getSprite("btn_right_hover"))
        menu.MainMenu(self._MUSIC, self._MUSIC_I, self._MUSIC_ON)

class Scenes(Programm): # основной класс реализующий главную часть игры. Показывает титульные сцены, сновные сцены, сцены выбора, обрабатывает текст, прочитаный в классе LoadFile
    def __init__(self, m_vol, m_on):
        Programm.__init__(self, m_vol, m_on)

    def TitleScene(self, part, chap, frame, divider, text_x, text_y):
        self.SCREEN.fill(0)
        frame = pygame.transform.scale(pygame.image.load(frame).convert_alpha(), (int(self._WIDTH * 0.5), int(self._HEIGHT * 0.3)))
        divider = pygame.transform.scale(pygame.image.load(divider).convert_alpha(), (int(self._WIDTH * 0.2), int(self._HEIGHT * 0.03)))
        self.SCREEN.blit(frame, (self._WIDTH//2-470, 150))
        self.SCREEN.blit(divider, (self._WIDTH//2-200, 165))

        label_Part = Label(self.SCREEN, self._WIDTH//2-150, 200, part, self._FONT, 35, self._color_font)
        label_Chapter = Label(self.SCREEN, text_x, text_y, chap, self._FONT, 25, self._color_font)
        label_tip = Label(self.SCREEN, self._WIDTH//2-150, self._HEIGHT-100, "Нажмите ENTER, чтобы продолжить", self._FONT, 20, self._color_font)
        label_Part.draw()
        label_Chapter.draw()
        label_tip.draw()

        run = True
        while run:
            for i in pygame.event.get():
                if pygame.key.get_pressed()[pygame.K_RETURN] == 1:
                    run = False
                if i.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    exit()
            pygame.display.update()

    def MiniTitleScene(self, chap, frame, divider, text_x, text_y):
        frame = pygame.transform.scale(pygame.image.load(frame).convert_alpha(), (int(self._WIDTH * 0.5), int(self._HEIGHT * 0.3)))
        divider = pygame.transform.scale(pygame.image.load(divider).convert_alpha(), (int(self._WIDTH * 0.2), int(self._HEIGHT * 0.03)))
        self.SCREEN.blit(frame, (self._WIDTH//2-470, 150))
        self.SCREEN.blit(divider, (self._WIDTH//2-200, 165))

        label_Chapter = Label(self.SCREEN, text_x, text_y, chap, self._FONT, 25, self._color_font)
        label_Chapter.draw()
        label_tip = Label(self.SCREEN, self._WIDTH//2-150, self._HEIGHT-100, "Нажмите ENTER, чтобы продолжить", self._FONT, 20, self._color_font)
        label_tip.draw()

        run = True
        while run:
            for i in pygame.event.get():
                if pygame.key.get_pressed()[pygame.K_RETURN] == 1:
                    run = False
                if i.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    exit()
            pygame.display.update()

    def ChoiceBtn(self, text, bg):
        btn_choice1 = ButtonClassic(self.SCREEN, self._WIDTH//2-340, 200, 700, 60, " ".join(text[1].split("_")), self._FONT, 24, self._color_font)
        btn_choice2 = ButtonClassic(self.SCREEN, self._WIDTH//2-340, 280, 700, 60, " ".join(text[3].split("_")), self._FONT, 24, self._color_font)

        run = True
        while run:
            for j in pygame.event.get():
                if btn_choice1.draw():
                    with open(text[2], "r", encoding="utf-8") as f:
                        choice = f.readlines()
                        for g in range(len(choice)):
                            str_line = choice[g].split(": ")
                            if str_line[0].find("Выбор") != -1:
                                str_line = str_line[0].split(" ")
                                self.ChoiceBtn(str_line, bg)
                            else: 
                                self.Scene(str_line, bg, self.sprites.getSprite("frame"), 
                                           self.sprites.getSprite("namebox"), self.sprites.getSprite("divider_up"), 
                                           self.sprites.getSprite("divider_down"))
                    run = False
                            
                if btn_choice2.draw():
                    with open(text[4][:len(text[4])-1], "r", encoding="utf-8") as f:
                        choice = f.readlines()
                        for g in range(len(choice)):
                            str_line = choice[g].split(": ")
                            if str_line[0].find("Выбор") != -1:
                                str_line = str_line[0].split(" ")
                                self.ChoiceBtn(str_line, bg)
                            else: 
                                self.Scene(str_line, bg, self.sprites.getSprite("frame"), 
                                           self.sprites.getSprite("namebox"), self.sprites.getSprite("divider_up"), 
                                           self.sprites.getSprite("divider_down"))
                    run = False

                if j.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    exit()
                pygame.display.update()

    def Scene(self, text, bg, frame, namebox, divider_up, divider_down):
        self.SCREEN.fill(0)

        bg = pygame.transform.scale(pygame.image.load(self.sprites.getSprite(bg)).convert_alpha(), (self._WIDTH, self._HEIGHT))
        self.SCREEN.blit(bg, (0, 0))
        divUp = pygame.transform.scale(pygame.image.load(divider_up).convert_alpha(), (int(self._WIDTH * 0.2), int(self._HEIGHT * 0.03)))
        divDown = pygame.transform.scale(pygame.image.load(divider_down).convert_alpha(), (int(self._WIDTH * 0.2), int(self._HEIGHT * 0.03)))
        textFrame = pygame.transform.scale(pygame.image.load(frame).convert_alpha(), (int(self._WIDTH * 0.9), int(self._HEIGHT * 0.3)))

        btnExit = ButtonClassic(self.SCREEN, 10, 20, 180, 60, "Выйти", self._FONT, 20, self._color_font)

        name = text[0]
        words = text[1]
        
        if name == "Рассказчик":
            self.SCREEN.blit(textFrame, (100, self._HEIGHT-350))
            self.SCREEN.blit(divUp, (self._WIDTH//2-200, self._HEIGHT-330))
            self.SCREEN.blit(divDown, (self._WIDTH//2-200, self._HEIGHT-75))
            label_text = WrappedLabel(self.SCREEN, 190, self._HEIGHT-270, textFrame.get_width()-180, textFrame.get_height(), words, self._FONT, 26, self._color_font)
            label_text.draw()
        else:
            if self.sprites.getSprite(name) != None:
                character = pygame.transform.scale(pygame.image.load(self.sprites.getSprite(name)), (int(self._WIDTH * 0.3), int(self._HEIGHT * 1.0)))
                self.SCREEN.blit(character, (self._WIDTH//2-200, 10))
            self.SCREEN.blit(textFrame, (100, self._HEIGHT-350))
            self.SCREEN.blit(divUp, (self._WIDTH//2-200, self._HEIGHT-330))
            self.SCREEN.blit(divDown, (self._WIDTH//2-200, self._HEIGHT-75))
            namebox = pygame.transform.scale(pygame.image.load(namebox).convert_alpha(), (int(self._WIDTH * 0.35), int(self._HEIGHT * 0.08)))
            self.SCREEN.blit(namebox, (-30, self._HEIGHT//2+180))
        
            label_name = Label(self.SCREEN, 180, self._HEIGHT//2+200, name, self._FONT, 35, self._color_font)
            label_name.draw()
            label_text = WrappedLabel(self.SCREEN, 190, self._HEIGHT-260, textFrame.get_width()-90, textFrame.get_height(), words, self._FONT, 26, self._color_font)
            label_text.draw()

        run = True
        while run:
            for i in pygame.event.get():
                if pygame.key.get_pressed()[pygame.K_RETURN] == 1:
                    run = False
                
                if btnExit.draw():
                    run = False
                    pygame.quit()
                    exit()

                if i.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    exit()
            pygame.display.update()

    def systemScene(self, text, text_x, text_y, frame, namebox, divider_up, divider_down):
        self.SCREEN.fill(0)
        if (text[0][0] == "Заголовок") and (text[1][0] == "Подзаголовок"):
            self.TitleScene(text[0][1], text[1][1], frame, divider_up, text_x, text_y)
            mus = self.music.getMusic(text[2][1])
            bg = text[2][3][0:len(text[2][3])-1]
            
            if self._MUSIC_ON == "Вкл":
                self.music.Play(mus, self._MUSIC, self._MUSIC_I, -1)
            for i in range(3, len(text)):
                if text[i][0] == "Музыка":
                    mus = self.music.getMusic(text[i][1])
                    if self._MUSIC_ON == "Вкл":
                        self.music.Play(mus, self._MUSIC, self._MUSIC_I, -1)
                    bg = text[i][3][0:len(text[i][3])-1]
                elif text[i][0] == "Выбор":
                    self.ChoiceBtn(text[i], bg)
                else:
                    self.Scene(text[i], bg, frame, namebox, divider_up, divider_down)
        elif text[0][0] == "Подзаголовок":
            self.MiniTitleScene(text[0][1], frame, divider_up, text_x, text_y)

            mus = self.music.getMusic(text[1][1])
            bg = text[1][3][0:len(text[1][3])-1]
            
            if self._MUSIC_ON == "Вкл":
                self.music.Play(mus, self._MUSIC, self._MUSIC_I, -1)
            for i in range(2, len(text)):
                if text[i][0] == "Музыка":
                    mus = self.music.getMusic(text[i][1])
                    if self._MUSIC_ON == "Вкл":
                        self.music.Play(mus, self._MUSIC, self._MUSIC_I, -1)
                    bg = text[i][3][0:len(text[i][3])-1]
                elif text[i][0] == "Выбор":
                    self.ChoiceBtn(text[i], bg)
                else:
                    self.Scene(text[i], bg, frame, namebox, divider_up, divider_down)

class Game(Programm): # основной класс, обращающийся к методу класса LoadFile и запускающий главы по очереди, после последней главы запускает сцену конца и завершает работу программы
    def __init__(self, m_vol, m_on):
        Programm.__init__(self, m_vol, m_on)
        self.scene = Scenes(m_vol, m_on)

    def START(self):
        PartOne_ChapOne = LoadFile(self._book_repos+"/Part1/Chap1/Part1_Chap1.txt").load_file()
        PartOne_ChapTwo = LoadFile(self._book_repos+"/Part1/Chap2/Part1_Chap2.txt").load_file()
        PartOne_ChapThree = LoadFile(self._book_repos+"/Part1/Chap3/Part1_Chap3.txt").load_file()
        PartOne_ChapFour = LoadFile(self._book_repos+"/Part1/Chap4/Part1_Chap4.txt").load_file()
        PartOne_ChapFive = LoadFile(self._book_repos+"/Part1/Chap5/Part1_Chap5.txt").load_file()
        PartOne_ChapSix = LoadFile(self._book_repos+"/Part1/Chap6/Part1_Chap6.txt").load_file()
        PartOne_ChapSeven = LoadFile(self._book_repos+"/Part1/Chap7/Part1_Chap7.txt").load_file()
        
        self.scene.systemScene(PartOne_ChapOne, self._WIDTH//2-255, 250, self.sprites.getSprite("frame"), 
                         self.sprites.getSprite("namebox"), self.sprites.getSprite("divider_up"), self.sprites.getSprite("divider_down"))
        self.scene.systemScene(PartOne_ChapTwo, self._WIDTH//2-160, 250, self.sprites.getSprite("frame"), 
                         self.sprites.getSprite("namebox"), self.sprites.getSprite("divider_up"), self.sprites.getSprite("divider_down"))
        self.scene.systemScene(PartOne_ChapThree, self._WIDTH//2-210, 230, self.sprites.getSprite("frame"), 
                         self.sprites.getSprite("namebox"), self.sprites.getSprite("divider_up"), self.sprites.getSprite("divider_down"))
        self.scene.systemScene(PartOne_ChapFour, self._WIDTH//2-100, 230, self.sprites.getSprite("frame"), 
                         self.sprites.getSprite("namebox"), self.sprites.getSprite("divider_up"), self.sprites.getSprite("divider_down"))
        self.scene.systemScene(PartOne_ChapFive, self._WIDTH//2-105, 230, self.sprites.getSprite("frame"), 
                         self.sprites.getSprite("namebox"), self.sprites.getSprite("divider_up"), self.sprites.getSprite("divider_down"))
        self.scene.systemScene(PartOne_ChapSix, self._WIDTH//2-140, 230, self.sprites.getSprite("frame"), 
                         self.sprites.getSprite("namebox"), self.sprites.getSprite("divider_up"), self.sprites.getSprite("divider_down"))
        self.scene.systemScene(PartOne_ChapSeven, self._WIDTH//2-70, 230, self.sprites.getSprite("frame"), 
                         self.sprites.getSprite("namebox"), self.sprites.getSprite("divider_up"), self.sprites.getSprite("divider_down"))
        
        self.END()

    def END(self):
        self.SCREEN.fill(0)
        frame = pygame.transform.scale(pygame.image.load(self.sprites.getSprite("frame")).convert_alpha(), (int(self._WIDTH * 0.5), int(self._HEIGHT * 0.3)))
        divider = pygame.transform.scale(pygame.image.load(self.sprites.getSprite("divider_up")).convert_alpha(), (int(self._WIDTH * 0.2), int(self._HEIGHT * 0.03)))
        self.SCREEN.blit(frame, (self._WIDTH//2-320, 150))
        self.SCREEN.blit(divider, (self._WIDTH//2-135, 165))
        label_Chapter = Label(self.SCREEN, self._WIDTH//2-30, 230, "Конец", self._FONT, 20, self._color_font)
        label_Chapter.draw()
        label_tip = Label(self.SCREEN, self._WIDTH//2-60, self._HEIGHT-100, "Нажмите ENTER", self._FONT, 15, self._color_font)
        label_tip.draw()

        run = True
        while run:
            for i in pygame.event.get():
                if pygame.key.get_pressed()[pygame.K_RETURN] == 1:
                    run = False

                if i.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    exit()
            pygame.display.update()

class Menu(Programm): # главное меню игры
    def __init__(self, m_path, bg_path, mm_img_path, settings, btn_left_normal, btn_left_hover, btn_right_normal, btn_right_hover):
        Programm.__init__(self, 5, "Вкл")
        self.music_path = m_path
        self.background_path = bg_path
        self.main_menu_img = mm_img_path
        self.settings_path = settings
        self.btn_left_normal = btn_left_normal
        self.btn_left_hover = btn_left_hover
        self.btn_right_normal = btn_right_normal
        self.btn_right_hover = btn_right_hover

        self.m_on = "Вкл"
        self.m_vol = 5

    def MainMenu(self, music_vols, m_vol, m_on):
        if m_on != "Выкл":
            self.music.Play(self.music_path, music_vols, m_vol, -1)
        background = pygame.transform.scale(pygame.image.load(self.background_path).convert_alpha(), (self._WIDTH, self._HEIGHT))
        main = pygame.transform.scale(pygame.image.load(self.main_menu_img), (self._WIDTH, self._HEIGHT))
        self.SCREEN.blit(background, (0, 0))
        self.SCREEN.blit(main, (0, 0))

        labelTitle = Label(self.SCREEN, 300, 120, self._TITLE_GAME, self._FONT, 40, self._color_font)
        labelMini = Label(self.SCREEN, 325, 230, self._MINI_TITLE_GAME, self._FONT, 25, self._color_font)
        btn_start = ButtonClassic(self.SCREEN, 310, 435, 280, 60, "Начать игру", self._FONT, 30, self._color_font)
        btn_settings = ButtonClassic(self.SCREEN, 310, self._HEIGHT//2+65, 280, 60, "Настройки", self._FONT, 30, self._color_font)

        btn_exit = ButtonClassic(self.SCREEN, 310, self._HEIGHT-300, 280, 60, "Выйти", self._FONT, 30, self._color_font)

        labelTitle.draw()
        labelMini.draw()

        run = True
        while run:

            if btn_start.draw():
                self.music.Pause()
                run = False
                Game(self.m_vol, self.m_on).START()
                
            if btn_settings.draw():
                run = False
                self.SETTINGS(m_on, music_vols, m_vol)
                
            if btn_exit.draw():
                run = False
                pygame.quit()
                exit()

            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    exit()
            pygame.display.update()

    def SETTINGS(self, music_on, music, m_vol): # настройки игры
        background = pygame.transform.scale(pygame.image.load(self.background_path).convert_alpha(), (self._WIDTH, self._HEIGHT))
        self.SCREEN.blit(background, (0, 0))
        settings_menu = pygame.transform.scale(pygame.image.load(self.settings_path).convert_alpha(), (self._WIDTH, self._HEIGHT))
        self.SCREEN.blit(settings_menu, (0, 0))

        labelSettings = Label(self.SCREEN, self._WIDTH//2-85, 160, "Настройки", self._FONT, 40, self._color_font)
        lableMusic_On_Off = Label(self.SCREEN, self._WIDTH//2-300, self._HEIGHT//2-100, "Вкл/Выкл музыку", self._FONT, 28, self._color_font)
        lableMusic = Label(self.SCREEN, self._WIDTH//2-300, self._HEIGHT//2, "Громкость музыки", self._FONT, 28, self._color_font)
        labelBack = Label(self.SCREEN, 200, self._HEIGHT-160, "Назад", self._FONT, 30, self._color_font)

        btn_Music_On_Off_minus = ButtonImage(self.SCREEN, self._WIDTH//2, self._HEIGHT//2-100, self._WIDTH, self._HEIGHT, self.btn_left_normal, self.btn_left_hover, 0.05)
        btn_Music_On_Off_plus = ButtonImage(self.SCREEN, self._WIDTH//2+180, self._HEIGHT//2-100, self._WIDTH, self._HEIGHT, self.btn_right_normal, self.btn_right_hover, 0.05)
        
        btn_Music_minus = ButtonImage(self.SCREEN, self._WIDTH//2, self._HEIGHT//2, self._WIDTH, self._HEIGHT, self.btn_left_normal, self.btn_left_hover, 0.05)
        btn_Music_plus = ButtonImage(self.SCREEN, self._WIDTH//2+180, self._HEIGHT//2, self._WIDTH, self._HEIGHT, self.btn_right_normal, self.btn_right_hover, 0.05)
        
        btn_back = ButtonImage(self.SCREEN, 20, self._HEIGHT-180, self._WIDTH, self._HEIGHT, self.btn_left_normal, self.btn_left_hover, 0.09)
        
        labelSettings.draw()
        lableMusic_On_Off.draw()
        lableMusic.draw()
        labelBack.draw()
        rect1 = MyRectangle(self.SCREEN, self._WIDTH//2+95, self._HEIGHT//2-100, 80, 40, self._color_font, (26, 26, 26), music_on, self._FONT, 28)
        rect1.draw()
        rect2 = MyRectangle(self.SCREEN, self._WIDTH//2+95, self._HEIGHT//2, 80, 40, self._color_font, (26, 26, 26), str(music[m_vol]), self._FONT, 28)
        rect2.draw()

        run = True
        while run:
            if btn_Music_On_Off_minus.draw():
                music_on = "Выкл"
                self.m_on = music_on
                self.music.Pause()
                rect = MyRectangle(self.SCREEN, self._WIDTH//2+90, self._HEIGHT//2-100, 80, 40, self._color_font, (26, 26, 26), music_on, self._FONT, 28)
                rect.draw()
            if btn_Music_On_Off_plus.draw():
                music_on = "Вкл"
                self.m_on = music_on
                self.music.Unpause()
                rect = MyRectangle(self.SCREEN, self._WIDTH//2+90, self._HEIGHT//2-100, 80, 40, self._color_font, (26, 26, 26), music_on, self._FONT, 28)
                rect.draw()

            if btn_Music_minus.draw():
                if m_vol > 0:
                    m_vol -= 1
                    self.m_vol = m_vol
                    mixer.music.set_volume(music[m_vol])
                    rect = MyRectangle(self.SCREEN, self._WIDTH//2+90, self._HEIGHT//2, 80, 40, (255, 215, 0), (26, 26, 26), str(music[m_vol]), self._FONT, 28)
                    rect.draw()
            if btn_Music_plus.draw():
                if m_vol < 10:
                    m_vol += 1
                    self.m_vol = m_vol
                    mixer.music.set_volume(music[m_vol])
                    rect = MyRectangle(self.SCREEN, self._WIDTH//2+90, self._HEIGHT//2, 80, 40, (255, 215, 0), (26, 26, 26), str(music[m_vol]), self._FONT, 28)
                    rect.draw()
            
            if btn_back.draw():
                run = False
                self.MainMenu(music, m_vol, music_on)

            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    exit()
            pygame.display.update()

VisualNovel = Programm(5, "Вкл") 
VisualNovel.main() # запуск игры

pygame.quit()
