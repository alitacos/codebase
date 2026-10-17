def get_ip_route_via_shell(password: str=None):
    """
    Retrieve the IP routing table.

    Executes the 'ip route' command to display the system's routing table.
    Uses sudo if a password is provided.

    Parameters:
        password (str): The sudo password (optional).

    Returns:
        str: The IP routing table or an error message.
    """
    import subprocess
    command = f'echo {password} | sudo -S ip route' if password else 'ip route'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        return 'IP Routing Table:\n' + result.stdout
    else:
        return 'Failed to retrieve IP routing table:\n' + result.stderr