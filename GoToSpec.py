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
			self.create_spec_file_and_folders(self.new_spec_filepath)
			self.open_right(self.implementation_filepath)
			self.open_left(self.new_spec_filepath)
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
		# EG: /path/to/your/rails/application/app/models/user.rb
		filename_with_full_path = self.window.active_view().file_name()

		# EG: /path/to/your/rails/application
		folder_path_to_current_app = "".join(self.window.folders())
		# EG: /app/models/user.rb
		current_file = filename_with_full_path.replace(folder_path_to_current_app, "")

		# dirname:   app/models
		# filename:  user
		# extension: .rb
		dirname  = os.path.dirname(current_file)
		filename, extension = os.path.splitext(os.path.basename(current_file))

		if filename.endswith('_spec'):
			verified_implementation_filepath = PathResolver().find_verified_implementation_path(folder_path_to_current_app, dirname, filename, extension)

			if verified_implementation_filepath:
				self.open_left(self.window.active_view().file_name())
				self.open_right(verified_implementation_filepath)
		else:
			spec_file_path = PathResolver().get_spec_path(folder_path_to_current_app, dirname, filename, extension)
			has_spec_file  = os.path.isfile(spec_file_path)
			implementation_filepath = self.window.active_view().file_name()

			if has_spec_file:
				self.open_right(implementation_filepath)
				self.open_left(spec_file_path)
			else:
				# These are used in the on_done callback
				self.implementation_filepath  = implementation_filepath
				self.new_spec_filepath = spec_file_path

				items = ["Do nothing", ["Create a new spec file", current_file]]
				self.window.show_quick_panel(items, self.on_done)
