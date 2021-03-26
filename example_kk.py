#!/usr/bin/env python
# -*- coding: utf-8
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.app import App
from kivy.core.window import Window

__author__ = 'test'
__version__ = '1.0'

Builder.load_string("""
#:kivy 1.9.1
<MyClass>:
    BoxLayout:
        id: main_layout
        orientation: 'vertical'
        canvas:
            Color:
                rgb: .5, .5, .5
            Rectangle:
                size: self.size
                pos: self.pos
        GridLayout:
            size_hint: (1, None)
            height: 200
            padding: 10
            rows: 1
            BoxLayout:
                canvas:
                    Color:
                        rgb: .2, .1, .5
                    Rectangle:
                        size: self.size
                        pos: self.pos
        TextInput:
            size_hint: (1,.1)
            text: app.text
            text_size: self.width - 20, self.height
#            size: self.texture_size
            valign: 'top'
""")

class MyClass(BoxLayout):

    def __init__(self, **kwargs):
        super(MyClass, self).__init__(**kwargs)
        softinput_mode = 'below_target'
        Window.softinput_mode = softinput_mode

class MyApp(App):
    def build(self):
        text = """
        Lorem ipsum dolor sit amet, consectetur adipiscing elit,
        sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
        Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut
        aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit
        in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
        Excepteur sint occaecat cupidatat non proident, sunt in culpa qui
        officia deserunt mollit anim id est laborum"""
        setattr(self, 'text', text)

        self.root = MyClass()
        self.root.bind(height = self.on_height)

        return self.root

    def on_height(self, instance, value):
        # instance.y += Window.keyboard_height
        print ("height changed!")

if __name__ == '__main__':
    my_app = MyApp()
    my_app.run()