import os
import random
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, GLib

class TesterWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="SIS tester")

        screen = Gdk.Screen.get_default()
        gtk_provider = Gtk.CssProvider()
        gtk_context = Gtk.StyleContext()
        gtk_context.add_provider_for_screen(screen, gtk_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        gtk_provider.load_from_path("style.css")

        vbox = Gtk.VBox()
        self.add(vbox)

        self.images = []
        self.names = []
        self.probabilities = []
        self.cur_guess = False
        self.cur_guess_index = False
        self.cur_timer = False
        self.default_image = GdkPixbuf.Pixbuf.new_from_file("default.png")
        self.load_images()
        
        self.img = Gtk.Image()
        self.img.set_from_pixbuf(self.default_image)
        vbox.add(self.img)
        
        self.entry = Gtk.Entry()
        self.entry.set_name("entry")
        self.entry.set_text("Radek")
        self.entry.props.xalign = 0.5
        self.entry.set_editable(False)
        self.entry.connect("event-after", self.text_submited)
        vbox.add(self.entry)

        entry_style_context = self.entry.get_style_context()
        entry_style_context.add_class("red")

        self.guessing = False;
        
        self.connect("key-press-event", self.on_key_press)
        
        
    def load_images(self):
        names = os.listdir("get_photos/out/")
        for name in names:
            self.images.append(GdkPixbuf.Pixbuf.new_from_file("get_photos/out/"+name))
            self.names.append(name.split("_")[1].split(".")[0].lower())
        self.probabilities = [2 for i in range(len(names))]

    def set_guessing(self,val):
        entry_style_context = self.entry.get_style_context()
        if val == True:
            entry_style_context.remove_class("red")
            entry_style_context.add_class("green")
        if val == False:
            entry_style_context.remove_class("green")
            entry_style_context.add_class("red")
        self.guessing = val
        
    def on_key_press(self,w,e):
        if self.guessing == False:
            keyval = e.keyval
            keyval_name = Gdk.keyval_name(keyval)
            if keyval_name == "space":
                self.entry.set_editable(True)
                self.next_image()
                self.set_guessing(True)

    def text_submited(self,v,w):
        if self.guessing == True:
            text = self.entry.get_text()
            if(text.strip() == self.cur_guess):
                GLib.source_remove(self.cur_timer)
                self.probabilities[self.cur_guess_index] -= 1
                self.next_image()
            
    def next_image(self):
        print(sum(self.probabilities))
        self.entry.set_text("")
        [new_guess] = random.choices(list(enumerate(zip(self.images,self.names))),weights=self.probabilities,k=1)
        self.img.set_from_pixbuf(new_guess[1][0])
        self.cur_guess = new_guess[1][1]
        self.cur_guess_index = new_guess[0]
        self.cur_timer = GLib.timeout_add(5000, self.timeout)

    def timeout(self):
        print("Timed Out")
        self.probabilities[self.cur_guess_index] += 1
        self.entry.set_text(self.cur_guess)
        self.entry.set_editable(False)
        self.set_guessing(False)
        
win = TesterWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
