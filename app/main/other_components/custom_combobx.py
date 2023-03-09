from tkinter import ttk
from ttkwidgets.autocomplete import AutocompleteCombobox

class CustomCombobox(AutocompleteCombobox):
    def __init__(self, container, textvariable=None, valueList=None, defaultvalue=None, *args, **kwargs):
        super().__init__(container, completevalues=valueList, textvariable=textvariable, *args, **kwargs)

        # Calling modified set_completion_list() by overriding same method of AutocompleteCombobox to add default value feature
        self.set_completion_list(self["values"], defaultvalue)
        # All the steps necessary same as base class to do after calling set_completion_list()
        self._hits = []
        self._hit_index = 0
        self.position = 0
        # navigate on keypress in the dropdown:
        # code taken from https://wiki.tcl-lang.org/page/ttk%3A%3Acombobox by Pawel Salawa, copyright 2011
        self.tk.eval("""
            proc ComboListKeyPressed {w key} {
                    if {[string length $key] > 1 && [string tolower $key] != $key} {
                            return
                    }

                    set cb [winfo parent [winfo toplevel $w]]
                    set text [string map [list {[} {\[} {]} {\]}] $key]
                    if {[string equal $text ""]} {
                            return
                    }

                    set values [$cb cget -values]
                    set x [lsearch -glob -nocase $values $text*]
                    if {$x < 0} {
                            return
                    }

                    set current [$w curselection]
                    if {$current == $x && [string match -nocase $text* [lindex $values [expr {$x+1}]]]} {
                            incr x
                    }

                    $w selection clear 0 end
                    $w selection set $x
                    $w activate $x
                    $w see $x
            }

            set popdown [ttk::combobox::PopdownWindow %s]
            bind $popdown.f.l <KeyPress> [list ComboListKeyPressed %%W %%K]
            """ % (self))

        # Avoiding Text highlight characteristics of ttk.Combobox after selection in clam theme
        if type(textvariable) == None.__class__:
            pass
        else:
            self.bind("<FocusIn>", lambda e: self.etc(textvariable))
        
        self.useless_entry = ttk.Entry(self)



    # Remove unecessary text selection in clam theme for combobox 
    def etc(self, textvariable):
        alo = textvariable.get()
        textvariable.set("")
        textvariable.set(alo)
        


    # Overriding AutocompleteCombobox method to add default value in value lists
    def set_completion_list(self, completion_list, defaultvalue=None):
        """
        Use the completion list as drop down selection menu, arrows move through menu.

        :param completion_list: completion values
        :type completion_list: list
        """
        self._completion_list = sorted(completion_list, key=str.lower)  # Work with a sorted list
        self.configure(values=completion_list)
        self._hits = []
        self._hit_index = 0
        self.position = 0
        self.bind('<KeyRelease>', self.handle_keyrelease)
        if type(defaultvalue) == None.__class__:
            self['values'] = self._completion_list  # Setup our popup menu
        else:
           self['values'] = defaultvalue + self._completion_list  # Setup our popup menu 
