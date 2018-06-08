from os.path import isfile
from app.config import DATASETS_FOLDER
from app.config import ALLOWED_EXTENSIONS, DEFAULT_TEST_FILE

def allowed_file(filename):
    """returns true if 'filename' file is valid"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def handle_missing_test_file(filename):    
    
    if (not filename) or (filename is None) or (filename == ""):
        filename = DEFAULT_TEST_FILE
    return filename

def handle_missing_mode(filename):
    if (not filename) or (filename is None) or (filename == ""):
        filename = None
    return filename

def does_file_exist(filename):    
    filename = DATASETS_FOLDER + filename + ".csv"     
    return True if isfile(filename) else False