from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.uix.popup import Popup
from kivy.properties import NumericProperty, StringProperty, ListProperty, BooleanProperty
from kivy.clock import Clock
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from random import random, randrange, randint
from datetime import datetime, timedelta, time

# words = ['Museum','Theme Park','Hospital']
with open('tutorial/words.txt','r') as f:
    words = f.read().splitlines()
class InitializeScreen(Screen):
    
    player_count = NumericProperty()
    word_randomization = BooleanProperty()
    selected_word = StringProperty()

    def initialize_options(self, size):
        size = int(size)
        app = App.get_running_app()
        if self.ids.randomize_word.active:
            word = self.t_in.text
        else:
            word = words[randint(0,2)].title()
        spy = randint(1,size) - 1
        print("Word: ",word)
        print("Spy: ",spy)
        app.spy = spy
        app.key = word
        self.manager.current = 'play'
        self.manager.get_screen('play').create_board(size)
        self.manager.get_screen('play').output_word()

    # def set_word(self):
    #     if self.randomize_word.active:
            
    def on_checkbox_active(self,active,*args):
        print(active)
        if active:
            # print(self.ids.randomize_word)
            # print(self.children.__dir__())
            self.t_in = TextInput()
            self.ids.blayout_1_2.add_widget(self.t_in)
        else:
            self.ids.blayout_1_2.remove_widget(self.t_in)
        


    def update_player_label(self,param):
        self.player_count = param


class VoteScreen(Screen):
    

    pass
    

    
class MainMenuScreen(Screen):

    pass

class StartGameScreen(Screen):
    pass

class ActivePlayScreen(Screen):
    display_clock = StringProperty("")

    def __init__(self,*args,**kwargs):
        super().__init__(**kwargs)
        
        

    def initialize_timer(self,player_count=7):
        
        starting_minutes = time(0,player_count,0)
        self.display_clock = starting_minutes.strftime("%M:%S")
        
    
    def on_enter(self,*args,**kwargs):
        Clock.unschedule(self.countdown)
        Clock.schedule_interval(self.countdown,1)
        

    def countdown(self,*args,**kwargs):
        s_time = datetime.strptime(self.display_clock,"%M:%S")
        n_time = s_time - timedelta(seconds=1)
        self.display_clock = n_time.strftime("%M:%S")

    
    
    

class SettingsScreen(Screen):

    pass

class CustomPopup(Popup):
    def __init__(self,obj,**kwargs):
        super().__init__(**kwargs)
        self.obj = obj

class PlayerCard(Button):
    
    def __init__(self,role,index,*args,**kwargs):
        super().__init__(**kwargs)
        self.role = role
        self.index = index

    def display(self,*args,**kwargs):
        
        app = App.get_running_app()

        content =Button(text=self.role)
        #Card Flip Animation
        pop = Popup(title='Popup Test',
                    content=content,size_hint = (.7,.7),auto_dismiss=False)
        
        pop2 = CustomPopup(title='Pass The Phone', size_hint = (.7,.7),content=Label(text='Pass The Phone'),obj=self.parent.parent)
        content.bind(on_press=pop.dismiss)
        pop.bind(on_dismiss=pop2.open)
        
        pop.open()
        self.disabled = True

        app.disable_check[self.index] = True
        print("Index: ", app.disable_check)
        
        Clock.schedule_once(pop2.dismiss,2)
        
        

        
        

class PlayScreen(Screen):
    
    

    def create_board(self,size):
        
        app = App.get_running_app()
        print("App Word ",app.key)
        print(app.spy)
        b = BoxLayout(orientation='vertical')
        l = Label(text='Selct Player Card')
        g = GridLayout(cols=2)
        legend = [app.key for i in range(size)]
        print("Legend: ", legend)
        legend[app.spy] = 'Spy'
        for i in range(size):
            print(i, legend[i])

            g.add_widget(PlayerCard(index=i,text=f"Player {i+1}",role=legend[i]))
            app.disable_check.append(False)
        b.add_widget(l)
        b.add_widget(g)
        self.add_widget(b)
        


        
        
    def output_word(self):
        app = App.get_running_app()
        print(app.key)
    


class SpyPlusApp(App):

    def __init__(self,*args,**kwargs):
        super().__init__(**kwargs)
        # self.key =''
        # self.spy = ''
        # self.word = ''

    key = StringProperty("")
    spy = NumericProperty(0)
    word = StringProperty("")
    disable_check = ListProperty()

    def check_to_start_game(self):
        app = App.get_running_app()
        if all(app.disable_check):
            self.root.current = 'start-screen'


    def build(self):
        sm = ScreenManager()

        sm.add_widget(MainMenuScreen(name='main-menu'))
        sm.add_widget(InitializeScreen(name='initialize-menu'))
        
        sm.add_widget(StartGameScreen(name='start-screen'))
        sm.add_widget(PlayScreen(name='play'))

        sm.add_widget(ActivePlayScreen(name='game'))
        sm.add_widget(VoteScreen(name='vote'))
        sm.add_widget(SettingsScreen(name='settings'))

        return sm
    
if __name__ == '__main__':
    SpyPlusApp().run()

