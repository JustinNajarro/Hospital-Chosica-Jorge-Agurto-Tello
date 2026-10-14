package pe.edu.utp.clinica.dao;

import java.time.LocalTime;
import java.util.List;

import pe.edu.utp.clinica.model.HorarioMedico;

public interface HorarioDAO {
    List<HorarioMedico> listarPorMedicoYDia(int idMedico, String diaSemana);
    List<HorarioMedico> listarPorMedico(int idMedico);
    HorarioMedico registrar(HorarioMedico horario);
    boolean eliminar(int idHorario);
    boolean medicoOcupado(int idMedico, String dia, LocalTime inicio, LocalTime fin);
    boolean consultorioOcupado(int idConsultorio, String dia, LocalTime inicio, LocalTime fin);
}
