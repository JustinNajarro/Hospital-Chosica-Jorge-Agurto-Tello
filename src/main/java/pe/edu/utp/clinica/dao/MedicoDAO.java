package pe.edu.utp.clinica.dao;

import java.util.List;

import pe.edu.utp.clinica.model.Medico;

public interface MedicoDAO {
    List<Medico> listarTodos();
    List<Medico> listarPorEspecialidad(int idEspecialidad);
    Medico buscarPorId(int idMedico);
    Medico registrar(Medico medico);
    boolean actualizar(int idMedico, Medico medico);
    boolean eliminar(int idMedico);
}
