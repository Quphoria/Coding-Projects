import win32con
from win32api import GetLogicalDriveStrings
from win32file import GetDriveType


def get_drives_list(drive_types=(win32con.DRIVE_REMOVABLE,)):
    ret = list()
    drives_str = GetLogicalDriveStrings()
    drives = [item for item in drives_str.split("\x00") if item]
    for drive in drives:
        if GetDriveType(drive) in drive_types:
            ret.append(drive[:2])
    return ret


if __name__ == "__main__":
    drives = get_drives_list()
    print("Removable drives: " + str(drives))
