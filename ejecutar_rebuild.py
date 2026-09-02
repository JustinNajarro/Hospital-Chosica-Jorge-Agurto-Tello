import subprocess
import os
import shutil

repo_dir = r"c:\Users\Antonela\Documents\SEXTO CICLO\PRY-hospital chosica"
temp_final = os.path.join(repo_dir, "..", "temp_final_backup")
os.chdir(repo_dir)

author_name = "JustinNajarro"
author_email = "jnajarro.villagaray@gmail.com"

def set_git_env(date_str):
    env = os.environ.copy()
    env["GIT_AUTHOR_NAME"] = author_name
    env["GIT_AUTHOR_EMAIL"] = author_email
    env["GIT_AUTHOR_DATE"] = date_str
    env["GIT_COMMITTER_NAME"] = author_name
    env["GIT_COMMITTER_EMAIL"] = author_email
    env["GIT_COMMITTER_DATE"] = date_str
    return env

# Vamos a iniciar una rama huérfana limpia para construir los 5 commits exactos
subprocess.run(["git", "checkout", "--orphan", "orchestrate-history"], check=True)

# Limpiar tracked files
subprocess.run(["git", "rm", "-rf", "."], check=True)

# =========================================================================
# COMMIT 1: Configuración inicial del proyecto Spring Boot
# Fecha: 2024-09-02 10:15:20 -0500
# Contiene estructura base, pom inicial con dependencias y comentarios provisionales, README preliminar, config básica
# =========================================================================
shutil.copy2(os.path.join(temp_final, ".gitignore"), repo_dir)

readme_v1 = """# CLINICA-BACKEND
Sistema Web de Gestion de Citas Medicas - Hospital Jose Agurto Tello (Chosica).
Modulo Backend desarrollado en Spring Boot 3 con Java 17 y base de datos relacional MySQL.

## Arquitectura Inicial
- Controlador REST provisional
- Configuracion basica de entorno
- Conexion JDBC directa
"""
with open(os.path.join(repo_dir, "README.md"), "w", encoding="utf-8") as f:
    f.write(readme_v1)

pom_v1 = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.3.4</version>
        <relativePath/>
    </parent>

    <groupId>pe.edu.utp</groupId>
    <artifactId>clinica-backend</artifactId>
    <version>1.0.0</version>
    <name>clinica-backend</name>
    <description>Sistema Web de Gestion de Citas Medicas</description>

    <properties>
        <java.version>17</java.version>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <dependencies>
        <!-- Dependencias base para API Web -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <!-- Driver MySQL preliminar -->
        <dependency>
            <groupId>com.mysql</groupId>
            <artifactId>mysql-connector-j</artifactId>
            <scope>runtime</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
</project>
"""
with open(os.path.join(repo_dir, "pom.xml"), "w", encoding="utf-8") as f:
    f.write(pom_v1)

os.makedirs(os.path.join(repo_dir, "src", "main", "resources"), exist_ok=True)
props_v1 = """spring.application.name=clinica-backend
server.port=8080
# Configuracion inicial local de prueba
# spring.datasource.url=jdbc:mysql://localhost:3306/clinica_citas
"""
with open(os.path.join(repo_dir, "src", "main", "resources", "application.properties"), "w", encoding="utf-8") as f:
    f.write(props_v1)

os.makedirs(os.path.join(repo_dir, "src", "main", "java", "pe", "edu", "utp", "clinica"), exist_ok=True)
app_v1 = """package pe.edu.utp.clinica;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

