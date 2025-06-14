from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.screenmanager import FadeTransition
# Dans main.py, avant de charger le KV
from kivy.factory import Factory
from kivy.uix.screenmanager import FadeTransition
Factory.register('FadeTransition', FadeTransition)
from kivymd.uix.list import OneLineListItem

import sqlite3
import time

#Modifier le six mai 2025

    
class Parking(MDApp):
    def build(self):
        main = Builder.load_file("main1.kv")
        self.Indice = 0
        self.Liste2 = ("","","","","") #Au cas cette truple ne contiendra pas de valeurs
        return main
    
    def page2(self,instance):
        self.root.ids.cr.transition = FadeTransition(clearcolor = [1,1,1,1])
        self.root.ids.cr.current = "Page2"
    
    def add(self,instance):
        self.root.ids.TopBar.title = "Ajout"
        self.root.ids.cr.current = "Page3"
    
    def enlever(self,instance):
        with sqlite3.connect("nom.db") as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS personne (nom TEXT, dates TEXT,heurs TEXT)")
            cur = conn.execute("SELECT nom,dates,heurs FROM personne")
            liste = cur.fetchall()
        if len(liste) == 0:
            self.show_info(Message="Il n'y pas de moto")
        else:
            self.Entry2()
    
    def Sombre_jour(self,instance):
        self.change()
        self.theme_cls.theme_style = "Dark" if self.theme_cls.theme_style == "Light" else "Light"
    
    def change(self):
        if self.theme_cls.theme_style == "Dark":
            self.root.ids.TopBar.right_action_items = [["weather-sunny",lambda x:self.Sombre_jour(x)],["text-box"],["information"]]
        else:
            self.root.ids.TopBar.right_action_items = [["weather-night",lambda x:self.Sombre_jour(x)],["text-box",lambda x : self.Couleur(x)],["information" , lambda x : self.Information(x)]]   
    
    def HEURS(self,instance):
        Time = f"Heurs : {time.strftime('%T')}\nDate : {time.strftime('%D')}"
        self.show_info(Message=Time)
        
    def Information(self,instance):
        Texte = "Code : Gestion de Parking \n Author : Elisée ATIKPO \n Lien github : ---"
        self.show_info(Message=Texte)
    
    def MENU(self,instance):
        self.show_info(Message="Pas de Menu")
    
    def Back(self,instance):
        Page = self.root.ids.cr.current
        nbt = int(Page[-1]) -1 
        if nbt == 0:
            self.stop()
        elif nbt != 3:
            self.root.ids.cr.current = f"Page{nbt}"
        else:
            self.root.ids.cr.current = "Page2"
            
    def Couleur(self,instance):
        Liste = ['Red', 'Pink', 'Purple', 'DeepPurple', 'Indigo', 'Blue', 'LightBlue', 'Cyan', 'Teal', 'Green', 'LightGreen', 'Lime', 'Yellow', 'Amber', 'Orange', 'DeepOrange', 'Brown', 'Gray', 'BlueGray']
        self.Indice += 1
        if self.Indice == len(Liste):
            self.Indice = 0
        #self.Indice %= len(Liste)
        self.theme_cls.primary_palette = Liste[self.Indice]
        
    def Entry2(self):
        self.Entryy = MDTextField(
            hint_text = "Plaque",
            mode = "rectangle",
            halign = "center",
        )
        
        self.Ok = MDDialog(
            title = "Plaque",
            content_cls = self.Entryy,
            type = "custom",
            buttons = [
                MDRaisedButton(
                    text = "[b]Annuler[/b]",
                    md_bg_color =  [1,0,0,1],
                    on_release= self.Ann,
                ),
                MDRaisedButton(
                    text = "[b]Valider[/b]",
                    md_bg_color =  [0,1,0,1],
                    on_release= self.Val1,
                )
            ]
        )
        self.Ok.open()
    
    def Val1(self,instance):
        texte = self.Entryy.text
        if texte == "":
            self.Entryy.error = True
            self.Entryy.helper_text = "Ce champs est Obligatoire"
        else:
            with sqlite3.connect("nom.db") as conn:
                conn.execute("CREATE TABLE IF NOT EXISTS personne (nom TEXT, dates TEXT,heurs TEXT)")
                cusor = conn.execute("SELECT nom,dates,heurs FROM personne")
                liste = cusor.fetchall()
            exist = False
            for elmt in liste:
                if elmt[0] == texte:
                    #Ici la page 3
                    dates , heurs = time.strftime('%D'),time.strftime('%T')
                    LAB = self.root.ids.Lab
                    self.Liste2 = (elmt[0],elmt[1],elmt[2],dates,heurs)
                    if dates == elmt[1]:
                        times = heurs.split(":") 
                        if int(times[0]) == 0:
                            times[0] = "24"
                        times_fin = int(times[0])*3600 + int(times[1])*60 + int(times[2])
                       
                        times = elmt[2].split(':')
                        if int(times[0]) == 0:
                            times[0] = "24"
                        times_dep = int(times[0])*3600 + int(times[1])*60 + int(times[2])
                        times = times_fin - times_dep
                        times /= 3600
                        if times > 10:
                            LAB.text = "100"
                        else:
                            LAB.text = "50"
                    else:
                        Dates = elmt[1].split("/") 
                        dates = dates.split("/")
                        if Dates[2] == dates[2]:
                            if Dates[1] == dates[1]:
                                    Jours = int(dates[0]) - int(Dates[0])
                                    if Jours <= 2:
                                        LAB.text = "200"
                                    elif 2< Jours <= 5:
                                        LAB.text = "350"
                                    elif 5 < Jours < 10:
                                        LAB.text= "450"
                                    else:
                                        LAB.text = "600"
                            else:
                                Mois = int(dates[1]) - int(Dates[1])
                                if Mois <= 2:
                                    LAB.text = "800"
                                elif 2<Mois <= 5:
                                    LAB.text = "800"
                                else:
                                    LAB.text='1500'
                        else:
                            Years = int(dates[2]) - int(Dates[2])
                            LAB.text = str(5000*Years)
                                        
                    self.Ok.dismiss()
                    self.root.ids.cr.current = "Page3"
                    exist = True
                    
            if not exist:
                self.Entryy.error = True
                self.Entryy.helper_text = "Cette plaque n'a pas été enregistré !"
                
    def remove(self,instance):
        with sqlite3.connect("nom.db") as conn:
            cur = conn.execute("SELECT nom,dates,heurs FROM personne") 
            Liste = cur.fetchall()
        
        for elmt in Liste:
            if elmt[0] == self.Entryy.text:
                Liste.remove(elmt)
        
        with sqlite3.connect("nom.db") as conn:
            conn.execute("DELETE FROM personne")  
        
        with sqlite3.connect("nom.db") as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS personne (nom TEXT , dates TEXT , heurs TEXT)")
            for elmt in Liste:
                conn.execute("INSERT INTO personne VALUES (?,?,?)",elmt) 
        
        with sqlite3.connect('Hist.db') as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS histoire (nom TEXT,dates1 TEXT , heurs1 TEXT , dates2 TEXT , heurs2 TEXT)")
            conn.execute("INSERT INTO histoire VALUES (?,?,?,?,?)",self.Liste2)
        #6 mai 2025
        
        self.show_info(Message = self.Entryy.text + " est retiré avec sucess !")  
        self.root.ids.cr.current = "Page2"   
    
    def show_histy(self,instance):
        with sqlite3.connect("Hist.db") as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS histoire (nom TEXT,dates1 TEXT , heurs1 TEXT , dates2 TEXT , heurs2 TEXT)")
            cur = conn.execute("SELECT nom,dates1,heurs1,dates2,heurs2 FROM histoire")
            self.Liste3 = cur.fetchall()
        
        if len(self.Liste3) == 0:
            self.show_info(Message="Pas d'histoire")
        else:
            self.root.ids.cr.current = "Page4" #Aller a la page 4
            Pge = self.root.ids.Liste
            for elmt in self.Liste3:
                wid = OneLineListItem(
                    text = elmt[0],
                    on_release= lambda x : self.info(elmt),
                )
                Pge.add_widget(wid)
            
    def info(self,value):
        texte = f"Plaque : {value[0]} \nDate d'arrivé : {value[1]} \n Heurs d'arrivé : {value[2]} \nDate de depart : {value[3]} \n Heurs de depart : {value[4]}"
        self.root.ids.Lab2.text = f'{texte}'
        self.root.ids.Nav.set_state("toggle")
        
    def Entry(self,instance):
        self.Entryy = MDTextField(
            hint_text = "Plaque",
            mode = "rectangle",
            halign = "center",
        )
        
        self.Ok = MDDialog(
            title = "Plaque",
            content_cls = self.Entryy,
            type = "custom",
            buttons = [
                MDRaisedButton(
                    text = "[b]Annuler[/b]",
                    md_bg_color =  [1,0,0,1],
                    on_release= self.Ann,
                ),
                MDRaisedButton(
                    text = "[b]Valider[/b]",
                    md_bg_color =  [0,1,0,1],
                    on_release= self.Val,
                )
            ]
        )
        self.Ok.open()
    
    def Ann(self,instance):
        self.Ok.dismiss()
    
    def Val(self,instance):
        texte = self.Entryy.text
        if texte == "":
            self.Entryy.error = True
            self.Entryy.helper_text = "Ce champs est Obligatoire"
        else:
            with sqlite3.connect("nom.db") as conn:
                conn.execute("CREATE TABLE IF NOT EXISTS personne (nom TEXT, dates TEXT,heurs TEXT)")
                cusor = conn.execute("SELECT nom,dates,heurs FROM personne")
                liste = cusor.fetchall()
            exist = False
            for elmt in liste:
                if elmt[0] == texte:
                    self.Entryy.error = True
                    self.Entryy.helper_text = "Cette plaque existe déjà"
                    exist = True
            if not exist:
                texte = (texte,time.strftime("%D"),time.strftime("%T"))
                try:
                    with sqlite3.connect("nom.db") as conn:
                        conn.execute("CREATE TABLE IF NOT EXISTS personne (nom TEXT, dates TEXT,heurs TEXT)")
                        conn.execute("INSERT INTO personne VALUES (? , ? , ?)",texte)
                    self.show_info(Message = texte[0] + " est ajouter succes !")
                    self.Ok.dismiss()
                except:
                    self.show_info(Message = "Quelque chose s'est mal passé !")
    
    def show_info(self,Message):
        self.DD = MDDialog(
            title = "Info",
            text = Message,
            buttons = [
                MDRaisedButton(
                    text = "[b]Ok[/b]",
                    on_release = self.OK,
                )
            ]
        )       
        self.DD.open()
        
    def OK(self,instance):
        self.DD.dismiss()
Parking().run()