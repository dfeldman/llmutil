import os
import subprocess

def create_virtual_environment():
    venv_name = "venv"
    subprocess.run(["python", "-m", "venv", venv_name], check=True)
    return venv_name

def activate_virtual_environment(venv_name):
    if os.name == "nt":  # Windows
        activate_script = os.path.join(venv_name, "Scripts", "activate")
        subprocess.run(["cmd", "/C", f"call {activate_script}"], shell=True, check=True)
    else:  # Unix/Linux/macOS
        activate_script = os.path.join(venv_name, "bin", "activate")
        subprocess.run(["source", activate_script], shell=True, check=True)

def install_requirements():
    subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)

def main():
    venv_name = create_virtual_environment()
    activate_virtual_environment(venv_name)
    install_requirements()
    print("Virtual environment created and requirements installed.")

if __name__ == "__main__":
    main()
    