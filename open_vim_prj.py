import sublime
import sublime_plugin
from glob import glob
import os
from os.path import abspath, dirname

class OpenVimPrjCommand(sublime_plugin.WindowCommand):
    def run(self):
        active_sheet = self.window.active_sheet()
        active_sheet_view = active_sheet.view()
        current_file = active_sheet_view.file_name()
        if not current_file.endswith('prj'):
            return
        current_dir = dirname(current_file)
        os.chdir(current_dir)

        window = self.window
        active_group = window.active_group()
        curr_view_id = window.active_view_in_group(active_group).id()
        for v in window.views_in_group(active_group):
            if v.id() == curr_view_id:
                continue
            window.focus_view(v)
            window.run_command("close")

        file_list_regions = active_sheet_view.split_by_newlines(sublime.Region(0, active_sheet_view.size()))
        filesList = []
        for region in file_list_regions:
            if (region.size() == 0):
                continue
            line = active_sheet_view.substr(region)
            if line and not line.startswith('#'):
                files = glob(line)
                filesList += files
        for file in sorted(filesList):
            self.window.open_file(abspath(file))

