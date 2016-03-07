import os

class PathResolver:

  # folder:     "/path/to/your/rails/app"
  # dirname:    "/app/models"
  # filename:   "user"
  # extension:  ".rb"
  def find_verified_spec_path(self, folder, dirname, filename, extension):
    if dirname.startswith('/app'):
      dirname = dirname[4:]

    dirname = "/spec" + dirname + "/"
    filename = filename + "_spec" + extension

    spec_file = folder + dirname + filename
    if os.path.isfile(spec_file):
      return spec_file

  # folder:     "/path/to/your/rails/app"
  # dirname:    "/app/models"
  # filename:   "user"
  # extension:  ".rb"
  def find_verified_implementation_path(self, folder, dirname, filename, extension):
    filename = filename[0:-5]
    dirname = dirname[5:] + '/'

    test_subject = folder + dirname + filename + extension
    if os.path.isfile(test_subject):
      return test_subject

    # spec/models/user_spec.rb -> app/models/user.rb
    dirname = '/app' + dirname
    test_subject = folder + dirname + filename + extension
    if os.path.isfile(test_subject):
      return test_subject
