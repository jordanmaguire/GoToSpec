import os

class PathResolver:

  # folder:     "/path/to/your/rails/app"
  # dirname:    "/app/models"
  # filename:   "user"
  # extension:  ".rb"
  def get_spec_path(self, folder, dirname, filename, extension):
    if dirname.startswith('/app'):
      dirname = dirname[4:]

    dirname = "/spec" + dirname + "/"
    filename = filename + "_spec" + extension

    return folder + dirname + filename

  # folder:     "/path/to/your/rails/app"
  # dirname:    "/app/models"
  # filename:   "user"
  # extension:  ".rb"
  def find_verified_implementation_path(self, folder, dirname, filename, extension):
    filename = filename[0:-5]
    dirname = dirname[5:] + '/'

    implementation_path = folder + dirname + filename + extension
    if os.path.isfile(implementation_path):
      return implementation_path

    # spec/models/user_spec.rb -> app/models/user.rb
    dirname = '/app' + dirname
    implementation_path = folder + dirname + filename + extension
    if os.path.isfile(implementation_path):
      return implementation_path
