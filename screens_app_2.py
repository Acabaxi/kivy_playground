import kivy
kivy.require('1.0.6')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.filechooser import FileChooserIconView

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.core.window import Window

from kivy.uix.behaviors import FocusBehavior

from kivy.core.window import Window
from kivy.properties import ObjectProperty, StringProperty
#
from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'dock')
Config.set('kivy', 'keyboard_layout', 'numeric.json')

from kivy.uix.behaviors import ButtonBehavior

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
        FloatLayout:          
            Image:
                id: image
                pos_hint:{'right':1}
                source: ""
            Button:
                id: butao
                text: 'Siga'
                pos_hint:{'right':1,'top':0.2}
                size_hint:0.2,0.15
                background_color:[1,1,1,0.5]
                on_press: 
                    root.manager.current = 'image_grid'
                    root.manager.transition.direction = 'left'
<ImageGridScreen>
    id: image_grid
    on_pre_enter: image_grid.create_grid_widget()
    
<BigImageScreen>
    id: big_image
    on_pre_enter: big_image.show_big_image()
        
    
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
        global current_filenames
        current_filenames = filename
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
        return "./images"

    pass


current_filenames = []
image_tints = {}
current_image = []


class ImageGridScreen(Screen,):
    
    def __init__(self, **kwargs):
        super(ImageGridScreen, self).__init__(**kwargs)

    def create_grid_widget(self):
        wid = create_image_grid_layout(current_filenames)
        self.add_widget(wid)

    def sup(self):
        print("ZAAAAAAAS")




class ImageButton(ButtonBehavior, Image):
    # Behaviour of button, look of image
    pass


class BigImageScreen(Screen):
    def __init__(self, **kwargs):
        super(BigImageScreen, self).__init__(**kwargs)
        flayout = FloatLayout()
        flayout.add_widget(Image(size_hint=[1,1]))

        # Selector grid
        grid_layout = GridLayout(cols=1, pos_hint={'right': 0.95, 'top': 0.5}, size_hint=[0.05, 0.4],
                                 spacing=[0, 10] )
        grid_layout.add_widget(ToggleButton(text="FL", group='region', on_press=set_fl))
        grid_layout.add_widget(ToggleButton(text="FR", group='region', on_press=set_fr))
        grid_layout.add_widget(ToggleButton(text="BR", group='region', on_press=set_br))
        grid_layout.add_widget(ToggleButton(text="BL", group='region', on_press=set_bl))
        grid_layout.add_widget(Label())
        grid_layout.add_widget(ToggleButton(text="Exclude", group='region', on_press=exclude_image))
        grid_layout.add_widget(Button(text="Back", on_release=back_to_img_grid))

        flayout.add_widget(grid_layout)

        self.add_widget(flayout)

    def show_big_image(self):
        print(current_image)
        self.children[0].children[1].source = current_image
        self.children[0].children[1].reload()

        # Reset toggle buttons
        for btn in self.children[0].children[0].children:
            btn.state = 'normal'

        # self.children[0].source = current_image
        # self.children[0].reload()

    pass


def create_image_grid_layout(filenames, ):
    print("Creating grid")
    grid_layout = GridLayout(cols=3, row_force_default=True, row_default_height=200)
    for img_name in filenames:
        tint = get_tint_value(img_name)
        aaa = ImageButton(source=img_name, color=tint, on_press=tint_image, on_release=unselect, )
        # grid_layout.add_widget(Image(source=img_name))
        grid_layout.add_widget(aaa)
        print(img_name)

    return grid_layout


def get_tint_value(img_name, ):
    if img_name not in image_tints:
        return 1, 1, 1, 1
    elif image_tints[img_name] == 'e':
        return 1, 0, 0, 1
    elif image_tints[img_name] == 'FR':
        return 0, 1, 0, 1
    elif image_tints[img_name] == 'FL':
        return 0, 0, 1, 1
    elif image_tints[img_name] == 'BR':
        return 0, 1, 1, 1
    elif image_tints[img_name] == 'BL':
        return 1, 0, 1, 1



    else:
        return 1,1,1,1


def exclude_image(button):
    image_tints[current_image] = 'e'

def set_fl(button):
    image_tints[current_image] = 'FL'

def set_fr(button):
    image_tints[current_image] = 'FR'

def set_bl(button):
    image_tints[current_image] = 'BL'

def set_br(button):
    image_tints[current_image] = 'BR'


def back_to_img_grid(button):
    sm.transition.direction = 'right'
    sm.current = 'image_grid'


def tint_image(bois):
    bois.color = (1,0,1,1)
    global current_image
    current_image = bois.source
    sm.transition.direction = 'left'
    sm.current = 'big_image'
    print(bois.source)


def unselect(bois):
    bois.color = (1, 1, 1, 1)
    print(bois.source)


sm = ScreenManager()
class ScreenApp(App):
    def build(self):

        # sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(FileChooseScreen(name='file_chooser'))
        sm.add_widget(ImageGridScreen(name='image_grid'))
        sm.add_widget(BigImageScreen(name='big_image'))
        return sm


if __name__ == '__main__':

    ScreenApp().run()
