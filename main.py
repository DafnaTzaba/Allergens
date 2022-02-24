from kivy.uix import dropdown
from kivy.uix.dropdown import DropDown
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.camera import Camera
import cv2
from kivy.properties import BooleanProperty
from kivymd.theming import ThemeManager
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem, MDList, OneLineIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.icon_definitions import md_icons
from kivy.uix.scrollview import ScrollView
from plyer import filechooser
import codeProject


IallergicEng=['Gluten','Milk','Peanuts','Soy','Tuna','Eggs','Fish','Nuts','Tonsils']

'''
for AllergScreen
'''
class ListItemWithCheckbox(OneLineAvatarIconListItem):
    '''Custom list item.'''
    icon = StringProperty("android")
    def check(self):
        myscreen=self.parent.parent.parent.manager.screens[2]
        arr=AllergScreen.save_checked(myscreen)
        if len(arr)==0:
            myscreen.ids.next_button.disabled = True
        else:
            myscreen.ids.next_button.disabled = False




class RightCheckbox(IRightBodyTouch, MDCheckbox):
    '''Custom right container.'''
    pass
class IconListItem(OneLineIconListItem):
    icon = StringProperty()


'''
Application opening screen
'''
class MenuScreen(Screen):
   pass


'''
Screen for selecting the desired allergens for testing
'''
class AllergScreen(Screen):
    '''
    initialization list of the ellargan (checkBox)
    '''
    def on_enter(self, *args):

        x = len(self.ids.scroll.children)
        if (x == 0):#In order not to reboot the list every time you return to the screen
         icons = list(md_icons.keys())

         self.ids.scroll.add_widget(ListItemWithCheckbox(text=f"Gluten" , icon="bread-slice",))
         self.ids.scroll.add_widget( ListItemWithCheckbox(text=f"Milk", icon="cow"))
         self.ids.scroll.add_widget(ListItemWithCheckbox(text=f"Peanuts", icon="peanut"))
         self.ids.scroll.add_widget(ListItemWithCheckbox(text=f"Soy", icon="soy-sauce"))
         self.ids.scroll.add_widget(ListItemWithCheckbox(text=f"Tuna", icon="fish"))
         self.ids.scroll.add_widget(ListItemWithCheckbox(text=f"Eggs", icon="egg"))
         self.ids.scroll.add_widget(ListItemWithCheckbox(text=f"Fish", icon="fish"))
         self.ids.scroll.add_widget(ListItemWithCheckbox(text=f"Nuts", icon="nut"))
         self.ids.scroll.add_widget(ListItemWithCheckbox(text=f"Tonsils", icon="nut"))

 # return a list of number of all the items that marked in the checkBox by their location index in the list
    def save_checked(self):

        allergList=[]
        mdlist = self.ids.scroll  # get reference to the MDList
        for item in mdlist.children:
            if isinstance(item, ListItemWithCheckbox):  # only interested in the ListItemWithCheckboxes- isinstance cheking if item is ListItemWithCheckbox
                cb = item.ids.cb  # use the id defined in kv
                if cb.active:  # only print selected items
                    allergList.append(IallergicEng.index(item.text))# insert to the list the index of the item

        return allergList




'''
 screen to upload/take a product picture 
'''
class UploadScreen(Screen):
    cameraActive = BooleanProperty(False)
    capture = cv2.VideoCapture()
# open/close camera button
    def start_camera(self):
            # if the camera turn off
        if not self.cameraActive:
            self.ids.camera_button.text = 'Stop Camera'
            self.ids.uploued_button.disabled = True
            self.image = self.ids.my_image
            self.capture = cv2.VideoCapture(0)
            if self.capture.isOpened():
                self.cameraActive = True
                Clock.schedule_interval(self.update, 1.0 / 10.0)
            else:
                print('Cannot Open the Camera at index 0')
        else:#close camera
            self.cameraActive = False
            self.ids.camera_button.text = 'Start Camera'
            if self.capture.isOpened():
                #take the last frame and save
                ret,frame = self.capture.read()
                cv2.imwrite('frame1.jpg', frame)
                self.ids.uploued_button.disabled = False
                self.cameraActive = False
                # set on the screen
                self.capture.release()#close camera
                self.ids.my_image.source = 'frame1.jpg'
                self.ids.next_button.disabled = False

        return self.capture

