# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 01:52:51 2023

@author: Giovanny Montes R. & Manuel González Camacho

"""

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.label import Label
from kivy.utils import platform
import time,os
import cv2
import numpy as np
from model import TensorFlowModel

from kivy.lang import Builder
Builder.load_file('cnnh2.kv')


class MainScreen(Screen):

    def go_to_screen(self):
        self.manager.current = 'opciones'


class Camara(Screen):

    def capture_image(self):
        Camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        if platform=="android":            
            file_path = "/storage/emulated/0/DCIM/Camera/IMG_{}.png".format(timestr)
        else:
            file_path = "IMG_{}.png".format(timestr)    
        Camera.export_to_png(file_path)
        app = App.get_running_app()
        app.selected_file = file_path


    def refresh_camera(self, instance):
        self.camera.play = False
        self.camera.play = True

    def go_to_screen(self):
        app = App.get_running_app()
        if app.selected_file:
            self.manager.current = 'Resultados'
        else:
            print("No se seleccionó la imagen")
            self.manager.current = 'opciones'


class Resultados(Screen):
    def __init__(self, **kwargs):
        super(Resultados, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.add_widget(self.layout)

    def on_pre_enter(self, *args):
        app = App.get_running_app()
        self.layout.clear_widgets()
        if app.selected_file:
            image_path=app.selected_file
            self.predict_image(image_path)
   
    def predict_image(self,image_path):
        
        lista_clases = ["Quemadura de la hoja", "Mancha angular", "Antracnosis",
                        "Deficiencia de calcio", "Moho gris", "Hoja saludable",
                        "Fruta saludable", "Viruela", "Oídio en fruta",
                        "Oídio en hoja"]
        app = App.get_running_app()
        model=app.mod
        img = cv2.imread(image_path)
        img_arr = np.array(cv2.resize(img,(224, 224)), np.float32)
        img_arr = img_arr[:, :, :3]
        img_arr = np.expand_dims(img_arr, axis=0)
        probabilidades=model.pred(img_arr)[0]
        dic_clases = dict(enumerate(lista_clases))

        # Primer bloque: Mostrar imagen

        image_block = BoxLayout(orientation='vertical')
        pre = Image(source=image_path,fit_mode="fill")#cambio aquí 
        image_block.add_widget(pre)
        self.layout.add_widget(image_block)

        # Segundo bloque: Etiqueta label
        label_block = BoxLayout(orientation='vertical',size_hint=(1,0.1))
        label_text = "Clase: {0}".format(dic_clases[np.argmax(probabilidades)])
        label1 = Label(text=label_text)
        label_block.add_widget(label1)
        self.layout.add_widget(label_block)

        # Tercer bloque: Otra etiqueta label1
        probability_block = BoxLayout(orientation='vertical',size_hint=(1,0.1))
        label_text = "Probabilidad de: {:.0%}".format(np.max(probabilidades))
        label2 = Label(text=label_text)
        probability_block.add_widget(label2)
        self.layout.add_widget(probability_block)
        
        # Cuarto bloque: Mas opciones
        opcion = BoxLayout(orientation='vertical',size_hint=(1,0.3))
        op1=Button(text="Salir", on_press=app.stop)
        opcion.add_widget(op1)
        op2=Button(text="Intentar de nuevo", on_press=self.go_to_screen)       
        opcion.add_widget(op2)
        self.layout.add_widget(opcion)

    def go_to_screen(self, instance):
        self.manager.current = 'opciones'

class Opciones(Screen):
    def go_to_screen1(self):
        self.manager.current = 'navegador'

    def go_to_screen2(self):
        self.manager.current = 'Camara'


class Navegador(Screen):

    def __init__(self, **kwargs):
        super(Navegador, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        if platform == 'android':
            ruta = r"/storage/emulated/0/DCIM/Camera"
        else:
            ruta = os.getcwd()
        self.file_chooser = FileChooserListView(path=ruta)
        self.select_button = Button(text='Imágen:Seleccionar/Quitar', size_hint=(1, 0.2), on_press=self.select_image)
        self.listo_boton = Button(text='Continuar', size_hint=(1, 0.2), on_press=self.go_to_screen3)
        self.layout.add_widget(self.file_chooser)
        self.layout.add_widget(self.select_button)
        self.add_widget(self.layout)

    def select_image(self, instance):           
        app = App.get_running_app()
        
        app.selected_file = self.file_chooser.selection and self.file_chooser.selection[0]  # Obtener la imagen seleccionada
        
        if app.seleccion==0:
            if app.selected_file:
                try:
                    self.image = Image(source=app.selected_file,fit_mode="fill")
                    # Mostrar la imagen seleccionada
                    self.layout.add_widget(self.image)
                    self.layout.add_widget(self.listo_boton)
                    app.seleccion=1
                except:
                    print("No seleccionó una imágen")
                    self.manager.current = "navegador"
            else: 
                print("no ha seleccionado una imágen")
        else:
        
           self.layout.remove_widget(self.image)
           self.layout.remove_widget(self.listo_boton)
           self.manager.current = "navegador"
           app.seleccion=0


    def go_to_screen3(self, instance):
        self.manager.current = 'Resultados'
        self.layout.remove_widget(self.image)
        self.layout.remove_widget(self.listo_boton)


class CNNHApp(App):
    selected_file = None  # Variable global para almacenar la imagen seleccionada
    seleccion=0
    mod = TensorFlowModel()
    mod.load(os.path.join(os.getcwd(),"model.tflite"))
    def build(self):
        Window.size = (1080, 2400)
        Window.fullscreen = "auto"  
        sm = ScreenManager()
        main_screen = MainScreen(name='MainScreen')
        camera = Camara(name='Camara')
        res = Resultados(name="Resultados")
        op = Opciones(name="opciones") 
        nav = Navegador(name="navegador")
        sm.add_widget(main_screen)
        sm.add_widget(op)
        sm.add_widget(nav)
        sm.add_widget(res)
        sm.add_widget(camera)
             
        return sm 



if __name__ == '__main__':
    CNNHApp().run()

