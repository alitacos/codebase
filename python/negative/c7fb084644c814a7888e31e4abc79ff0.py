
# is a class method. non reusable
def connect_to_drive(self, drive='/content/drive', force_remount:bool=False)->None:
    """
	    Mounts Google Colab Drive at the specified path if it is not already mounted, or remounts if forced.

    Args:
        self (Any): The instance of the class calling this method
        drive_path (str): The path where the Google Drive should be mounted (Defaults to '/content/drive')
        force_remount (bool): If True, forces the remount even if already mounted (Defaults to False)

    Returns:
        None: Does not return any value

    Example usage:
        >>> result = mount_google_colab_drive_if_not_mounted_or_force_remount(self='obj', drive_path='/content/drive', force_remount=False)
    """
    import os
    from google.colab import drive
    if not os.path.ismount('/content/drive') or force_remount:
        drive.mount('/content/drive')
    return None