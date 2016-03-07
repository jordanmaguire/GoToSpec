import os

class PathResolver:

  def find_spec(self, folder, dirname, filename, extension):
    if dirname.startswith('/app'):
      dirname = dirname[4:]

    dirname = "/spec" + dirname + "/"
    filename = filename + "_spec" + extension

    spec_file = folder + dirname + filename
    if os.path.isfile(spec_file):
      return spec_file

    dirname = dirname.replace('spec/', 'spec/requests/')

    spec_file = folder + dirname + filename
    if os.path.isfile(spec_file):
      return spec_file

  def find_implementation(self, folder, dirname, filename, extension):
    filename = filename[0:-5]
    dirname = dirname[5:] + '/'

    test_subject = folder + dirname + filename + extension
    if os.path.isfile(test_subject):
      return test_subject

    dirname = '/app' + dirname
    test_subject = folder + dirname + filename + extension
    if os.path.isfile(test_subject):
      return test_subject

    dirname = dirname.replace('/requests', '')
    test_subject = folder + dirname + filename + extension
    if os.path.isfile(test_subject):
      return test_subject
