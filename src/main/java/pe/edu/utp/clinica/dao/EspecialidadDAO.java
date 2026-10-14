package pe.edu.utp.clinica.dao;

import java.util.List;

import pe.edu.utp.clinica.model.Especialidad;

public interface EspecialidadDAO {
    List<Especialidad> listar();
    Especialidad registrar(Especialidad especialidad);
    boolean actualizar(int idEspecialidad, Especialidad especialidad);
    boolean eliminar(int idEspecialidad);
}