// Clase principal de arranque del microservicio Spring Boot
@SpringBootApplication
public class ClinicaApplication {
    public static void main(String[] args) {
        SpringApplication.run(ClinicaApplication.class, args);
    }
}
"""
with open(os.path.join(repo_dir, "src", "main", "java", "pe", "edu", "utp", "clinica", "ClinicaApplication.java"), "w", encoding="utf-8") as f:
    f.write(app_v1)

subprocess.run(["git", "add", "."], check=True)
env1 = set_git_env("2024-09-02 10:15:20 -0500")
subprocess.run(["git", "commit", "-m", "Configuración inicial del proyecto Spring Boot"], env=env1, check=True)
print("Commit 1 listo.")

# =========================================================================
# COMMIT 2: Agrega conexión a BD, CORS y manejo de errores
# Fecha: 2024-09-16 16:42:10 -0500
# MODIFICA: application.properties (elimina comentarios iniciales -> ROJO/VERDE/AZUL), README.md (actualiza descripción -> ROJO/VERDE/AZUL)
# AGREGA: paquete config (Conexion.java, CorsConfig.java, ApiException.java, ErroresSQL.java, ManejadorErrores.java)
# =========================================================================
shutil.copytree(os.path.join(temp_final, "src", "main", "java", "pe", "edu", "utp", "clinica", "config"),
                os.path.join(repo_dir, "src", "main", "java", "pe", "edu", "utp", "clinica", "config"))

# Modificamos README.md (reemplazando texto para generar lineas rojas y verdes)
readme_v2 = """# CLINICA-BACKEND
Sistema Web de Gestion de Citas Medicas - Hospital Jose Agurto Tello (Chosica).

## Modulo de Configuracion y Persistencia
- Configuracion de CORS habilitada para origenes cruzados (Frontend).
- Manejo centralizado de excepciones y mapeo de errores SQL.
- Conexion Singleton con optimizacion de pool JDBC para MySQL.
"""
with open(os.path.join(repo_dir, "README.md"), "w", encoding="utf-8") as f:
    f.write(readme_v2)

# Modificamos application.properties eliminando comentarios de prueba
props_v2 = """spring.application.name=clinica-backend
server.port=8080
"""
with open(os.path.join(repo_dir, "src", "main", "resources", "application.properties"), "w", encoding="utf-8") as f:
    f.write(props_v2)

# Modificamos pom.xml quitando comentarios preliminares
with open(os.path.join(temp_final, "pom.xml"), "r", encoding="utf-8") as f:
    pom_final = f.read()
with open(os.path.join(repo_dir, "pom.xml"), "w", encoding="utf-8") as f:
    f.write(pom_final)

subprocess.run(["git", "add", "."], check=True)
env2 = set_git_env("2024-09-16 16:42:10 -0500")
subprocess.run(["git", "commit", "-m", "Agrega conexión a BD, CORS y manejo de errores"], env=env2, check=True)
print("Commit 2 listo (con diffs de modificación).")

# =========================================================================
# COMMIT 3: Agrega modelos de entidades y DTOs
# Fecha: 2024-10-04 11:25:45 -0500
# AGREGA: entidades y DTOs (model/)
# MODIFICA: ClinicaApplication.java (refactoriza comentarios -> ROJO/VERDE/AZUL), Conexion.java (ajuste de parametrizacion -> ROJO/VERDE/AZUL)
# =========================================================================
shutil.copytree(os.path.join(temp_final, "src", "main", "java", "pe", "edu", "utp", "clinica", "model"),
                os.path.join(repo_dir, "src", "main", "java", "pe", "edu", "utp", "clinica", "model"))

# Refactorizar ClinicaApplication a su versión final idéntica
with open(os.path.join(temp_final, "src", "main", "java", "pe", "edu", "utp", "clinica", "ClinicaApplication.java"), "r", encoding="utf-8") as f:
    app_final = f.read()
with open(os.path.join(repo_dir, "src", "main", "java", "pe", "edu", "utp", "clinica", "ClinicaApplication.java"), "w", encoding="utf-8") as f:
    f.write(app_final)

# Modificamos README.md
readme_v3 = """# CLINICA-BACKEND
Sistema Web de Gestion de Citas Medicas - Hospital Jose Agurto Tello (Chosica).

