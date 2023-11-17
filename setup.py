from cx_Freeze import setup, Executable

build_exe_options = {
    "include_files": ["NotoMono-Regular.ttf", "message.html"],
}

setup(
    name="SoE",
    version="1.0",
    description="Отправка уведомлений об экзаменах",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base="Win32GUI", target_name="SoE.exe")]
)