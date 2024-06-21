from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "TRUE"
import pygame as pg


class Input:
    def __init__(self):
        # keys_inst is reset with every update
        # if key in keys[]
        self.keys_inst = []
        self.keys = []
        
        self.quit = False

        # to keep track of input text, you can simply set it to "" and then it will automatically update.
        self.text = ""

        self.mouse = (0,0)
        self.click_inst = False
        self.click = False

        self.on_click = []

        self.scroll = 0
        
    def update(self):
        self.scroll = 0
        self.keys_inst = []
        self.click_inst = False
        for event in pg.event.get():
            if event.type == pg.TEXTINPUT:
                self.text += event.text
                
            if event.type == pg.KEYDOWN:
                
                self.keys_inst.append(event.key)
                self.keys.append(event.key)
                
                if event.key == pg.K_BACKSPACE and self.text:
                    self.text = self.text[:-1]
            
            elif event.type == pg.KEYUP:
                if event.key in self.keys:
                    self.keys.remove(event.key)

            elif event.type == pg.MOUSEBUTTONDOWN:
                self.click_inst = True
                self.click = True
                for fun in self.on_click:
                    if fun():break

            elif event.type == pg.MOUSEBUTTONUP:
                self.click = False

            elif event.type == pg.MOUSEWHEEL:
                self.scroll = event.y
            
            elif event.type == pg.QUIT:
                self.quit = True
        self.mouse = pg.mouse.get_pos()
