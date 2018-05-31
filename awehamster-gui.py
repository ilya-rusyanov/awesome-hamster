#!/usr/bin/env python2
import os
import dbus
import gtk

class AwesomeHamsterGui():
    def __init__(self):
        self.activitiesList = [ ]

        bus = dbus.SessionBus()

        proxyHamster = bus.get_object('org.gnome.Hamster', '/org/gnome/Hamster')
        self.ifaceHamster = dbus.Interface(proxyHamster, 'org.gnome.Hamster')

        activities = self.ifaceHamster.GetActivities('')

        for act in activities:
            if act[1] != '':
                self.activitiesList.append(act[0] + '@' + act[1])
            else:
                self.activitiesList.append(act[0])


    def _match_anywhere(self, completion, entrystr, iter, data):
        modelstr = completion.get_model()[iter][0]
        return entrystr in modelstr


    def _on_entry_activate(self, entry):
        text = entry.get_text()
        if text != '':
            self.ifaceHamster.AddFact(text, 0, 0, False)
            self.dialog.destroy()

    def on_key_down(self, widget, event):
        if event.keyval == 65364:
            widget.set_text(self.activitiesList[self.histcounter])

    def run(self):
        self.histcounter = 0
        listStore = gtk.ListStore(str)
        maxLen = 0
        for act in self.activitiesList:
            if len(act) > maxLen:
                maxLen = len(act)
            listStore.append([act])

        label = gtk.Label("New activity: ")
        hBox = gtk.HBox()

        entryCompletion = gtk.EntryCompletion()
        entryCompletion.set_model(listStore)
        entryCompletion.set_text_column(0)
        entryCompletion.set_minimum_key_length(0)
        entryCompletion.set_match_func(self._match_anywhere, None)
        entryCompletion.set_inline_selection(True)

        self.entry = gtk.Entry()
        self.entry.set_completion(entryCompletion)
        self.entry.set_width_chars(maxLen + 5)
        self.entry.connect("activate", self._on_entry_activate)
        self.entry.connect('key_press_event', self.on_key_down)

        self.dialog = gtk.Dialog("New activity",
                                 None,
                                 gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                 (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))

        hBox.pack_start(label)
        hBox.pack_start(self.entry)
        self.dialog.vbox.pack_start(hBox)
        label.show()
        self.entry.show()
        hBox.show()
        self.dialog.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.dialog.run()

ahgui = AwesomeHamsterGui()
ahgui.run()
