#!/usr/bin/python

import sublime
import sublime_plugin

# TODO: limit the size of this?
history = []


class ClipboardDisplayCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        print history
        if not history:
            return
        self.view.window().show_quick_panel(history, self.panel_done)

    def panel_done(self, picked):
        if 0 > picked < len(history):
            return

        s = sublime.load_settings("ClipboardHistory.sublime-settings")

        text = history[picked]
        edit = self.view.begin_edit()
        new_regions = []
        for region in self.view.sel():
            self.view.replace(edit, region, text)
            new_region = sublime.Region(region.begin() + len(text),
                region.end() + len(text))
            new_regions.append(new_region)
        self.view.sel().clear()
        for region in new_regions:
            self.view.sel().add(region)
        self.view.end_edit(edit)

        if s.get("add_on_paste"):
            sublime.set_clipboard(text)


# Here we see a cunning plan. We listen for a key, but never say we
# support it. This lets us respond to ctrl-c and ctrl-x, without having
# to re-implement the copy and cut commands. (Important, since
# run_command("copy") doesn't do anything.)
class ClipboardListner(sublime_plugin.EventListener):
    def on_query_context(self, view, key, *args):
        if key != "clipboardcopy_fake":
            return None
        for selected in view.sel():
            selected = view.sel()[0]
            if selected.empty():
                selected = view.line(selected)

            text = view.substr(selected)

            if not history or history[-1] != text:
                history.insert(0, text)

        s = sublime.load_settings("ClipboardHistory.sublime-settings")
        if s.get("limit") < len(history):
            for i in xrange(len(history) - s.get("limit")):
                history.pop()

        return None
