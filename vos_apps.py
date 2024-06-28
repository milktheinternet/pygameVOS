import pygame as pg

CURID = 0
def nextID():
    global CURID
    CURID+=1
    return CURID

def point_within_rect(point, rect):
    px, py = point
    x, y, w, h = rect
    return x <= px < x + w and y <= py < y + h

class App:
    def __init__(self, vos, name="AppClass"):
        self.desktop = True
        self.vos = vos
        self.name = name
        self.id = nextID()
        self.flags = []
        self.active = True
        self.visible = False
        self.path = self.vos.path_apps + name + '/'

    def open_path(self, path):
        self.vos.log(f'opened {path} with {self.name} (did nothing)')
        
    def run(self):
        app = type(self)(self.vos)
        running_names = ', '.join([f'{app.name}{app.id}' for app in self.vos.running])
        #print(f"adding {self.name}{self.id} to {running_names}")
        self.vos.running.append(app)
        app.on_run()
        self.vos.on_run(app)
        return app

    def on_run(self):
        pass

    def close(self):
        self.vos.log("closed",self.name)
        app = type(self)(self.vos)
        if self in self.vos.running:
            self.vos.running.remove(self)
        
    def update(self):
        pass
    def render(self):
        pass
    def idle_render(self):
        pass

class SurfaceApp(App):
    def __init__(self, vos, name="SurfaceAppClass", res=None):
        super().__init__(vos, name)
        self.visible = True
        self.res = res if res else vos.res
        self.parent_srf = vos.srf
        self.center()
    def center(self):
        self.x, self.y = ((self.vos.res[0]-self.res[0])//2, (self.vos.res[1]-self.res[1])//2)
    def resize(self, res=None):
        if res: self.res = res
        self.center()
        self.srf = pg.Surface(self.res)
    def on_run(self):
        self.resize()
    def render(self):
        self.idle_render()
    def idle_render(self):
        self.parent_srf.blit(self.srf, (self.x, self.y))

    @property
    def rect(self):
        return [self.x, self.y] + list(self.res)

    @property
    def mouse(self):
        mx, my = self.vos.input.mouse
        return mx - self.x, my - self.y


class WindowApp(SurfaceApp):
    def __init__(self, vos, name="WindowAppClass", res=None):
        super().__init__(vos, name, res)
        self.flags.append("WindowApp")
        
        self.tab_height = 15
        self.tab_bg = (200, 200, 200)
        self.tab_close = (255, 0, 0)
        self.tab_minimize = (255, 200, 0)
        self.tab_resize = (0, 0, 255)

        self.dragging = False
        self.drag_from = (0, 0)

        self.bg = (50,50,50)

        self.fs = False

        self.minimize_start = 0
        self.minimize_duration = 500
        self.minimize_srf = None

        self.resizeable = False

    def on_run(self):
        super().on_run()
        self.vos.input.on_click.insert(0,self.on_click)
        self.focus()
        
    def close(self):
        while self.on_click in self.vos.input.on_click:
            self.vos.input.on_click.remove(self.on_click)
        super().close()

    def focus(self):
        vos = self.vos
        self.visible = True

        #stop all window apps
        for app in vos.running:
            if "WindowApp" in app.flags:
                app.active = False
        self.active = True
        
        vos.running.remove(self)
        vos.running.append(self)
        
        if self.on_click in vos.input.on_click:
            vos.input.on_click.remove(self.on_click)
        vos.input.on_click.insert(0,self.on_click)

    @property
    def full_rect(self):
        return list(self.tab_pos) + [self.res[0], self.res[1]+self.tab_height]

    def on_click(self):
        if not self.visible:return
        
        tabx, taby = self.tab_pos
        tabh = self.tab_height
        mx, my = self.vos.input.mouse

        w,h = self.res

        clicked_window = point_within_rect((mx, my), self.full_rect)

        if clicked_window:
            self.focus()
        
        if point_within_rect((mx, my), (tabx, taby, self.res[0], tabh)):
            if mx > tabx + self.res[0] - tabh: # close button
                self.close()
            elif mx > tabx + self.res[0] - tabh*2: # minimize button
                self.minimize()
            elif self.resizeable and mx > tabx + self.res[0] - tabh*3:
                # resizing button
                self.vos.get_app("Resizer").run(target=self)
            elif self.active:
                self.dragging = True
                self.drag_from = self.mouse

        return clicked_window

    def minimize(self):
        self.visible = False
        self.active = False
        self.vos.log(f"minimizing {self.name}")
        self.animate_minimize()
        self.on_minimize(self)

    def on_minimize(self, app):
        self.vos.log(f"no minimization handler for {self.name}")

    def make_tab_srf(self):
        w, h = (self.res[0], self.tab_height)
        self.tab_srf = pg.Surface((w,h))
        self.tab_srf.fill(self.tab_bg)
        pg.draw.rect(self.tab_srf, self.tab_close, (w-h, 0, h, h))
        pg.draw.rect(self.tab_srf, self.tab_minimize, (w-h*2, 0, h, h))
        if self.resizeable:
            pg.draw.rect(self.tab_srf, self.tab_resize, (w-h*3, 0, h, h))

    @property
    def tab_pos(self):
        return (self.x, self.y-self.tab_height)

    def resize(self, res=None):

        self.vos.input.reset()
        
        if res: self.res = res

        self.fs = self.res == self.vos.res
        
        if not self.fs:
            self.make_tab_srf()
        super().resize()
    
    def update(self):
        if self.dragging:
            mx, my = self.vos.input.mouse
            dx, dy = self.drag_from
            self.x, self.y = mx - dx, my - dy
            self.x = max(-self.res[0] + self.tab_height * 4, min(self.vos.res[0]-self.tab_height, self.x))
            self.y = max(self.tab_height, min(self.vos.res[1], self.y))
            if not self.vos.input.click:
                self.dragging = False

    def render(self):
        if self.visible:
            super().render()

    def animate_minimize(self):
        srf = pg.Surface(self.full_rect[2:])
        srf.blit(self.tab_srf, (0,0))
        srf.blit(self.srf, (0, self.tab_height))
        self.minimize_start = self.vos.time
        self.minimize_srf = srf
        
    
    def idle_render(self):
        if self.visible:
            if not self.fs:
                self.render_tab()
            super().idle_render()
        if self.minimize_start:
            delta = self.vos.time - self.minimize_start
            delta /= self.minimize_duration
            delta **= 2
            if delta > 1:
                self.minimize_start = 0
            else:
                scale = 1 - delta
                self.minimize_srf.set_alpha(
                    round(scale*255))
                size = (round(self.res[0]*scale),
                        round(self.res[1]*scale))
                x, y = self.tab_pos
                pos = (x+self.res[0]-size[0],
                       y)
                self.vos.srf.blit(
                    pg.transform.smoothscale(
                        self.minimize_srf, size), pos)

    def render_tab(self):
        self.parent_srf.blit(self.tab_srf, self.tab_pos)


class TextApp(WindowApp):
    def __init__(self, name, vos, resolution=None, font=None):
        super().__init__(name, vos, resolution)
        self.font = font if font else self.vos.load_font(size=17)
        self.margin = 10
        self.line_height = 20
        if not self.res:
            self.res = self.vos.res
        self.max_lines = self.res[1]//(self.line_height+self.margin)
        self.bg = (0,0,0)
        self.color = (255,255,255)
        self.old_text = ""
    def update_render(self, text):
        if text == self.old_text:
            return
        self.old_text = text
        self.srf.fill(self.bg)
        x, y = self.margin, self.margin
        lines = text.split('\n')
        lines = lines[:min(self.max_lines, len(lines))]
        for line in lines:
            if line:
                self.srf.blit(
                    self.font.render(line, True, self.color, self.bg), (x,y))
            y += self.line_height

class DictMenuApp(TextApp):
    def __init__(self, name, vos, resolution=None):
        super().__init__(name, vos, resolution)
        self.tree = {"- no options -":None}
        self.location = []
        self.idx = 0
        self.BACK = "<- back"
        self.text = ""

        self.branchflags = []
        
    def back(self):
        if self.location:
            self.location.pop()
            if "double_back" in self.branchflags:
                self.branchflags = []
                self.back()
        
    def get_branch(self, loc):
        loc = list(loc)
        branch = self.tree
        [branch:=branch[loc] for loc in self.location]
        return branch

    def update_options(self):
        branch = self.get_branch(self.location)
        
        options = list(branch.keys())

        self.branchflags = branch.get("flags")
        if self.branchflags != None:
            options.remove('flags')
        else:
            self.branchflags = []

        
        
        if self.location:
            options.insert(0, self.BACK)
        self.idx %= len(options)

        s = self.text + '\n\n' if self.text else ''
        for i in range(len(options)):
            s += ('> ' if self.idx == i else '  ') + options[i] + '\n'

        if pg.K_RETURN in self.vos.input.keys_inst:
            choice = options[self.idx]
            self.idx = 0
            if choice == self.BACK:
                self.back()
            elif isinstance(branch[choice], dict):
                self.location.append(choice)
            elif branch[choice]:branch[choice]()

        self.update_render(s)

    def on_run(self):
        super().on_run()
        self.update_render(str(self.tree))

    def update(self):
        if not self.visible:
            return
        super().update()
        inp = self.vos.input
        if pg.K_UP in inp.keys_inst:
            self.idx -= 1
        if pg.K_DOWN in inp.keys_inst:
            self.idx += 1

        self.update_options()