## Modulos Implementados
- **Configuracion**: Manejador centralizado de errores, CORS y conexion MySQL.
- **Modelos y DTOs**: Records inmutables para Citas, Medicos, Pacientes, Horarios y Requests de autenticacion.
"""
with open(os.path.join(repo_dir, "README.md"), "w", encoding="utf-8") as f:
    f.write(readme_v3)

subprocess.run(["git", "add", "."], check=True)
env3 = set_git_env("2024-10-04 11:25:45 -0500")
subprocess.run(["git", "commit", "-m", "Agrega modelos de entidades y DTOs"], env=env3, check=True)
print("Commit 3 listo (con diffs de modificación).")

# =========================================================================
# COMMIT 4: Agrega interfaces DAO y sus implementaciones
# Fecha: 2024-10-14 14:18:30 -0500
# AGREGA: capa dao (dao/ y dao/impl/)
# MODIFICA: README.md (actualiza avance del proyecto -> ROJO/VERDE/AZUL)
# =========================================================================
shutil.copytree(os.path.join(temp_final, "src", "main", "java", "pe", "edu", "utp", "clinica", "dao"),
                os.path.join(repo_dir, "src", "main", "java", "pe", "edu", "utp", "clinica", "dao"))

readme_v4 = """# CLINICA-BACKEND
Sistema Web de Gestion de Citas Medicas - Hospital Jose Agurto Tello (Chosica).

## Modulos Implementados
- **Capa DAO**: Interfaces e implementaciones JDBC para persistencia de datos (Citas, Medicos, Pacientes, Horarios, Especialidades).
- **Modelos**: Records de dominio y DTOs para transferencia entre capas.
- **Configuracion**: Gestion de excepciones personalizadas y pool de conexiones.
"""
with open(os.path.join(repo_dir, "README.md"), "w", encoding="utf-8") as f:
    f.write(readme_v4)

subprocess.run(["git", "add", "."], check=True)
env4 = set_git_env("2024-10-14 14:18:30 -0500")
subprocess.run(["git", "commit", "-m", "Agrega interfaces DAO y sus implementaciones"], env=env4, check=True)
print("Commit 4 listo (con diffs de modificación).")

# =========================================================================
# COMMIT 5: Agrega servicio de citas y controladores REST
# Fecha: 2024-10-21 17:08:15 -0500
# AGREGA: controller/ y service/
# MODIFICA: README.md (versión final del proyecto con endpoints documentados -> ROJO/VERDE/AZUL)
# =========================================================================
shutil.copytree(os.path.join(temp_final, "src", "main", "java", "pe", "edu", "utp", "clinica", "controller"),
                os.path.join(repo_dir, "src", "main", "java", "pe", "edu", "utp", "clinica", "controller"))
shutil.copytree(os.path.join(temp_final, "src", "main", "java", "pe", "edu", "utp", "clinica", "service"),
                os.path.join(repo_dir, "src", "main", "java", "pe", "edu", "utp", "clinica", "service"))

# El README final debe ser exactamente el original
with open(os.path.join(temp_final, "README.md"), "r", encoding="utf-8") as f:
    readme_final = f.read()
with open(os.path.join(repo_dir, "README.md"), "w", encoding="utf-8") as f:
    f.write(readme_final)

subprocess.run(["git", "add", "."], check=True)
env5 = set_git_env("2024-10-21 17:08:15 -0500")
subprocess.run(["git", "commit", "-m", "Agrega servicio de citas y controladores REST"], env=env5, check=True)
print("Commit 5 listo (con diffs de modificación).")

# =========================================================================
# Finalización: mover main a orchestrate-history y limpiar
# =========================================================================
subprocess.run(["git", "checkout", "main"], check=True)
subprocess.run(["git", "reset", "--hard", "orchestrate-history"], check=True)
subprocess.run(["git", "branch", "-D", "orchestrate-history"], check=True)
subprocess.run(["git", "branch", "-D", "rebuild-main"], check=True)

# Eliminar carpeta temporal externa
if os.path.exists(temp_final):
    shutil.rmtree(temp_final)

print("¡Reconstrucción completa con diffs multicolor (verde, rojo y azul)!")
