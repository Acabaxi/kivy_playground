import kivy
kivy.require('1.0.6')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.filechooser import FileChooserIconView

from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

from kivy.uix.behaviors import FocusBehavior

from kivy.core.window import Window
from kivy.properties import ObjectProperty, StringProperty
#
from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'dock')
Config.set('kivy', 'keyboard_layout', 'numeric.json')


Builder.load_string("""
<MenuScreen>:
    id: fds
    GridLayout:
        cols: 2
        AnchorLayout:
            anchor_x:'center'
            anchor_y:'center'
            TextInput:
                id: id_input
                font_size: 20
                halign: 'center'
                hint_text: 'Patient ID'
                size_hint_x: 0.5
                size_hint_y: 0.5
                padding_y: self.size[0] / 10
                on_text: fds.save_text(id_input.text)
                on_focus: fds.focus_value(id_input)
        ToggleButton:
            text: 'Quit'
            group: 'input_media'
        AnchorLayout:
            anchor_x:'center'
            anchor_y:'center'
            TextInput:
                id: num_input
                font_size: 20
                halign: 'center'
                hint_text: 'UF number'
                size_hint_x: 0.5
                size_hint_y: 0.5
                padding_y: self.size[0] / 10
                on_text: fds.save_text(num_input.text)
                on_focus: fds.focus_value(id_input)
        ToggleButton:   
            text: 'Quit'
            group: 'input_media'
        Label:
        Label:
        Label:
        Button:
            text:'zas'
            on_press: 
                root.manager.current='file_chooser'
                root.manager.transition.direction = 'left'
<SettingsScreen>:
    BoxLayout:
        Button:
            text: 'My settings button'
        Button:
            text: 'Back to menu'
            on_press: 
                root.manager.current = 'menu'
                root.manager.transition.direction = 'left'
<FileChooseScreen>
    id: fc_widget
    BoxLayout:
        FileChooserIconView:
            id: filechooser
            multiselect: True
            path: fc_widget.set_path()
            on_selection: fc_widget.selected(filechooser.selection)
            size_hint_x: 1
        Image:
            id: image
            source: ""
""")


class MenuScreen(Screen):

    def save_text(self, value):
        print(value)

    def focus_value(self, text_input):
        print("FOCUS IS ", text_input.focus)
        print("Size is", text_input.size)
    pass


class SettingsScreen(Screen):
    pass


class FileChooseScreen(Screen):

    def __init__(self, **kwargs):
        super(FileChooseScreen, self).__init__(**kwargs)
        self.previous_filenames = {}

    def selected(self, filename):

        filenames = set(filename)
        z = filenames.symmetric_difference(self.previous_filenames)

        for i in z:
            self.ids.image.source = i
            break

        self.previous_filenames = filename.copy()


        # try:
        #     print("all files", filename)
        #     self.ids.image.source = filename[0]
        #     print(filename[-1])
        # except:
        #     pass

    def set_path(self):
        return "/home/pedro"
    pass


class ScreenApp(App):
    def build(self):

        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(FileChooseScreen(name='file_chooser'))
        return sm


if __name__ == '__main__':

    ScreenApp().run()
