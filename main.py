#!/usr/bin/python3
# -*- coding: utf-8 -*-
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
gi.require_version('GtkSource', '3.0')
from gi.repository import GtkSource
from config import check_config_file
from config import save_config_file
import os
from os.path import expanduser




class KentPyIDE(Gtk.Window):
    ProjectFolder = expanduser("~")+"/PyIDE"
    ProjectDict = {"ProjectFolder": ProjectFolder, "Author": "Noname as Noname", "Email": "email@de.de",
                  "ProjectName": "Projektname", "ProjectVersion": "ProjectVersion", "ProjectFiles": "noname"}

    def create_project(self, widget):
        #print("Folder to save projects in: " + self.ProjectFolder)
        #print("Creating project..  Print out info from textentrys as a start.")
        #print("Testar dict:" + self.ProjectDict["ProjectFolder"])
        #project_name=self.project_entry_name.get_text()
        self.ProjectDict["ProjectFolder"]= expanduser("~") + "/PyIDE"
        self.ProjectDict["Author"] = self.project_entry_author.get_text()
        self.ProjectDict["ProjectName"] = self.project_entry_name.get_text()
        self.ProjectDict["Email"] = self.project_entry_email.get_text()
        self.ProjectDict["ProjectFiles"]= self.ProjectDict["ProjectName"]+".py"

        #print("Testar self.ProjectDict ProjectFolder: " + self.ProjectDict["ProjectFolder"])
        #print("Testar self.ProjectDict Author: " + self.ProjectDict["Author"])
        #print("Testar self.ProjectDict Project Name: " + self.ProjectDict["ProjectName"])
        #print("Test self.ProjectDict Email: " + self.ProjectDict["Email"])
        
        project_email=self.project_entry_email.get_text()
        project_author=self.project_entry_author.get_text()  
        #print("Project name: ", project_name, "\nProject author: ", project_author, "\nemail: ", project_email)
        #print("Project folder to check for:" + self.ProjectFolder + "/" + project_name)

        if not os.path.isdir(self.ProjectDict["ProjectFolder"]):
           os.mkdir(self.ProjectDict["ProjectFolder"])
            #print("PyIDE i home fanns ej, skapar.")

        if os.path.isdir(self.ProjectDict["ProjectFolder"] + "/" + self.ProjectDict["ProjectName"]):
           #print("Project folder exists.")
           project_folder=1
           #Show information that a project with that name already exists.
           #Offer to open that project instead.
           #Cansel this function. 
           return 
        else:
           #print("Project folder does not exist.")
           project_folder=0
           #print("Creating project folder..")
           os.mkdir(self.ProjectDict["ProjectFolder"] + "/" + self.ProjectDict["ProjectName"])
           project_file = open(self.ProjectDict["ProjectFolder"] + "/" + self.ProjectDict["ProjectName"] + "/"+self.ProjectDict["ProjectName"]+".prj", "w")
           save_config_file(self, project_file)
           project_file.close()
           #Create the files that are configured to be created in the dialog? Most often, main.py etc.
        

    def project_cansel_pressed(self, widget):
        #print("Cansel pressed in project dialog")
        self.project_window.hide()

    def project_hide(self, event, data):
        #print("hiding project dialog. Catched delete event from window.")
        self.project_window.hide()
        return True   #Need to return True, otherwise widgets in window is destroyed.

    def new_project_from_template(self, widget):
        # Should create the window in the class, and only show/hide it as wanted.  So we dont recreate it all the time.
       #print("New project_from_template   from menu.")
       self.project_window.show_all()





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
            fp = check_config_file(tmp)  # Should return something to tell if the config is wrong.
            file_to_open = open(fp, "r")
	    #Check the prj config file. Sort of.
            

            text = file_to_open.read()
            self.textbuffer.set_text(text)
            file_dialog.destroy()



    def save_project(self, widget):
        print("Text to save..")

        buffer= self.sourceview.get_buffer()
        startiter, enditer = buffer.get_bounds()
        text = buffer.get_text(startiter, enditer, True)
        file_to_save = open("main-ide.py", "r+")
        file_to_save.write(text)


    def close_project(self, widget):
        print("Closing project")


    def show_about_dialog(self, widget):
        about_dialog = Gtk.AboutDialog()

        about_dialog.set_destroy_with_parent(True)
        about_dialog.set_program_name("Python IDE")
        about_dialog.set_version("0.1 ")
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


        self.project_window = Gtk.Window(title="New Project")
        self.project_window.connect("delete-event", self.project_hide ) #self.project_hide
        self.project_window.set_default_size(500,300)
       
        self.project_grid = Gtk.Grid()
        self.project_window.add(self.project_grid)
        self.project_name = Gtk.Label("Enter project name:")
        self.project_grid.attach(self.project_name, 1, 0, 1, 1)
        self.project_author = Gtk.Label("Enter author name:")
        self.project_grid.attach(self.project_author, 1, 1, 1, 1)
        self.project_email  = Gtk.Label("Enter Email of author or project:")
        self.project_grid.attach(self.project_email, 1, 2, 1, 1)
       
        self.project_create_button = Gtk.Button("Create project")
        self.project_grid.attach(self.project_create_button, 1,3,1,1)
        self.project_cansel_button = Gtk.Button("Cansel project")
        self.project_grid.attach(self.project_cansel_button, 2,3,1,1)
        
        self.project_entry_name = Gtk.Entry()
        self.project_entry_email = Gtk.Entry()
        self.project_entry_author = Gtk.Entry()
 
        self.project_grid.attach(self.project_entry_name, 2, 0, 1, 1)
        self.project_grid.attach(self.project_entry_author, 2, 1, 1, 1)	
        self.project_grid.attach(self.project_entry_email, 2, 2, 1, 1)
        self.project_cansel_button.connect("clicked", self.project_cansel_pressed)
        self.project_create_button.connect("clicked", self.create_project)



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
        #self.menuitem_file_github_upload = Gtk.MenuItem(label='Upload to GitHub')
        self.menuitem_file_close = Gtk.MenuItem(label='Close')
        self.menuitem_file_exit = Gtk.MenuItem(label='Exit')

        self.menuitem_file_exit.connect("activate", Gtk.main_quit)
        self.menuitem_file_save.connect("activate", self.save_project)
        self.menuitem_file_close.connect("activate", self.close_project)
        self.menuitem_file_open.connect("activate", self.open_file)
        self.menuitem_file_new_from_template.connect("activate", self.new_project_from_template)

        self.file_menu.append(self.menuitem_file_new_from_template)
        self.file_menu.append(self.menuitem_file_open)
        self.file_menu.append(self.menuitem_file_save)
        #self.file_menu.append(self.menuitem_file_github_upload)
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


        self.menuitem_git = Gtk.MenuItem(label="Git")
        self.menubar.append(self.menuitem_git)
        self.git_menu = Gtk.Menu()
        self.menuitem_git.set_submenu(self.git_menu)
        self.menuitem_git_config = Gtk.MenuItem(label="Configure Git")
        self.menuitem_git_config.connect("activate", Gtk.main_quit)
        self.menuitem_git_commit = Gtk.MenuItem(label="Commit to git")
        
        self.git_menu.append(self.menuitem_git_config)
        self.git_menu.append(self.menuitem_git_commit)



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
        tmp_label = Gtk.Label("main.py")
        self.notebook.append_page(scrolled_window, tmp_label)

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
        self.notebook.show_all()

        #split self.ProjectDict["ProjectFiles"] into a list. Do a range on it, and create tabs.
        label = Gtk.Label(label="label main.py")
        tab_label = Gtk.Label(label="config.py")
        self.notebook.append_page(label, tab_label)
        self.notebook.show_all() 

win = KentPyIDE()
win.set_default_size(500,500)
win.connect('delete_event', Gtk.main_quit)
win.show_all()
Gtk.main()
