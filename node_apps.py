import pygame as pg
from vos_apps import WindowApp, point_within_rect

class NodeApp(WindowApp):
    def __init__(self, vos, name="NodeApp", res=None):
        super().__init__(vos, name, res)
        self.children = []
        self.global_pos = (0,0)
    def update(self):
        super().update()
        for node in self.children:
            node.update()
    def render_nodes(self):
        self.srf.fill(self.bg)
        for node in self.children:
            node.render()
    def render(self):
        super().render()
    def add(self, node):
        self.children.append(node)
        node.parent = self
        node.orphan = False
    def remove(self, node):
        self.children.remove(node)
        node.orphan = True

class Node:
    def __init__(self, app, pos=(0,0)):
        self.app = app
        self.vos = app.vos
        self.children = []
        self.parent = None
        self.x, self.y = pos
        self.orphan = True
    @property
    def global_pos(self):
        x, y = self.parent.global_pos
        return self.x, self.y
    def update(self):
        for node in self.children:
            node.update()
    def render(self):
        for node in self.children:
            node.render()
    def add(self, node):
        self.children.append(node)
        node.parent = self
        node.orphan = False
    def remove(self, node):
        self.children.remove(node)
        node.orphan = True

class SurfaceNode(Node):
    def __init__(self, app, pos=(0,0), size=(100, 100)):
        super().__init__(app, pos)
        self.size = size
        self.srf = pg.Surface(size)
        self.parent_srf = self.app.srf
    def render(self):
        self.parent_srf.blit(self.srf, self.global_pos)
        super().render()

class RectNode(Node):
    def __init__(self, app, pos=(0,0), size=(100, 100), color=(255,0,255)):
        super().__init__(app, pos)
        self.size = size
        self.srf = pg.Surface(size)
        self.color = color
    def render(self):
        pg.draw.rect(self.app.srf, self.color, list(self.global_pos) + list(self.size))
        super().render()

class TextNode(SurfaceNode):
    def __init__(self, app, pos=(0,0), size=(100, 100), text="This is a TextNode", font = None, color=(255,255,255), background=(0,0,0), center = False, parent_srf = None):
        super().__init__(app, pos, size)
        if parent_srf:
            self.parent_srf = parent_srf
        self.text = text
        self.old_text = None
        self.font = font if font else self.vos.font
        self.color = color
        self.bg = background
        self.center = center
    def render(self):
        if self.text != self.old_text:
            if self.bg:
                self.srf.fill(self.bg)
            self.old_text = self.text
            srf = self.font.render(self.text, True, self.color, self.bg)
            if not self.center:
                self.srf.blit(srf, (0,0))
            else:
                w, h = srf.get_size()
                W, H = self.size
                self.srf.blit(srf, (W//2-w//2,H//2-h//2))
        super().render()

class ScrollTextNode(SurfaceNode):
    def __init__(self, app, pos=(0,0), size=(100, 100), text="This is a TextNode", font = None,
                 color=(255,255,255), background=(0,0,0), center = False, line_height = None, parent_srf = None):
        super().__init__(app, pos, size)
        if parent_srf:
            self.parent_srf = parent_srf
        self.text = text
        self.old_text = None
        self.font = font if font else self.vos.font
        self.color = color
        self.bg = background
        self.center = center
        self.line_height = line_height if line_height else self.font.render("lyg", True, [0]*3).get_height()
        self.scroll = 0
        self.old_scroll = None
        self.nlines = 0
        self.speed = 1
    def update(self):
        if not self.app.visible:
            return
        self.scroll -= self.vos.input.scroll * self.speed * self.line_height
        self.scroll = max(min(self.scroll, (self.line_height * self.nlines - self.size[1])), 0)
        super().update()
    def render(self):
        if self.text != self.old_text:
            lines = self.text.split('\n')
            self.nlines = len(lines)
            self.text_srf = pg.Surface((self.size[0], self.line_height * self.nlines))
            if self.bg:
                self.text_srf.fill(self.bg)
            y = 0
            for line in lines:
                text = TextNode(self.app, (0,y), (self.size[0], self.line_height),
                                line, self.font, self.color, self.bg, self.center,
                                parent_srf = self.text_srf)
                text.parent = self
                text.render()
                y += self.line_height

        if self.scroll != self.old_scroll or self.text != self.old_text:
            self.old_text = self.text
            self.old_scroll = self.scroll
            self.srf.fill(self.bg)
            self.srf.blit(self.text_srf, (0, -self.scroll))
        super().render()

class ButtonNode(TextNode):
    def __init__(self, app, pos=(0,0), size=(100, 100), text="This is a TextNode",
                 font = None, color=(255,255,255), background=(0,0,0), on_press=None,
                 center = False):
        super().__init__(app, pos, size, text, font, color, background, center)
        self.on_press = on_press
        self.pressed = False
    def update(self):
        super().update()
        if not self.app.visible:
            return
        inp = self.vos.input
        self.pressed = True
        if inp.click_inst and point_within_rect(self.app.mouse, [self.x, self.y]+list(self.size)) and self.on_press:
            self.on_press()
            self.pressed = True
