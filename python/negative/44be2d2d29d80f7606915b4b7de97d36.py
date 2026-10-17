def get_ip_route_or_error_via_shell(password: str='') -> str:
    """
    Fetches the system's IP routing table.

    Executes the 'ip route' command to display the current routing table of the system.
    If a sudo password is provided, it will run the command with elevated privileges using `sudo`.

    Parameters:
        password (str): The sudo password for authentication (optional).

    Returns:
        str: The system's IP routing table, or an error message if the command fails or encounters an exception.
    """
    import subprocess
    try:
        command = f'echo {password} | sudo -S ip route' if password else 'ip route'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return 'IP Routing Table:\n' + result.stdout
        else:
            return 'Failed to retrieve IP routing table:\n' + result.stderr
    except Exception as e:
        #print(e)
        return e