# icon Back. release camera if open
    def on_upload_back(self):
        self.cameraActive = False
        self.ids.camera_button.text = 'Start Camera'
        self.capture.release()
        self.manager.current = 'allerg'#back to the allerg windows

# video update on screen all the time
    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            # convert it to texture
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tobytes()
            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.image.texture = image_texture
            self.ids.my_image = self.image


#uploading files frome the device
    def upload_file(self):
        self.ids.camera_button.disabled = True
        path = filechooser.open_file(title="Pick a Image file..")
        pathstr=str(path)
        #Arranging the path- in some computers the slashes in the path are doubled
        pathstr = pathstr.replace('\\\\', "/")
        pathstr = pathstr.replace("[\'", "")
        pathstr = pathstr.replace("\']", "")
        if(pathstr=='[]'):#cancal upload file
            self.ids.my_image.source = 'galleryToCameraPage.png'
        else:
         self.ids.my_image.source=pathstr
         self.ids.next_button.disabled = False
        self.ids.camera_button.disabled = False
'''
 windows to pick a language and send all the information to process 
'''
class Lang(Screen):
    dropdown = DropDown()
    #initialization
    def  on_enter(self, *args):
        self.ids.ansLabel.text = ""  # Receiving a final answer
        Lang.hide_widget(self.ids.field, False)
        Lang.hide_widget(self.ids.startProcess, False)

        global dropdown
        lna = ["English", "Spanish", "Russian", "French"]

        menu_items = [
            {
                "viewclass": "IconListItem",
                "icon": "flag-outline",
                "font_name": "Sticky Notes.ttf",
                "height":dp(56),
                "text": f"{i}",
                "on_release": lambda x=f"{i}": self.set_item(x),
            }  for i in lna]
        #insert language to the dropDown
        dropdown = MDDropdownMenu(
            caller=self.ids.field,
            items=menu_items,
            position="bottom",
            width_mult=4,
        )
        dropdown.open()
 # After choosing language
    def set_item(self, text__item):
            self.ids.field.text = text__item
            self.ids.startProcess.disabled=False
            dropdown.dismiss()

    # for Hide Widget accroding our need
    def hide_widget(wid, dohide=True):
        if hasattr(wid, 'saved_attrs'):
            if not dohide:
                wid.height, wid.size_hint_y, wid.opacity, wid.disabled = wid.saved_attrs
                del wid.saved_attrs
        elif dohide:
            wid.saved_attrs = wid.height, wid.size_hint_y, wid.opacity, wid.disabled
            wid.height, wid.size_hint_y, wid.opacity, wid.disabled = 0, None, 0, True

    # Organize all the information accumulated from the user throughout the process and send for processing
    def startProcess(self):
      lang=self.ids.field.text#language
      allerg=AllergScreen.save_checked(self.manager.screens[2])#List of allergens
      path= self.manager.screens[1].ids.my_image.source#image
      whynot,caneat=codeProject.Answer_processing(allerg,path,lang)#sending to processing, return bool and list
      strAnswer=""
      if not caneat:
           strAnswer="       The product contains\n       these allergens from\n        your list: "
           strAnswer+=whynot
           strAnswer+="\n"+"           Do not eat!"
      else:
          strAnswer="      This product does not\n       contain products from\n                your list.\n              bon appetit!"

      self.ids.ansLabel.text=strAnswer#Receiving a final answer

      Lang.hide_widget(self.ids.field,True)
      Lang.hide_widget(self.ids.startProcess, True)
      if not caneat:
          self.ids.ansLabel.color=.54,.09,.09

      else:
          self.ids.ansLabel.color = .03, .6, .9, 1






class Identification_AllergensApp(MDApp):
    
    def build(self):
        self.icon = '2Eat.png'
        kv = Builder.load_file("main.kv")
        return kv





if __name__ == "__main__":
    Identification_AllergensApp().run()