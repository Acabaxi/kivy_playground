import kivy
kivy.require('1.0.9')

import example_program

from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'systemanddock')
Config.set('kivy', 'keyboard_layout', 'numeric.json')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.filechooser import FileChooserIconView

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout

from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.uix.image import Image

from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

Window.fullscreen = True

from kivy.uix.behaviors import FocusBehavior


from kivy.properties import ObjectProperty, StringProperty
#

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("module://kivy.garden.matplotlib.backend_kivy")
from kivy.garden.matplotlib import FigureCanvasKivyAgg

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
                font_size: 50
                halign: 'center'
                hint_text: 'Patient ID'
                size_hint_x: 0.5
                size_hint_y: 0.5
                padding: [0, ( self.height - self.line_height ) / 2]
                on_text: fds.save_patient_id(id_input.text)
                on_focus: fds.focus_value(id_input)
        AnchorLayout:
            ToggleButton:
                size_hint_x: 0.25
                size_hint_y: 0.5
                text: 'SD Card'
                group: 'input_media'
        AnchorLayout:
            anchor_x:'center'
            anchor_y:'center'
            TextInput:
                id: num_input
                font_size: 50
                halign: 'center'
                hint_text: 'UF number'
                size_hint_x: 0.5
                size_hint_y: 0.5
                padding: [0, ( self.height - self.line_height ) / 2] 
                on_text: fds.save_uf_number(num_input.text)
                on_focus: fds.focus_value(id_input)
        AnchorLayout:
            ToggleButton:
                size_hint_x: 0.25
                size_hint_y: 0.5   
                text: 'From Camera'
                group: 'input_media'
        Label:
        Label:
        Label:
        AnchorLayout:
            Button:
                size_hint_x: 0.25
                size_hint_y: 0.5
                text:'Prosseguir'
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
    AnchorLayout:
        anchor_x:'right'
        anchor_y:'bottom'
        Button:
            id: butao
            text: 'Siga'
            #pos_hint:{'right':1,'top':0.2}
            size_hint:0.1,0.1
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

patient_id = -1
uf_number = -1
class MenuScreen(Screen):

    def save_patient_id(self, value):
        global patient_id
        print("Saving patient id", value)
        patient_id = value

    def save_uf_number(self, value):
        global uf_number
        print("Saving uf number", value)
        uf_number = value

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
        # Avoid inserting duplicate widgets on layout
        self.clear_widgets()

        # self explanatory
        wid = create_image_grid_layout(current_filenames)

        # Scroll grid
        scroll_widget = ScrollView(size_hint=(1,1), size=(500,500))
        scroll_widget.add_widget(wid)
        self.add_widget(scroll_widget)

        next_button_layout = AnchorLayout(anchor_x='right',
                             anchor_y='bottom')
        next_button = Button(size_hint_x=0.1,
                             size_hint_y=0.1,
                             text='Next screen',
                             on_press=to_processing_screen
                             )
        next_button_layout.add_widget(next_button)
        self.add_widget(next_button_layout)


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
        grid_layout.add_widget(ToggleButton(text="FL", group='region', on_press=set_fl,on_release=back_to_img_grid))
        grid_layout.add_widget(ToggleButton(text="FR", group='region', on_press=set_fr,on_release=back_to_img_grid))
        grid_layout.add_widget(ToggleButton(text="BR", group='region', on_press=set_br,on_release=back_to_img_grid))
        grid_layout.add_widget(ToggleButton(text="BL", group='region', on_press=set_bl,on_release=back_to_img_grid))
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

    pass


def create_image_grid_layout(filenames, ):
    print("Creating grid")
    grid_layout = GridLayout(cols=3, row_force_default=True, row_default_height=200, size_hint_y=None, spacing=10)
    grid_layout.bind(minimum_height=grid_layout.setter('height'))
    for img_name in filenames:
        tint = get_tint_value(img_name)
        img_label = get_image_label(img_name)
        anchor_image_button_layout = FloatLayout()
        aaa = ImageButton(source=img_name, color=tint, on_press=tint_image, on_release=unselect, pos_hint={'right': 1, 'top': 1})
        bbb = Button(size_hint=(0.1, 0.2), background_color=[1, 1, 1, 0.5], pos_hint={'right': 1, 'top': 1}, text=img_label, background_down='atlas://data/images/defaulttheme/button')

        anchor_image_button_layout.add_widget(aaa)
        anchor_image_button_layout.add_widget(bbb)
        # grid_layout.add_widget(Image(source=img_name))

        grid_layout.add_widget(anchor_image_button_layout)
        print(img_name)

    return grid_layout


def get_tint_value(img_name, ):
    if img_name not in image_tints:
        return 1, 1, 1, 1
    elif image_tints[img_name] == 'e':
        return 1, 0, 0, 0.75
    elif image_tints[img_name] == 'FR':
        return 1, 1, 1, 0.5
    elif image_tints[img_name] == 'FL':
        return 1, 1, 1, 0.5
    elif image_tints[img_name] == 'BR':
        return 1, 1, 1, 0.5
    elif image_tints[img_name] == 'BL':
        return 1, 1, 1, 0.5
    else:
        return 1, 1, 1, 1


