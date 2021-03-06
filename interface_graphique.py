from tkinter import *
import manipulate_json as jm


class Main_Window():

    def __init__(self, player_name):

        self.main_window = Tk()

        self.main_window.title("Bloks")
        self.main_window.resizable(False, False)
        self.main_window.iconbitmap("img/icone.ico")

        self.main_window.option_add('*Font', 'Constantia 12')
        self.main_window.option_add('*Button.relief', 'flat')
        self.main_window.option_add('*Button.overRelief', 'ridge')
        self.main_window.option_add('*justify', 'left')
        # self.backgroundcolor='#8BD8BD'
        # self.foregroundcolor='#243665'
        self.backgroundcolor = "#292826"
        self.foregroundcolor = "#F9D342"

        self.aabg = "#3F3E3B"
        self.aaborder = self.foregroundcolor
        self.aaline = "#8E38F7"
        self.aahitbox = "#FF5C56"

        self.main_window.option_add('*background', self.backgroundcolor)
        self.main_window.option_add('*foreground', self.foregroundcolor)
        self.main_window.option_add('*compound', 'left')

        # self.main_window.configure(bg='gray')
        self.main_window.attributes("-fullscreen", True)


        # Actuellement : 1280 * 720
        #self.main_canvas = Canvas(self.main_window,width=16*80,height=9*80)
        # self.main_canvas.pack(expand=True,fill="both")

        # Actuellement : 1280 * 560
        self.game_canvas = Canvas(
            self.main_window, width=16 * 80, height=7 * 80)
        self.game_canvas.pack(expand=True, fill="both")
        self.game_canvas.update()

        height = self.game_canvas.winfo_height()
        width = self.game_canvas.winfo_width()

        import outputbox
        self.outputbox = outputbox.OutputBox(
            canvas=self.game_canvas, x=width - 300, y=height - 300 - 200, height=300, width=300)
        self.outputbox.show()

        self.myMap = None
        self.combat = False

        self.player_dic = jm.load_file(
            filename='player_dic', player_name=player_name)
        self.spell_dic = jm.load_file(
            filename='spell_dic', player_name=player_name)
        self.attribut_dic = jm.load_file(
            filename='attribut_dic', player_name=player_name)
        self.inventory_dic = jm.load_file(
            filename='inventory_dic', player_name=player_name)

        self.draw_menu()

    # Une fonction qui DOIT ne rien renvoyer
    # Elle sera utilisée régulièrement, quand un changement est effectué "globalement dans les dictionnaires", mais pas réellement dans le disque
    def save_all(self, *args):
        import manipulate_stats as ms

        self.player_dic = ms.calculate_playerstats(
            attribut_dic=self.attribut_dic, player_dic=self.player_dic)

        jm.save_file(self.player_dic, filename='player_dic',
                     player_name=self.player_dic['name'])
        jm.save_file(self.attribut_dic, filename='attribut_dic',
                     player_name=self.player_dic['name'])
        jm.save_file(self.inventory_dic, filename='inventory_dic',
                     player_name=self.player_dic['name'])
        jm.save_file(self.spell_dic, filename='spell_dic',
                     player_name=self.player_dic['name'])

        self.outputbox.add_text('Everything has been saved')

    # Une fonction qui DOIT ne rien renvoyer
    def reload_everything(self, *args):
        import manipulate_stats as ms

        self.player_dic = ms.calculate_playerstats(
            attribut_dic=self.attribut_dic, player_dic=self.player_dic)

        self.player_dic = jm.load_file(
            filename='player_dic', player_name=self.player_dic['name'])
        self.spell_dic = jm.load_file(
            filename='spell_dic', player_name=self.player_dic['name'])
        self.attribut_dic = jm.load_file(
            filename='attribut_dic', player_name=self.player_dic['name'])
        self.inventory_dic = jm.load_file(
            filename='inventory_dic', player_name=self.player_dic['name'])
        self.used_objects = jm.load_file(filename="used_objects",player_name=self.player_dic['name'])

        self.outputbox.add_text('Everything has been loaded')


    ## Menu canvas related functions ##

    def draw_menu(self):
        height = self.game_canvas.winfo_height()
        self.StatsButton = Button(
            self.game_canvas, text="Stats", command=self.openstatwindow)
        self.StatsButton.place(x=50, y=height - 50, anchor='s')

        self.AttributButton = Button(
            self.game_canvas, text="Attributs", command=self.openattributwindow)
        self.AttributButton.place(x=50 + 150, y=height - 50, anchor='s')

        self.SpellMenuButton = Button(
            self.game_canvas, text="Spells", command=self.openspellwindow)
        self.SpellMenuButton.place(x=50 + 300, y=height - 50, anchor='s')

        self.InventoryButton = Button(
            self.game_canvas, text="Inventaire", command=self.openinventorywindow)
        self.InventoryButton.place(x=50 + 450, y=height - 50, anchor='s')

        self.LevelupButton = Button(
            self.game_canvas, text="Level Up", command=self.openlevelupwindow)
        self.LevelupButton.place(x=50 + 600, y=height - 50, anchor='s')

    def openstatwindow(self):
        import stats_window as sw

        x = self.game_canvas.winfo_width() / 4
        y = self.game_canvas.winfo_height() / 4 - 100

        w = sw.StatsWindow(toplevel=True)
        w.show(stat_dic=self.player_dic['stats'], name=self.player_dic['name'],
               level=self.player_dic['level'], image_dir=self.player_dic['image'], x_relative=x, y_relative=y)

    def openspellwindow(self):
        import spell_window as spw

        x = self.game_canvas.winfo_width() / 4
        y = self.game_canvas.winfo_height() / 4 - 100

        w = spw.SpellWindow(toplevel=True)
        w.show(player_dic=self.player_dic, spell_dic=self.spell_dic,
               function=self.save_all, x_relative=x, y_relative=y)

    def openinventorywindow(self):
        import inventory_window as iw

        x = self.game_canvas.winfo_width() / 4
        y = self.game_canvas.winfo_height() / 4 - 100

        w = iw.InventoryWindow(toplevel=True, player_dic=self.player_dic, inventory_dic=self.inventory_dic,
                               attribut_dic=self.attribut_dic, function=self.save_all, x_relative=x, y_relative=y)

    def openattributwindow(self):
        import attribut_window as aw

        x = self.game_canvas.winfo_width() / 4
        y = self.game_canvas.winfo_height() / 4 - 100

        w = aw.AttributWindow(toplevel=True)
        w.show(player_dic=self.player_dic, attribut_dic=self.attribut_dic,
               function=self.save_all, x_relative=x, y_relative=y)

    def openlevelupwindow(self):
        import levelup_window as luw

        x = self.game_canvas.winfo_width() / 4
        y = self.game_canvas.winfo_height() / 4 - 100

        w = luw.Levelup_Window(toplevel=True, player_dic=self.player_dic,
                               attribut_dic=self.attribut_dic, function=self.save_all, x_relative=x, y_relative=y)


    ## Map-related functions ##
    import manipulate_map as mm

    def load_map(self, mapdir, mapname, tilename, imgdir):
        used_objects = jm.load_file(filename="used_objects",player_name=self.player_dic['name'])
        self.myMap = mm.load_map(mapdir=mapdir, mapname=mapname, tilename=tilename, imgdir=imgdir, used_objects=used_objects)

    def load_player(self, player_imgdir):
        import manipulate_showplayer as msp
        self.player_image = PhotoImage(file=player_imgdir)
        self.showplayer = msp.ShowPlayer(window=self.main_window,
                                         myMap=self.myMap,
                                         game_canvas=self.game_canvas,
                                         player_name = self.player_dic['name'],
                                         player_photoimage=self.player_image,
                                         outputbox=self.outputbox,
                                         x_limit=self.myMap.x_limit,
                                         y_limit=self.myMap.y_limit)

    def test(self, event):
        self.outputbox.add_text(text=f"{event.x},{event.y}")

    def clear_map(self):
        self.game_canvas.delete('all')
        self.showplayer.turn_bind_off()

    # La fonction draw_map doit prendre en argument seulement les x,y du bloc tout en haut à gauche de l'écran
    # Attention : x et y sont en "numéro de bloc"
    # 1,1 correspond donc au bloc en haut à gauche ligne 1 colonne 1
    # Ainsi, si x_debut = 0.5, on ne voit affiché que la moitié (en x) du bloc en haut à gauche
    def draw_map(self, x_debut, y_debut):
        if self.myMap is None:
            return()

        self.myMap.draw_map(canvas=self.game_canvas,
                            x_debut=x_debut, y_debut=y_debut)

    def draw_player(self, x_debut, y_debut):

        self.showplayer.draw(x_map=x_debut, y_map=y_debut)

        self.game_canvas.bind_all('<Left>', self.showplayer.move_left)
        self.game_canvas.bind_all('<Right>', self.showplayer.move_right)
        self.game_canvas.bind_all('<Up>', self.showplayer.move_up)
        self.game_canvas.bind_all('<Down>', self.showplayer.move_down)
        self.game_canvas.bind_all('<e>',self.testcheck)

        self.game_canvas.bind_all('<Button-1>', self.test)
        self.game_canvas.bind_all('<p>', self.test_play)
        self.game_canvas.bind_all('<c>', self.test_combat)
        self.game_canvas.bind_all('<f>', self.test_fuite)
        self.game_canvas.bind_all('<a>', self.test_attaque)
        self.game_canvas.bind_all('<space>', self.test_stoptheline)
        self.game_canvas.bind_all('<d>', self.test_defense)
        self.game_canvas.bind_all('<s>', self.test_spell)

        self.game_canvas.bind_all('<?>', self.test_help)
        self.outputbox.add_text(text=f"Appuie <?> pour afficher l'aide")

        self.showplayer.turn_bind_on()

    def testcheck(self, *args):
        self.showplayer.check_for_everything()

    def test_help(self, *args):
        self.outputbox.add_text(text="\n")
        self.outputbox.add_text(text=f"Appuie sur <c> pour démarrer un combat")
        self.outputbox.add_text(text=f"Appuie sur <f> pour fuire le combat")
        self.outputbox.add_text(text=f"Appuie sur <a> pour attaquer en combat")
        self.outputbox.add_text(
            text=f"Appuie sur ESPACE pour arrêter la barre")
        self.outputbox.add_text(text=f"Appuie sur <d> pour défendre en combat")
        self.outputbox.add_text(
            text=f"Appuie sur <s> pour lancer un sort en combat")
        self.outputbox.add_text(text=f"Appuie <?> pour afficher l'aide")

    def test_play(self, *args):
        if not self.combat:
            return
        try:
            if self.playbutton['state'] == 'normal' and self.playbutton['text'] == '(P)LAY':
                self.function_play_button()
            elif self.playbutton['state'] == 'normal' and self.playbutton['text'] == '(P)QUIT':
                self.player_wincombat()
            elif self.playbutton['state'] == 'normal' and self.playbutton['text'] == "(P)Quitter le combat":
                self.hide_combat()
            else:
                self.outputbox.add_text(text=f"Pas maintenant !")
        except Exception as e:
            self.outputbox.add_text(text=f"Erreur : {e}")

    def test_combat(self, *args):
        if not self.combat:
            monster_dic = jm.load_file(
                fulldir="ressources/template/monster/slime_rouge.json")

            self.show_combat(monster_dic=monster_dic)

    def test_fuite(self, *args):
        if not self.combat:
            return
        try:
            if self.fleebutton['state'] == 'normal':
                self.player_tryfleecombat()
            else:
                self.outputbox.add_text(
                    text=f"Vous ne pouvez pas fuire maintenant.")
        except Exception as e:
            self.outputbox.add_text(text=f"Erreur : {e}")

    def test_attaque(self, *args):
        if not self.combat:
            return
        try:
            if self.attackbutton['state'] == 'normal':
                self.player_attack()
            else:
                self.outputbox.add_text(
                    text=f"Vous ne pouvez pas attaquer maintenant.")
        except Exception as e:
            self.outputbox.add_text(text=f"Erreur : {e}")

    def test_stoptheline(self, *args):
        if not self.combat:
            return
        try:
            self.attackbar.stoptheline()
        except Exception as e:
            self.outputbox.add_text(text=f"Erreur : {e}")

    def test_defense(self, *args):
        if not self.combat:
            return
        try:
            if self.defendbutton['state'] == 'normal':
                self.player_defend()
            else:
                self.outputbox.add_text(
                    text=f"Vous ne pouvez pas défendre maintenant.")
        except Exception as e:
            self.outputbox.add_text(text=f"Erreur : {e}")

    def test_spell(self, *args):
        if not self.combat:
            return
        try:
            if self.spellbutton['state'] == 'normal':
                self.player_spell()
            else:
                self.outputbox.add_text(
                    text=f"Vous ne pouvez pas lancer un sort maintenant.")
        except Exception as e:
            self.outputbox.add_text(text=f"Erreur : {e}")
    def draw_everything(self, x_debut=None, y_debut=None):
        if x_debut is None or y_debut is None:
            x_debut, y_debut = self.showplayer.coords()
            if x_debut is None or y_debut is None:
                raise Exception(
                    "Impossible de draw player sans avoir de coordonnées !")
        self.draw_map(x_debut, y_debut)
        self.draw_player(x_debut, y_debut)


    ## Combat-related functions ##

    def show_combat(self, monster_dic):
        import healthbar
        import speedbar
        import outputbox
        import spellbar
        import attackbar
        import manipulate_stats as ms

        # Efface la map
        self.clear_map()

        # Désactive tous les boutons de Menu inutiles
        self.AttributButton.config(state=DISABLED)
        self.SpellMenuButton.config(state=DISABLED)
        self.InventoryButton.config(state=DISABLED)
        self.LevelupButton.config(state=DISABLED)

        self.combat = True
        self.playerturn = False
        self.defending = False

        self.monster_dic = monster_dic

        # Ces 3 dictionnaires pourront bouger en plein combat, et sont recréés pour les manipuler
        self.player_stats = self.player_dic['stats']
        self.equipped_list = self.player_dic['equipped_list']
        self.number_of_weapons = ms.number_of_weapons(self.player_dic)

        # self.game_canvas

        x_playerhealth = 20
        y_label = 20

        self.player_label = Label(self.game_canvas,
                                  text=f"{self.player_dic['name']}", font="Constantia 13 bold")
        self.player_label.place(x=x_playerhealth, y=y_label)

        y_healthbar = y_label + 25

        hpmax = self.player_stats['HP']
        self.player_healthbar = healthbar.HealthBar(canvas=self.game_canvas, length=200, height=25, maximum=hpmax, x=x_playerhealth,
                                                    y=y_healthbar, color="red", backgroundcolor=self.backgroundcolor, bordercolor=self.foregroundcolor)
        self.player_healthbar.show()

        self.bind_player_tooltip()

        height = self.game_canvas.winfo_height()
        width = self.game_canvas.winfo_width()

        x_monster_label = width - 220
        self.monster_label = Label(self.game_canvas,
                                   text=f"{self.monster_dic['name']}", font="Constantia 13 bold")
        self.monster_label.place(
            x=x_monster_label + 200, y=y_label, anchor='ne')

        hpmax = self.monster_dic['stats']['HP']
        self.monster_healthbar = healthbar.HealthBar(canvas=self.game_canvas, length=200, height=25, maximum=hpmax, x=x_monster_label,
                                                     y=y_healthbar, color="red", backgroundcolor=self.backgroundcolor, bordercolor=self.foregroundcolor, special="right")
        self.monster_healthbar.show()
        self.bind_monster_tooltip()

        # joueur en or, à gauche
        # monstre en rouge, à droite
        speed1 = self.player_stats['Agilité']
        speed2 = self.monster_dic['stats']['Agilité']
        x_speedbar = (x_playerhealth + x_monster_label) / 2 + 90
        self.speedbar = speedbar.SpeedBar(canvas=self.game_canvas, x=x_speedbar, y=20, length=200, max1=100, max2=100, speed1=speed1,
                                          speed2=speed2, color1="#FFFFFF", color2="red", backgroundcolor=self.backgroundcolor, bordercolor=self.foregroundcolor)
        self.speedbar.show()

        x_spellbar = width - 300
        y_spellbar = height - 200

        self.spellbar = spellbar.SpellBar(canvas=self.game_canvas, x=x_spellbar, y=y_spellbar, length=200, height=25, current_value=0,
                                          maximum=100, color="#EB2188", backgroundcolor=self.backgroundcolor, bordercolor=self.foregroundcolor, special="middle")
        self.spellbar.show()

        x_aa = x_playerhealth + 50
        y_aa = y_healthbar + 250

        dif_level = ms.attackbar_difficulty(self.player_dic['level'])
        self.outputbox.add_text(text=f"Difficulté : {dif_level}/20")
        self.attackbar = attackbar.AttackBar(canvas=self.game_canvas, x=x_aa, y=y_aa, width=800, height=300, difficulty_level=dif_level, backgroundcolor=self.aabg,
                                             backgroundbordercolor=self.aaborder, linecolor=self.aaline, linebordercolor=self.aaborder, hitboxcolor=self.aahitbox)
        self.attackbar.show()

        x_spellbutton = x_spellbar + 200
        self.spellbutton = Button(
            self.game_canvas, text="", state='disabled', command=self.player_spell)
        self.spellbutton.place(x=x_spellbar + 200, y=y_spellbar, anchor='nw')
        self.spell_is_active = False

        # self.game_canvas
        self.playbutton = Button(
            self.game_canvas, text="(P)LAY", command=self.function_play_button)
        self.playbutton.place(x=width - 400, y=height - 100, anchor='s')

        self.attackbutton = Button(
            self.game_canvas, text="(A)TTACK", state=DISABLED, command=self.player_attack)
        self.attackbutton.place(x=width - 250, y=height - 100, anchor='s')

        self.defendbutton = Button(
            self.game_canvas, text="(D)EFEND", state=DISABLED, command=self.player_defend)
        self.defendbutton.place(x=width - 100, y=height - 100, anchor='s')

        self.fleebutton = Button(
            self.game_canvas, text="(F)UIRE", state=DISABLED, command=self.player_tryfleecombat)
        self.fleebutton.place(x=width - 400, y=height - 50, anchor='s')

        self.order = None

    def function_play_button(self):
        self.showplayer.loop = False
        self.play_combat_loop()

        self.playbutton.config(text="(P)QUIT")
        self.playbutton.config(command=self.player_wincombat)

    def bind_player_tooltip(self):
        import stats_window as sw
        toolTip = sw.StatsWindow(widget=self.player_healthbar.widget)

        def enter(event):
            toolTip.show(stat_dic=self.player_stats,
                         name=self.player_dic['name'], level=self.player_dic['level'], image_dir=self.player_dic['image'], category='')

        def leave(event):
            toolTip.hidetip()
        self.player_healthbar.widget.bind('<Enter>', enter)
        self.player_healthbar.widget.bind('<Leave>', leave)

    def bind_monster_tooltip(self):
        import stats_window as sw
        toolTip = sw.StatsWindow(widget=self.monster_healthbar.widget)

        def enter(event):
            toolTip.show(stat_dic=self.monster_dic['stats'], name=self.monster_dic['name'], level=self.monster_dic['level'],
                         image_dir=self.monster_dic['image'], category=self.monster_dic['category'], x_relative=-500)

        def leave(event):
            toolTip.hidetip()
        self.monster_healthbar.widget.bind('<Enter>', enter)
        self.monster_healthbar.widget.bind('<Leave>', leave)
    def check_spellbar_progress(self, *args):
        try:
            if self.spellbar.current_value >= 100:
                self.spell_is_active = True
                self.spellbutton.config(state='disabled')
                self.spellbutton.config(text='(S)PELL')
            else:
                self.spell_is_active = False
                self.spellbutton.config(state='disabled')
                self.spellbuton.config(text="")
        except:
            pass

    def player_spell(self, *args):
        from manipulate_spells import cast_spell

        if self.defending:
            self.outputbox.add_text(
                text=f"Vous ne pouvez pas lancer un sort en vous défendant.")
            return()

        spell_number = self.spell_dic['active'].split('spell')[-1]

        self.spellbar.slowprogress(
            addvalue=-100, function=self.check_spellbar_progress)

        self.order = None
        self.playerturn = False
        self.speedbar.order = None
        self.attackbutton.config(state=DISABLED)
        self.defendbutton.config(state=DISABLED)
        self.fleebutton.config(state=DISABLED)
        self.spellbutton.config(state=DISABLED)

        cast_spell(spell_number=spell_number, player_stats=self.player_stats, monster_dic=self.monster_dic,
                   spell_dic=self.spell_dic, outputbox=self.outputbox, function=self.play_combat_loop)


    def play_combat_loop(self):
        self.order = self.speedbar.order

        if self.order == "wait":
            self.main_window.after(20, self.play_combat_loop)

        elif self.order is None:

            self.order = self.speedbar.lets_go()

            self.playbutton.config(state=DISABLED)
            self.main_window.after(20, self.play_combat_loop)

        # Tour du monstre
        elif self.order == 2:
            self.order = None
            self.speedbar.order = None
            self.main_window.after(500, self.monster_attack)

        # Tour du joueur
        elif self.order == 1:
            self.playerturn = True
            self.attackbutton.config(state=NORMAL)
            self.defendbutton.config(state=NORMAL)
            self.fleebutton.config(state=NORMAL)
            if self.spell_is_active:
                self.spellbutton.config(state=NORMAL)
            else:
                self.spellbutton.config(state=DISABLED)

        elif self.order == "stop":
            self.hide_combat()

    def player_defend(self):
        if (not self.combat) or (not self.playerturn):
            return

        # Le joueur s'enlève de l'état
        if self.defending:
            self.defending = False
            self.defendbutton.config(text="(D)EFEND")
        # Le jour se met dans l'état
        else:
            self.defending = True
            self.defendbutton.config(text="STOP (D)EFEND")

    def player_attack(self):
        if (not self.combat) or (not self.playerturn):
            return

        self.attackbutton.config(state=DISABLED)
        self.defendbutton.config(state=DISABLED)
        self.fleebutton.config(state=DISABLED)
        self.spellbutton.config(state=DISABLED)

        if self.number_of_weapons == 0:
            self.player_attack_suite(pourcentage_total=0)
        else:
            self.attackbar.start_animation(
                number_of_times=self.number_of_weapons, function=self.player_attack_suite)

    def player_attack_suite(self, pourcentage_total=0):
        import manipulate_stats as ms

        if self.defending:
            mult_damage = ms.player_multiplicateur_defense(
                player_stats=self.player_stats, attacking=True, receiving=False)
            self.outputbox.add_text(
                text=f"Vous tapez à hauteur de {100*mult_damage:0.1f}% de vos dégâts normaux en forme défensive")
        else:
            mult_damage = 1

        damage = ms.calculate_damage_player(player_stats=self.player_stats, monster_stats=self.monster_dic['stats'], player_itemlist=self.equipped_list,
                                            number_of_weapons=self.number_of_weapons, multiplicateur_defense=mult_damage, multiplicateur_attaque=pourcentage_total)
        spellbarprogress = ms.spellbar_progress(self.player_stats)

        self.monster_healthbar.take_hit(damage)
        self.spellbar.slowprogress(
            addvalue=spellbarprogress + 50, function=self.check_spellbar_progress)
        if damage > 1:
            s = 's'
        else:
            s = ''
        self.outputbox.add_text(
            f"{self.monster_dic['name']} a subi {damage:0.1f} dommage{s}")
        self.monster_dic['stats']['HP'] -= damage

        if self.monster_dic['stats']['HP'] < 0:
            self.outputbox.add_text(
                f"{self.monster_dic['name']} a été vaincu !")
            self.player_wincombat()

        else:
            self.order = None
            self.playerturn = False
            self.speedbar.order = None
            self.play_combat_loop()

    def monster_attack(self):
        if not self.combat:
            return

        if self.defending:
            self.attackbar.start_animation(
                number_of_times=1, function=self.monster_attack_suite)
        else:
            self.monster_attack_suite(pourcentage_total=0)

    def monster_attack_suite(self, pourcentage_total=0):
        import manipulate_stats as ms

        if self.defending:
            mult_defense = ms.player_multiplicateur_defense(
                player_stats=self.player_stats, attacking=False, receiving=True, pourcentage_total=pourcentage_total)
            self.outputbox.add_text(
                text=f"Vous ne prenez que {mult_defense*100:0.1f}% des dégâts en forme défensive")
        else:
            mult_defense = 1

        damage = ms.calculate_damage_monster(
            monster_stats=self.monster_dic['stats'], player_stats=self.player_stats, element=self.monster_dic['element'], multiplicateur_defense=mult_defense)

        self.player_healthbar.take_hit(damage)
        self.player_stats['HP'] -= damage
        if damage > 1:
            s = 's'
        else:
            s = ''
        self.outputbox.add_text(
            f"{self.player_dic['name']} a subi {damage:0.1f} dommage{s}")

        if self.player_stats['HP'] < 0:
            self.outputbox.add_text(
                f"{self.player_dic['name']} a été vaincu !")
            self.player_losecombat()

        else:
            self.order = None
            self.speedbar.order = None
            self.main_window.after(1500, self.play_combat_loop)

    def player_wincombat(self):
        self.speedbar.order = "stop"
        self.playerturn = False
        self.outputbox.add_text(
            f"Vous gagnez A IMPLEMENTER points d'expérience !")
        self.playbutton.config(text="(P)Quitter le combat")
        self.playbutton.config(state=NORMAL)
        self.playbutton.config(command=self.hide_combat)
        self.attackbutton.config(state=DISABLED)
        self.defendbutton.config(state=DISABLED)
        self.fleebutton.config(state=DISABLED)
        self.spellbutton.config(state=DISABLED)

    def player_losecombat(self):
        self.speedbar.order = "stop"
        self.playerturn = False
        self.outputbox.add_text(f"Vous êtes mort...")
        self.playbutton.config(text="(P)Quitter le combat")
        self.playbutton.config(state=NORMAL)
        self.playbutton.config(command=self.hide_combat)
        self.attackbutton.config(state=DISABLED)
        self.defendbutton.config(state=DISABLED)
        self.fleebutton.config(state=DISABLED)
        self.spellbutton.config(state=DISABLED)

    def player_tryfleecombat(self):
        if not self.combat or not self.playerturn:
            self.outputbox.add_text(f"Vous ne pouvez pas fuire maintenant.")
            return
        if self.defending:
            self.outputbox.add_text(f"Vous ne pouvez pas défendre en fuyant.")
            return

        from manipulate_stats import chance_fuite
        from random import random

        self.attackbutton.config(state=DISABLED)
        self.defendbutton.config(state=DISABLED)
        self.spellbutton.config(state=DISABLED)
        self.fleebutton.config(state=DISABLED)

        chance = chance_fuite(player_stats=self.player_stats,
                              monster_stats=self.monster_dic['stats'])
        r = random()

        self.outputbox.add_text(
            f"Vous avez {chance*100:0.0f}% de chance de fuire")
        self.outputbox.add_text(f"")

        # avec 100% de chance de fuite la condition est réalisée
        if chance >= r:
            self.aux_flee_loop(True, chance, 0)
        else:
            self.aux_flee_loop(False, chance, 0)

    def aux_flee_loop(self, success, chance, k):
        if k < 15:
            self.outputbox.concatenate_text("█")
            self.main_window.after(
                30, self.aux_flee_loop, success, chance, k + 1)
        else:
            self.player_fleecombat(success)
    def player_fleecombat(self, success):
        if success:
            self.speedbar.order = "stop"
            self.playerturn = False
            self.outputbox.add_text(f"Vous avez réussi à fuire !")
            self.outputbox.add_text(
                f"Vous ne gagnez pas de point d'expérience pour avoir fui.")
            self.playbutton.config(text="(P)Quitter le combat")
            self.playbutton.config(state=NORMAL)
            self.playbutton.config(command=self.hide_combat)
            self.attackbutton.config(state=DISABLED)
            self.defendbutton.config(state=DISABLED)
            self.fleebutton.config(state=DISABLED)
            self.spellbutton.config(state=DISABLED)
        else:
            self.outputbox.add_text(f"Vous n'avez pas réussi à fuire !")
            self.outputbox.add_text(f"Vous passez votre tour.")
            self.order = None
            self.playerturn = False
            self.speedbar.order = None
            self.attackbutton.config(state=DISABLED)
            self.defendbutton.config(state=DISABLED)
            self.spellbutton.config(state=DISABLED)
            self.fleebutton.config(state=DISABLED)
            self.play_combat_loop()

    def hide_combat(self):
        self.player_healthbar.hidetip()
        self.monster_healthbar.hidetip()
        self.speedbar.hidetip()
        self.spellbar.hidetip()
        self.attackbar.hidetip()
        self.player_label.destroy()
        self.monster_label.destroy()

        self.attackbutton.destroy()
        self.defendbutton.destroy()
        self.playbutton.destroy()
        self.spellbutton.destroy()
        self.fleebutton.destroy()

        self.player_stats = None
        self.equipped_list = None
        self.combat = False
        self.playerturn = False
        self.player_stats = None
        self.monster_dic = None

        self.AttributButton.config(state=NORMAL)
        self.SpellMenuButton.config(state=NORMAL)
        self.InventoryButton.config(state=NORMAL)
        self.LevelupButton.config(state=NORMAL)

        self.draw_everything()


if __name__ == "__main__":
    global w
    import manipulate_json as jm
    import manipulate_map as mm

    player_dic = jm.load_file('player_dic', 'Blue Dragon')
    attribut_dic = jm.load_file('attribut_dic', 'Blue Dragon')
    spell_dic = jm.load_file('spell_dic', 'Blue Dragon')
    inventory_dic = jm.load_file('inventory_dic', 'Blue Dragon')
    monster_dic = jm.load_file(
        fulldir="ressources/template/monster/slime_bleu.json")

    mapdir = "img/stock/_tiles/Tiled software"
    mapname = "my_first_map"
    tilename = "bloks"

    imgdir = "img/stock/_tiles/non resized"

    w = Main_Window(player_dic['name'])
    w.load_map(mapdir, mapname, tilename, imgdir)
    player_imgdir = "img/claptrap.gif"
    w.load_player(player_imgdir=player_imgdir)

    w.draw_everything(3, 3)

    # w.show_combat(monster_dic=monster_dic)

    w.main_window.focus_force()
    w.main_window.mainloop()
