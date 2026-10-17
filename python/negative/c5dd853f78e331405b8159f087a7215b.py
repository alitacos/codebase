def get_local_running_lab_servers_via_subprocess_into_tuple_of_stdout_and_stderr(command:str|list=['jupyter', 'lab', 'list'])->tuple:
    import subprocess
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return (result.stdout, result.stderr)