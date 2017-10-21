import os


def theme_dir_path():
    grandparent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    return os.path.join(grandparent_dir, 'themes')

def template_dir_path(filename=''):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(current_dir, 'templates', filename)
