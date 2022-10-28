import PyInstaller.__main__, os
from shutil import copy

class CreateEXE:
    def __init__(self, files: list) -> None:
        self.files = files
        self.icon = os.path.abspath("locked.ico")

    def build_program(self, name: str):
        PyInstaller.__main__.run(
            [f"{name}.py", "--onedir", "--windowed", f"-i={self.icon}"]
        )
    def run(self):
        for name in self.files:
            self.build_program(name)

# For testing only
if __name__ == "__main__":
    builder = CreateEXE(["PyPass"])
    builder.run()
    copy(builder.icon, "dist/PyPass")
