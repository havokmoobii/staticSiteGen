import os, shutil

def main():
    log = ""
    log = rm_public(log)
    if not os.path.exists("./static"):
        raise Exception("FATAL: ./static not found.")
    else:
        os.mkdir("./public")
        log = log + "Created ./public\n"
        log = copy_static_to_public("./static", log)

    with open("main_log.txt", "w") as f:
        f.write(log)

def rm_public(log):
    if os.path.exists("./public"):
        shutil.rmtree("./public")
        log = log + "Removed ./public\n"
    return log

def copy_static_to_public(path, log):
    log = log + f"Files found in {path}: {os.listdir(path)}\n"
    current_level_files = os.listdir(path)
    for file in current_level_files:        
        if not os.path.isfile(f"{path}/{file}"):
            os.mkdir(f"./public/{path[8:]}{file}")
            log = log + f"Copied {path}/{file} to ./public/{path[9:]}{file}\n"
            log = copy_static_to_public(f"{path}/{file}", log)
        else:
            shutil.copy(f"{path}/{file}", f"./public/{path[9:]}/{file}")
            log = log + f"Copied {path}/{file} to ./public/{path[9:]}/{file}\n"
    return log
main()