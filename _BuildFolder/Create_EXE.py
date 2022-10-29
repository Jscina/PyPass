import PyInstaller.__main__, os, time
from shutil import copy, rmtree, move
class CreateEXE:
    def __init__(self, files: list) -> None:
        self.files = files
        self.icon = os.path.abspath("_BuildFolder/PyPass.ico")

    def build_program(self, name: str) -> None:
        PyInstaller.__main__.run([f"{name}.py", "--onedir", "--windowed", f"-i={self.icon}"])
            
    def run(self) -> None:
        for name in self.files:
            self.build_program(name)

# Run to build the exe
if __name__ == "__main__":
    builder = CreateEXE(["src/PyPass"])
    start_time = time.time() # Track execution time
    builder.run()
    copy(builder.icon, "dist/PyPass")   
    rmtree(os.path.join(os.getcwd(), "build"))
    if os.path.exists(os.path.join(os.getcwd(), "Staging", "dist")):
        rmtree(os.path.join(os.getcwd(), "Staging"))
    src = os.path.join(os.getcwd(), "dist")
    dst = os.path.join(os.getcwd(), "Staging")
    move(src, dst)
    os.remove(os.path.join(os.getcwd(), "PyPass.spec"))
    print(f"Done, build took {time.time() - start_time} seconds")
