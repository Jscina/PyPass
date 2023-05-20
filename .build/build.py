from PyInstaller import __main__
from pathlib import Path

def main():
    app_icon = Path(__file__).parent.joinpath("pypass.png")
    static_dir = Path(__file__).parent.parent.joinpath("app/static")
    template_dir = Path(__file__).parent.parent.joinpath("app/templates")
    __main__.run([
        "--onedir",
        "--windowed",
        "--exclude-module=_tkinter", 
        f"--icon={app_icon}",
        f"--add-data={static_dir}:app/static",
        f"--add-data={template_dir}:app/templates",
        "--name=pypass",  # Set the output name here
        "app.py"
    ])

if __name__ == "__main__":
    main()
