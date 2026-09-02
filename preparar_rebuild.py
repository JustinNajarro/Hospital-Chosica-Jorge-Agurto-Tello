import subprocess
import os
import shutil

repo_dir = r"c:\Users\Antonela\Documents\SEXTO CICLO\PRY-hospital chosica"
os.chdir(repo_dir)

# Asegurar que estamos en una rama limpia
subprocess.run(["git", "checkout", "main"], check=True)
subprocess.run(["git", "checkout", "-b", "rebuild-main"], check=True)

# Guardar los archivos de la app final en memoria/directorio temporal
temp_final = os.path.join(repo_dir, "..", "temp_final_backup")
if os.path.exists(temp_final):
    shutil.rmtree(temp_final)
shutil.copytree(os.path.join(repo_dir, "src"), os.path.join(temp_final, "src"))
shutil.copy2(os.path.join(repo_dir, "pom.xml"), os.path.join(temp_final, "pom.xml"))
shutil.copy2(os.path.join(repo_dir, "README.md"), os.path.join(temp_final, "README.md"))
shutil.copy2(os.path.join(repo_dir, ".gitignore"), os.path.join(temp_final, ".gitignore"))

print("Backup final temporal creado.")
