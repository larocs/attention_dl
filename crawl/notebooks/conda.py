if __name__ == "__main__":
    import os
    import sys
    import getpass

    crc_path = os.path.join("C:\\Users", "DXT6", ".condarc")
    with open(crc_path, "r") as f:
        data = f.read()

    bkp_data = data
    pwd = getpass.getpass()
    data = data.replace(":senha", f":{pwd}")
    with open(crc_path, "w") as f:
        f.write(data)

    # Install ...
    try:
        cmd = " ".join(sys.argv[1:])
        print(cmd)
        os.system(cmd)
    except:
        pass

    with open(crc_path, "w") as f:
        f.write(bkp_data)
