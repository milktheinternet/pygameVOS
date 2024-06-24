from vos import *
from math import floor, sqrt

class Notify(TextNode):
    def __init__(self, app, text):
        super().__init__(app, text = text, center = True, nobg = True,
                         size = (app.res[0], 50), font=app.vos.load_font(size=17))
        self.start = self.vos.time
    def update(self):
        if self.vos.time - self.start > 1000:
            self.app.children.remove(self)

class Canvas(SurfaceNode):
    def __init__(self, app, size=(600, 600), cnvsize=(32,32), cb1=(100,100,100), cb2=(120,120,120)):
        super().__init__(app, size=size)
        self.cnv = pg.Surface(cnvsize, pg.SRCALPHA)
        self.cnv.fill((0, 0, 0, 0))
        self.cnvw, self.cnvh = cnvsize

        W, H = self.size
        if self.cnvw > self.cnvh:
            cnvw, cnvh = (W, W/self.cnvw*self.cnvh)
        else:
            cnvw, cnvh = (H/self.cnvh*self.cnvw, H)

        self.cnv_size = (cnvw, cnvh)
        self.cnv_pos = (W//2-cnvw//2, H//2-cnvh//2)

        self.checkerboard = pg.Surface(cnvsize)
        self.checkerboard.fill(cb1)
        for x in range(self.cnvw):
            for y in range(self.cnvh):
                if x%2==y%2:
                    self.checkerboard.set_at((x,y), cb2)
        self.checkerboard = pg.transform.scale(self.checkerboard, self.cnv_size)

    def set_image(self, srf):
        self.cnv = srf

    def to_cnv(self, pos):
        x, y = pos
        gx, gy = self.global_pos
        cnvx, cnvy = self.cnv_pos
        x = floor((x - gx - cnvx)/self.cnv_size[0]*self.cnvw)
        y = floor((y - gy - cnvy)/self.cnv_size[1]*self.cnvh)
        return x, y

    def on_cnv(self, pos):
        x, y = pos
        return 0 <= x < self.cnvw and 0 <= y < self.cnvh

    def draw(self, color, pos, sz=1):
        sz /= 2
        x, y = self.to_cnv(pos)
        if self.on_cnv((x, y)):
            if sz >= 1: pg.draw.circle(self.cnv, color, (x, y), sz)
            else:self.cnv.set_at((x,y), color)

    def line(self, color, from_pos, to_pos, sz=1):
        self.draw(color, from_pos, sz-1 if sz <= 3 else sz)
        self.draw(color, to_pos, sz-1 if sz <= 3 else sz)
        from_pos, to_pos = self.to_cnv(from_pos), self.to_cnv(to_pos)
        pg.draw.line(self.cnv, color, from_pos, to_pos, sz)

    def circle(self, color, from_pos, to_pos, sz=1):
        sx, sy = self.to_cnv(from_pos)
        ex, ey = self.to_cnv(to_pos)
        dist = sqrt((sx-ex)**2 + (sy-ey)**2)
        pg.draw.circle(self.cnv, color, (sx, sy), round(dist), sz)

    def rect(self, color, from_pos, to_pos, sz=1):
        sx, sy = self.to_cnv(from_pos)
        ex, ey = self.to_cnv(to_pos)
        if ex < sx: sx, ex = ex, sx
        if ey < sy: sy, ey = ey, sy
        w, h = ex - sx + 1, ey - sy + 1
        if w and h:
            pg.draw.rect(self.cnv, color, (sx, sy, w, h), sz)

    def list2d(self):
        return [[self.cnv.get_at((x,y)) for y in range(self.cnvh)] for x in range(self.cnvw)]

    def fill(self, color, pos):
        list2d = self.list2d()
        x, y = self.to_cnv(pos)
        if not self.on_cnv((x, y)):
            return
        target = list2d[x][y]

        if target == color:
            return

        stack = [(x, y)]

        while stack:
            x, y = stack.pop()
            if not self.on_cnv((x, y)):
                continue
            if list2d[x][y] == target:
                self.cnv.set_at((x, y), color)
                list2d[x][y] = color
                for xm, ym in ((-1, 0), (1, 0), (0, 1), (0, -1)):
                    stack.append((x + xm, y + ym))

    def render(self):
        self.srf.blit(self.checkerboard, self.cnv_pos)
        self.srf.blit(pg.transform.scale(self.cnv, self.cnv_size), self.cnv_pos)
        super().render()

class MyApp(NodeApp):
    def __init__(self, vos):
        super().__init__(vos, "Pixel Art", (800, 600))

        self.init_res = self.res
        self.fs = False
        
        self.bg = (10, 10, 10)
        self.bg2 = (33, 33, 33)
        self.color = (200,200,200)
        self.font = self.vos.load_font(size=17)

        self.draw_color = (0,0,0,255)

        self.TOOL_DRAW, self.TOOL_FILL, self.TOOL_LINE, self.TOOL_RECT, self.TOOL_CIRCLE \
                        = 'draw fill line rect circle'.split()
        self.tool = self.TOOL_DRAW

        self.pen_size = 1

        self.tool_mouse_start = None

        self.cnv_size = (32, 32)

        self.savepath = "tmp/export.png" # None
        
        for ext in 'png jpg jpeg'.split():
            self.vos.open_with[ext] = self

    def notify(self, text):
        self.add(Notify(self, text))

    def on_run(self):
        super().on_run()
        self.setup_nodes()

    def set_color(self):
        def callback(c):
            self.draw_color = c
            self.notify(f"Set color to {self.draw_color}.")
        app = self.vos.get_app('Color Picker').run()
        app.set_color(self.draw_color)
        app.callback = callback

    def set_size(self):
        def callback(sz):
            try:
                self.pen_size = int(sz)
                self.notify(f"Set size to {self.pen_size}.")
            except ValueError:
                self.notify(f"Invalid size!")
        app = self.prompt(callback, "Set pen size:")

    def set_tool(self, tool):
        self.notify(f"Switched to {tool} tool.")
        self.tool = tool

    def btn_new(self):
        def callback(resp):
            try:
                res = eval(resp)
                if len(res) == 2 and isinstance(res[0], int) and isinstance(res[1], int):
                    self.cnv_size = res
                    self.setup_nodes()
                else:self.btn_new()
            except:self.btn_new()
            
        self.prompt(callback, "Enter canvas size as (width, height):")

    def open_path(self, path):
        app = self.run()
        img = app.vos.load_image(path, transparent=True)
        if not img:
            return
        
        app.savepath = path
        app.cnv_size = img.get_size()
        app.setup_nodes()
        app.cnv.set_image(img)

    def save(self):
        print('saved!')
        if isinstance(self.savepath, str):
            self.notify(self.savepath)
            pg.image.save(self.cnv.cnv, self.vos.path+self.savepath)

    def prompt(self, callback, prompt):
        self.vos.get_app('Prompt').run(lambda resp:(callback(resp), self.focus()), prompt)

    def fullscreen(self):
        cnv = self.cnv.cnv
        self.fs = not self.fs
        self.resize(self.vos.res if self.fs else self.init_res)
        self.setup_nodes()
        self.cnv.set_image(cnv)

    def setup_nodes(self):
        self.children = []

        self.cnv = Canvas(self, tuple([min(self.res)]*2), self.cnv_size)
        self.add(self.cnv)

        button_data = {
            "save [shift + s]":self.save,
            "new [shift + n]":lambda:(self.fullscreen() if self.fs else 0,self.btn_new()),
            
            "color [c]":self.set_color,
            "size [s]":self.set_size,
            
            "pen [p]":lambda:self.set_tool(self.TOOL_DRAW),
            "line [l]":lambda:self.set_tool(self.TOOL_LINE),
            "fill [f]":lambda:self.set_tool(self.TOOL_FILL),
            
            "rect [r]":lambda:self.set_tool(self.TOOL_RECT),
            "circle [o]":lambda:self.set_tool(self.TOOL_CIRCLE),
            
            "fullscreen [shift + f]":self.fullscreen
            }
        
        btn_w = self.res[0] - self.cnv.size[0]
        btn_h = self.res[1] / len(button_data)

        self.truecnv = None

        x, y = self.cnv.size[0], 0

        self.btns = {}
        for text, on_press in button_data.items():
            btn = ButtonNode(self, pos=(x,round(y)), size=(btn_w, btn_h), text = text, center=True, on_press = on_press, font = self.font)
            self.add(btn)
            self.btns[text] = btn
            y += btn_h

    def update(self):
        super().update()
        inp = self.vos.input

        if inp.text:
            text = inp.text
            if ord(text[0]) in range(ord('A'), ord('Z')+1):
                text = 'shift + '+text.lower()
            text = f'[{text}]'
            for name, btn in self.btns.items():
                if text in name:
                    btn.on_press()
            inp.text = ""
        
        if self.tool == self.TOOL_DRAW:
            if inp.click:
                self.cnv.draw(self.draw_color, self.mouse, self.pen_size)
                
        elif self.tool in [self.TOOL_LINE, self.TOOL_CIRCLE, self.TOOL_RECT]:
            if inp.click_inst:
                self.tool_mouse_start = self.mouse
                self.truecnv = self.cnv.cnv.copy()
            elif inp.click and self.truecnv:
                self.cnv.cnv = self.truecnv.copy()
                func = {
                    self.TOOL_LINE:self.cnv.line,
                    self.TOOL_CIRCLE:self.cnv.circle,
                    self.TOOL_RECT:self.cnv.rect
                    }[self.tool]
                func(self.draw_color, self.tool_mouse_start, self.mouse, self.pen_size)
            elif not inp.click and self.tool_mouse_start:
                self.tool_mouse_start = None
                
        elif self.tool == self.TOOL_FILL:
            if inp.click_inst:
                self.cnv.fill(self.draw_color, self.mouse)

    def render(self):
        self.srf.fill(self.bg)
        self.render_nodes()
        super().render()
