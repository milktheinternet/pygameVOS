from vos import *
from math import *

class MyApp(NodeApp):
    def __init__(self, vos):
        super().__init__(vos, "Calculator", res = (400, 600))
        self.init_res = self.res
        self.fs = False
        self.vos.input.text = ""
        self.resizeable = True
        self.expression = ""

    def on_run(self):
        super().on_run()
        self.setup_nodes()
        self.reset()
        self.update_exp()

    def resize(self, res=None):
        super().resize(res)
        self.setup_nodes()
        self.update_exp()
        

    def fullscreen(self):
        self.fs = not self.fs
        self.resize(self.vos.res if self.fs else self.init_res)

    def setup_nodes(self, expression_height = 35, font_size = 30, margin = 5):

        self.children = []

        self.font = self.vos.load_font(size=font_size)
        
        W, H = self.res
        EXP_H = expression_height
        
        self.expression_node = TextNode(self, size=(W, EXP_H), text = "ANSWER HERE", font = self.font)
        self.add(self.expression_node)
        
        button_data = {
            "(":lambda:self.type("("),
            ")":lambda:self.type(")"),
            "C":lambda:self.reset(),
            "<-":lambda:self.backspace(),
            
            "7":lambda:self.type("7"),
            "8":lambda:self.type("8"),
            "9":lambda:self.type("9"),
            "+":lambda:self.type("+"),
            
            "4":lambda:self.type("4"),
            "5":lambda:self.type("5"),
            "6":lambda:self.type("6"),
            "/":lambda:self.type("/"),
            
            "1":lambda:self.type("1"),
            "2":lambda:self.type("2"),
            "3":lambda:self.type("3"),
            "*":lambda:self.type("*"),
            
            ".":lambda:self.type("."),
            "0":lambda:self.type("0"),
            "-":lambda:self.type("-"),
            "=":lambda:self.solve(),

            "FS":self.fullscreen,
            }
        self.btns_per_row = 4
        BTN_W = W//self.btns_per_row
        BTN_H = (H - EXP_H)/ceil(len(button_data)/self.btns_per_row)

        x, y = 0, EXP_H
        for text, on_press in button_data.items():
            btn = ButtonNode(self, size=(BTN_W-margin, BTN_H-margin), pos=(x+margin//2, y+margin//2), text=text, on_press=on_press, center=True, font = self.font)
            self.add(btn)
            x += BTN_W
            if x >= W:
                x = 0
                y += BTN_H

    def solve(self):
        try:
            solved = eval(self.expression)
            if int(solved) == solved:
                solved = int(solved)
            else:
                solved = round(solved, 10)
            self.expression = str(solved)
            self.update_exp()
        except:
            self.expression = "ERR"
            self.update_exp()

    def backspace(self):
        if self.expression:
            self.expression = self.expression[:-1]
        self.update_exp()

    def reset(self):
        self.expression = ""
        self.update_exp()
    
    def type(self, s):
        self.expression += s
        self.update_exp()

    def update_exp(self):
        self.expression_node.text = self.expression

        self.srf.fill(self.bg)
        for node in self.children:
            node.render()

    def update(self):
        super().update()
        inp = self.vos.input
        if inp.text:
            self.type(inp.text)
            inp.text = ""
        elif pg.K_BACKSPACE in inp.keys_inst:
            self.backspace()
        elif pg.K_RETURN in inp.keys_inst:
            self.solve()
