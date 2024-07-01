from cx_Freeze import setup, Executable

build_exe_options = {
    "excludes": ['unicodedata', 'logging', 'unittest', 'http', 'xml', 'bz2','xmlrpc','tkinter','tk8.6'],
    "include_files": ["NotoMono-Regular.ttf", "message.html"],
    "zip_include_packages": ['dearpygui','csv','sqlite3','win32api','os','Thread','configparser','smtplib','email','pyodbc','urllib']
}

setup(
    name="SoE",
    version="1.0",
    description="Отправка уведомлений об экзаменах",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base="Win32GUI", target_name="SoE.exe",icon='exam.ico')]
)