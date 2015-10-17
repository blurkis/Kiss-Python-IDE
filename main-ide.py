#!/usr/bin/python
# -*- coding: utf-8 -*-
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
gi.require_version('GtkSource', '3.0')
from gi.repository import GtkSource
from config import check_config_file

# Comment





class KentPyIDE(Gtk.Window):

  
    def open_file(self, widget):
        print("Open file..")
        filter = Gtk.FileFilter()
        filter.set_name("Any Project")
        filter.add_pattern("*.prj")
        file_dialog = Gtk.FileChooserDialog(title="Choose a project to open,", buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        file_dialog.add_filter(filter)
        response = file_dialog.run()


        if response == Gtk.ResponseType.OK:
            print("File selected: %s" % file_dialog.get_filename())


        tmp = file_dialog.get_filename()
        if tmp == None:
            print("No file to open")
            file_dialog.destroy()
        else:
            file_to_open = open(tmp, "r")
	    #Check the prj config file. Sort of.
            check_config_file(tmp)

            text = file_to_open.read()
            self.textbuffer.set_text(text)
            file_dialog.destroy()



    def save_project(self, widget):
        print("Text to save..")

        buffer= self.sourceview.get_buffer()
        startiter, enditer = buffer.get_bounds()
        text = buffer.get_text(startiter, enditer, True)
        file_to_save = open("hej.py", "r+")
        file_to_save.write(text)


    def close_project(self, widget):
        print("Closing project")


    def show_about_dialog(self, widget):
        about_dialog = Gtk.AboutDialog()

        about_dialog.set_destroy_with_parent(True)
        about_dialog.set_program_name("Python IDE")
        about_dialog.set_version("1.0")
        about_dialog.set_authors(["Kent Nyberg"])
        about_dialog.set_comments("A simple yet fully working Python IDE.")
        about_dialog.set_copyright("(C) Kent Nyberg 2015. Licensed under GPL.")

        about_dialog.run()
        about_dialog.destroy()


    def load_from_file(self, widget):
        print("load from file")
        open_file = open("hej.py", "r")
        text = open_file.read()  # Read the whole file, should do something about size.. perhaps?
        self.get_buffer_text(text)


    def get_buffer_text(self):
        buffer= self.sourceview.get_buffer()
        startiter, enditer = buffer.get_bounds()
        text = buffer.get_text(startiter, enditer, True)

        return text

    def cursor_changed(self, buffer, data=None):
        text = self.get_buffer_text()
        text=text[:buffer.props.cursor_position]
        #print(text)
        nmr_endl=1
        for endl in text:
            if endl == '\n':
                nmr_endl+=1
        print(nmr_endl)


        print(buffer.props.cursor_position)



    def __init__(self):
        Gtk.Window.__init__(self, title='Kent PyIDE')
        self.grid = Gtk.Grid()
        self.add(self.grid)



        self.menubar = Gtk.MenuBar()
        self.menubar.set_hexpand(True)
        self.grid.attach(self.menubar, 1, 0, 1, 1)

        self.menuitem_file = Gtk.MenuItem(label="File")
        self.menubar.append(self.menuitem_file)

        self.file_menu = Gtk.Menu()
        self.menuitem_file.set_submenu(self.file_menu)
        self.menuitem_file_save = Gtk.MenuItem(label='Save project')
        self.menuitem_file_open = Gtk.MenuItem(label='Open project')
        self.menuitem_file_new_from_template = Gtk.MenuItem(label='New project from template')
        self.menuitem_file_close = Gtk.MenuItem(label='Close')
        self.menuitem_file_exit = Gtk.MenuItem(label='Exit')

        self.menuitem_file_exit.connect("activate", Gtk.main_quit)
        self.menuitem_file_save.connect("activate", self.save_project)
        self.menuitem_file_close.connect("activate", self.close_project)
        self.menuitem_file_open.connect("activate", self.open_file)

        self.file_menu.append(self.menuitem_file_new_from_template)
        self.file_menu.append(self.menuitem_file_open)
        self.file_menu.append(self.menuitem_file_save)
        self.file_menu.append(self.menuitem_file_close)
        self.file_menu.append(self.menuitem_file_exit)



        self.menuitem_edit = Gtk.MenuItem(label="Edit")
        self.menubar.append(self.menuitem_edit)
        self.edit_menu = Gtk.Menu()
        self.menuitem_edit.set_submenu(self.edit_menu)
        self.menuitem_edit_template = Gtk.MenuItem(label='Edit templates')
        self.edit_menu.append(self.menuitem_edit_template)


        self.menuitem_run = Gtk.MenuItem(label="Run")
        self.menubar.append(self.menuitem_run)
        self.run_menu = Gtk.Menu()
        self.menuitem_run.set_submenu(self.run_menu)
        self.menuitem_run_run = Gtk.MenuItem(label='Run application..')
        self.menuitem_run_run.connect("activate", Gtk.main_quit)

        self.run_menu.append(self.menuitem_run_run)


        self.menuitem_help = Gtk.MenuItem(label="Help")
        self.menubar.append(self.menuitem_help)
        self.help_menu = Gtk.Menu()
        self.menuitem_help.set_submenu(self.help_menu)
        self.menuitem_help_about = Gtk.MenuItem(label='About')

        self.menuitem_help_about.connect('activate', self.show_about_dialog)

        self.help_menu.append(self.menuitem_help_about)


        self.notebook = Gtk.Notebook()
        self.grid.attach(self.notebook, 1, 1, 1, 1)




        scrolled_window= Gtk.ScrolledWindow()

        scrolled_window.set_hexpand(True)
        scrolled_window.set_vexpand(True)
        #self.grid.attach(scrolled_window, 1, 2, 1, 1)
        self.notebook.append_page(scrolled_window)

        self.sourceview = GtkSource.View.new()

        self.sourceview.set_show_line_marks(True)
        self.sourceview.set_show_line_numbers(True)

        self.lm = GtkSource.LanguageManager.new()

        self.textbuffer = self.sourceview.get_buffer()
        self.textbuffer.set_language(self.lm.get_language('python'))
        self.textbuffer.set_highlight_syntax(True)

        self.textbuffer.connect("notify::cursor-position",
                            self.cursor_changed)
        self.textbuffer.set_text("#!/usr/bin/python\n# -*- coding: utf-8 -*-\n"
                                 )
        scrolled_window.add(self.sourceview)



win = KentPyIDE()
win.set_default_size(500,500)
win.connect('delete_event', Gtk.main_quit)
win.show_all()
Gtk.main()