def get_image_label(img_name, ):
    if img_name not in image_tints:
        return ""
    elif image_tints[img_name] == 'e':
        return "XXX"
    elif image_tints[img_name] == 'FR':
        return "FR"
    elif image_tints[img_name] == 'FL':
        return "FL"
    elif image_tints[img_name] == 'BR':
        return "BR"
    elif image_tints[img_name] == 'BL':
        return "BL"
    else:
        return ""


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


# Processing Screen
def to_processing_screen(button):
    sm.transition.direction = 'left'
    sm.current = 'processing'


processed_images = {}
image_counts = {}
validated = False
count_margin_percent = 5
selected_images_max = {}
selected_images_min = {}


def validate_count():

    img_distribution = {}

    for img_num in range(len(image_tints.keys())):
        zone = image_tints[list(image_tints.keys())[img_num]]
        if zone in img_distribution:
            img_distribution[zone].append(img_num)
        else:
            img_distribution[zone] = [img_num]

    max_value = 0
    min_value = 0
    for key in img_distribution:
        zone_max = max(img_distribution[key], key=lambda x: image_counts[x])
        zone_min = min(img_distribution[key], key=lambda x: image_counts[x])

        selected_images_max[key] = zone_max
        selected_images_min[key] = zone_min

        max_value = max_value + image_counts[zone_max]
        min_value = min_value + image_counts[zone_min]

    print("Max value found", max_value)
    print("Min value found", min_value)
    print(img_distribution)
    print(image_counts)


class ProcessingScreen(Screen):
    def __init__(self, **kwargs):
        super(ProcessingScreen, self).__init__(**kwargs)
        self.add_widget(Label(text='Processing...'))

    def on_enter(self):
        print("Entering")
        print(current_filenames)

        global processed_images
        global image_counts
        processed_images, image_counts = example_program.read_images_and_flip(current_filenames)

        validate_count()
        sm.transition.direction = 'left'
        sm.current = 'results'

    pass


# Results grid

class ResultsGridScreen(Screen):
    def __init__(self, **kwargs):
        super(ResultsGridScreen, self).__init__(**kwargs)

    def on_pre_enter(self, *args):
        self.clear_widgets()
        #
        res_layout = BoxLayout(orientation='vertical')
        btn1 = Label(size_hint=(1, 0.1), text='Results', font_size=50)

        #
        image_grids_result_layout = GridLayout(size_hint=(1, 0.8), cols=2)

        for key in selected_images_max:
            if key == 'e':
                continue
            img_number = selected_images_max[key]
            img = processed_images[img_number][:,:,::-1]
            fig, ax = self.get_image_figure(img)
            image_grids_result_layout.add_widget(FakeFigureCanvas(figure=fig))


        # img1 = processed_images[0][:,:,::-1]
        # img2 = processed_images[1][:,:,::-1]
        # img3 = processed_images[2][:,:,::-1]
        # img4 = processed_images[3][:,:,::-1]
        # # img4 = plt.imread('images/microwave-custard-pudding-3a-1.jpg')
        # # img3 = plt.imread('images/delish-190802-pumpkin-pudding-0042-portrait-pf-1568301342.jpg')
        # # img2 = plt.imread('images/Vanilla-Pudding-SM-4457.jpg')
        # # img1 = plt.imread('images/queen-of-puddings-8059-1.jpeg')
        #
        # fig1, ax1 = self.get_image_figure(img1)
        # fig2, ax2 = self.get_image_figure(img2)
        # fig3, ax3 = self.get_image_figure(img3)
        # fig4, ax4 = self.get_image_figure(img4)
        #
        # image_grids_result_layout.add_widget(FakeFigureCanvas(figure=fig1))
        # image_grids_result_layout.add_widget(FakeFigureCanvas(figure=fig2))
        # image_grids_result_layout.add_widget(FakeFigureCanvas(figure=fig3))
        # image_grids_result_layout.add_widget(FakeFigureCanvas(figure=fig4))

        #
        bottom_box = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        btn2 = Button(text='Continue??', background_color=[0,1,0,1],background_down='atlas://data/images/defaulttheme/button')
        btn_yes = Button(text='Yes')
        btn_no = Button(text='No')
        bottom_box.add_widget(btn_no)
        bottom_box.add_widget(btn2)
        bottom_box.add_widget(btn_yes)

        res_layout.add_widget(btn1)
        res_layout.add_widget(image_grids_result_layout)
        res_layout.add_widget(bottom_box)

        self.add_widget(res_layout)

    def get_image_figure(self, image):
        fig, ax = plt.subplots()
        fig.set_facecolor('black')
        ax.axis("off")
        imgplot = ax.imshow(image)

        return fig, ax


class FakeFigureCanvas(FigureCanvasKivyAgg):
    # https://andnovar.wordpress.com/2015/06/15/connecting-events-between-kivy-and-matplotlib/
    def __init__(self, **kwargs):
        super(FakeFigureCanvas, self).__init__(**kwargs)

    # Disables previously defined on_touch_down. Doesn't call vitual keyboard
    def on_touch_down(self, event):
        pass


sm = ScreenManager()


class ScreenApp(App):
    def build(self):

        # sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(FileChooseScreen(name='file_chooser'))
        sm.add_widget(ImageGridScreen(name='image_grid'))
        sm.add_widget(BigImageScreen(name='big_image'))
        sm.add_widget(ProcessingScreen(name='processing'))
        sm.add_widget(ResultsGridScreen(name='results'))
        return sm


if __name__ == '__main__':

    ScreenApp().run()
