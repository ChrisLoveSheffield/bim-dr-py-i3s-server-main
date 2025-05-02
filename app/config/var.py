DEFAULT_HOME = r'slpk'  # Default home directory for slpk files
cached_slpk = None


def get_home():
    # Replace with the correct logic for `home`
    global cached_slpk
    if cached_slpk is None:
        from init import slpk_dir
        if slpk_dir is None:
            import os
            current_path = os.getcwd()
            slpk_dir = os.path.join(current_path, DEFAULT_HOME)
        cached_slpk = slpk_dir
    return cached_slpk


home = get_home()
