def check_python_code_if_has_errors_via_flake8(code):
    import tempfile
    import subprocess
    with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
        f.write(code)
        fname = f.name
    result = subprocess.run(["flake8", fname], capture_output=True, text=True)
    print(result.stdout)

#example usage
#check_python_code_if_has_errors_via_flake8('''\nasync def foo():\n    pass\n\ndef bar():\n    foo()  # unawaited coroutine\n\ntry:\n    x = 1 / 0\nexcept:\n    pass\n''')
