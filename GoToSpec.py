import sublime, sublime_plugin, os, time
from path_resolver import *

class GoToSpecCommand(sublime_plugin.WindowCommand):
	def open_left(self, file):
		self.window.open_file(file)
		if self.window.active_group() == 0:
			return

		self.window.run_command('close')
		self.window.run_command('set_layout',
			{ "cols": [0.0, 0.5, 1.0], "rows": [0.0, 1.0], "cells": [[0,0,1,1],[1,0,2,1]] })

		self.window.focus_group(0)
		self.window.open_file(file)

	def open_right(self, file):
		self.window.open_file(file)
		if self.window.active_group() == 1:
			return

		self.window.run_command('close')
		self.window.run_command('set_layout',
			{ "cols": [0.0, 0.5, 1.0], "rows": [0.0, 1.0], "cells": [[0,0,1,1],[1,0,2,1]] })

		self.window.focus_group(1)
		self.window.open_file(file)

	def spec_for(self, folder, dirname, filename, extension):
		if dirname.startswith('/app'):
			dirname = dirname[4:]

		dirname = "/spec" + dirname + "/"
		filename = filename + "_spec" + extension

		return folder + dirname + filename

	def underscore_to_class(self, value):
	    def camelcase():
	        yield str.capitalize
	        while True:
	            yield str.capitalize

	    c = camelcase()
	    return "".join(c.next()(x) if x else '_' for x in value.split("_"))

	def try_to_append(self):
		view = self.window.active_view()

		if view.is_loading():
			sublime.set_timeout(self.try_to_append, 50)
		else:
			file_name  = os.path.basename(view.file_name())
			spec_class = self.underscore_to_class(file_name.encode('utf8').replace("_spec.rb", ""))

			edit = view.begin_edit()
			total = view.insert(edit, 0, """require 'rails_helper'

describe %s do

end
""" % spec_class)
			view.sel().clear()
			view.sel().add(sublime.Region(total - 5))
			view.end_edit(edit)

	def on_done(self, option):
		# Only perform the operation if the "Create a new spec file" option is selected. If we
		# do not compare with 1, pressing ESC will trigger the action to run
		if option == 1:
			self.create_spec_file_and_folders(self.proposed_spec)
			self.open_right(self.subject_file)
			self.open_left(self.proposed_spec)
			self.try_to_append()

	def create_spec_file_and_folders(self, filename):
		base, filename = os.path.split(filename)
		self.create_folders(base)

	def create_folders(self, base):
		if not os.path.exists(base):
			parent = os.path.split(base)[0]
			if not os.path.exists(parent):
				self.create_folders(parent)
			os.mkdir(base)

	# Called by Sublime
	def run(self):
		current_file = self.window.active_view().file_name()

		folders = self.window.folders()
		for folder in folders:
			if current_file.startswith(folder):
				current_folder = folder
				current_file   = current_file.replace(folder, "")

		dirname  = os.path.dirname(current_file)
		filename = os.path.basename(current_file)
		filename, extension = os.path.splitext(filename)

		if filename.endswith('_spec'):
			spec_file    = current_folder + current_file
			subject_file = PathResolver().find_verified_implementation_path(folder, dirname, filename, extension)

			if spec_file and subject_file:
				self.open_left(spec_file)
				self.open_right(subject_file)
		else:
			spec_file    = PathResolver().find_verified_spec_path(folder, dirname, filename, extension)
			subject_file = current_folder + current_file

			if spec_file and subject_file:
				self.open_right(subject_file)
				self.open_left(spec_file)
			else:
				if subject_file:
					self.subject_file  = subject_file
					self.proposed_spec = self.spec_for(folder, dirname, filename, extension)
					self.pretty_name   = self.spec_for("", dirname, filename, extension)
					items = ["Do nothing", ["Create a new spec file", self.pretty_name]]
					self.window.show_quick_panel(items, self.on_done)
