import os
import sys
import vim

def find_compile_commands():
    files = os.listdir()
    for f in files:
        if f == "compile_commands.json":
            return 1
    return 0

if len(sys.argv) < 2:
    os._exit(1)


def get_ext(file):
    full = os.path.splitext(file)
    ext = full[1]
    return ext

def get_filename(file):
    full = os.path.splitext(file)
    filename = full[0]
    return filename

available_cpps = [".cpp", ".cc", ".cxx"]
available_hpps = [".h", ".hpp", ".hxx", ".hh"]

def try_find_in_current(path, file, filename, full_filename):
    os.chdir(path)
    files = os.listdir()
    for f in files:
        if os.path.splitext(f)[0] == filename:
            if f != full_filename:
                print ("found in current: " + f + ", without ext: " + os.path.splitext(f)[1])
                return os.getcwd() + '/' + f

def try_find_in_includes(path, file, filename, full_filename):
    os.chdir(path)
    current_dir = os.getcwd()
    os.chdir('include')
    if current_dir == os.getcwd():
        return None
    files = os.listdir()
    for f in files:
        if os.path.splitext(f)[0] == filename:
            if f != full_filename:
                print ("found in include/: " + f + ", without ext: " + os.path.splitext(f)[1])
                return os.getcwd() + '/' + f

def try_find_in_dotdotincludes(path, file, filename, full_filename):
    os.chdir(path)
    current_dir = os.getcwd()
    os.chdir('../include')
    if current_dir == os.getcwd():
        return None
    files = os.listdir()
    for f in files:
        if os.path.splitext(f)[0] == filename:
            if f != full_filename:
                print ("found in dotdot/: " + f + ", without ext: " + os.path.splitext(f)[1])
                return os.getcwd() + '/' + f

def find_file(path, file):
    full_filename = file
    ext = get_ext(file)
    filename = get_filename(file)
    if ext in available_cpps or ext in available_hpps:
        result = try_find_in_current(path, file, filename, full_filename)
        if result == None:
            result = try_find_in_includes(path, file, filename, full_filename)
            if result == None:
                result = try_find_in_dotdotincludes(path, file, filename, full_filename)
        return result
    return None

def main():
    file = vim.current.buffer.name
    path = os.path.split(file)[0]
    file = os.path.split(file)[1]
    alt = find_file(path, file)
    if alt != None :
        vim.command('e ' + alt)

if __name__ == '__main__':
    main()

