package pe.edu.utp.clinica.dao.impl;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.time.LocalTime;
import java.util.ArrayList;
import java.util.List;

import org.springframework.stereotype.Repository;

import pe.edu.utp.clinica.config.Conexion;
import pe.edu.utp.clinica.config.ErroresSQL;
import pe.edu.utp.clinica.dao.HorarioDAO;
import pe.edu.utp.clinica.model.HorarioMedico;

@Repository
public class HorarioDAOImpl implements HorarioDAO {

    private static final String COLUMNAS =
            "id_horario, id_medico, id_consultorio, dia_semana, hora_inicio, hora_fin";
    private static final String ORDEN_DIAS =
            "FIELD(dia_semana, 'LUNES','MARTES','MIERCOLES','JUEVES','VIERNES','SABADO','DOMINGO')";

    @Override
    public List<HorarioMedico> listarPorMedicoYDia(int idMedico, String diaSemana) {
        return consultar("SELECT " + COLUMNAS + " FROM horario_medico WHERE id_medico = ? AND dia_semana = ? "
                + "ORDER BY hora_inicio", idMedico, diaSemana);
    }

    @Override
    public List<HorarioMedico> listarPorMedico(int idMedico) {
        return consultar("SELECT " + COLUMNAS + " FROM horario_medico WHERE id_medico = ? "
                + "ORDER BY " + ORDEN_DIAS + ", hora_inicio", idMedico);
    }

    @Override
    public HorarioMedico registrar(HorarioMedico h) {
        String sql = "INSERT INTO horario_medico (id_medico, id_consultorio, dia_semana, hora_inicio, hora_fin) "
                + "VALUES (?, ?, ?, ?, ?)";
        try (Connection cn = Conexion.getInstancia().getConnection();
             PreparedStatement ps = cn.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {
            ps.setInt(1, h.idMedico());
            ps.setInt(2, h.idConsultorio());
            ps.setString(3, h.diaSemana());
            ps.setObject(4, h.horaInicio());
            ps.setObject(5, h.horaFin());
            ps.executeUpdate();
            try (ResultSet rs = ps.getGeneratedKeys()) {
                rs.next();
                return new HorarioMedico(rs.getInt(1), h.idMedico(), h.idConsultorio(),
                        h.diaSemana(), h.horaInicio(), h.horaFin());
            }
        } catch (SQLException e) {
            throw ErroresSQL.traducir(e, "registrar horario");
        }
    }

    @Override
    public boolean eliminar(int idHorario) {
        try (Connection cn = Conexion.getInstancia().getConnection();
             PreparedStatement ps = cn.prepareStatement("DELETE FROM horario_medico WHERE id_horario = ?")) {
            ps.setInt(1, idHorario);
            return ps.executeUpdate() > 0;
        } catch (SQLException e) {
            throw ErroresSQL.traducir(e, "eliminar horario");
        }
    }

    @Override
    public boolean medicoOcupado(int idMedico, String dia, LocalTime inicio, LocalTime fin) {
        return existe("SELECT 1 FROM horario_medico WHERE id_medico = ? AND dia_semana = ? "
                + "AND hora_inicio < ? AND hora_fin > ?", idMedico, dia, fin, inicio);
    }

    @Override
    public boolean consultorioOcupado(int idConsultorio, String dia, LocalTime inicio, LocalTime fin) {
        return existe("SELECT 1 FROM horario_medico WHERE id_consultorio = ? AND dia_semana = ? "
                + "AND hora_inicio < ? AND hora_fin > ?", idConsultorio, dia, fin, inicio);
    }

    private boolean existe(String sql, Object... params) {
        try (Connection cn = Conexion.getInstancia().getConnection();
             PreparedStatement ps = cn.prepareStatement(sql)) {
            for (int i = 0; i < params.length; i++) {
                ps.setObject(i + 1, params[i]);
            }
            try (ResultSet rs = ps.executeQuery()) {
                return rs.next();
            }
        } catch (SQLException e) {
            throw ErroresSQL.traducir(e, "verificar horario");
        }
    }

    private List<HorarioMedico> consultar(String sql, Object... params) {
        List<HorarioMedico> lista = new ArrayList<>();
        try (Connection cn = Conexion.getInstancia().getConnection();
             PreparedStatement ps = cn.prepareStatement(sql)) {
            for (int i = 0; i < params.length; i++) {
                ps.setObject(i + 1, params[i]);
            }
            try (ResultSet rs = ps.executeQuery()) {
                while (rs.next()) {
                    lista.add(new HorarioMedico(
                            rs.getInt("id_horario"),
                            rs.getInt("id_medico"),
                            rs.getInt("id_consultorio"),
                            rs.getString("dia_semana"),
                            rs.getObject("hora_inicio", LocalTime.class),
                            rs.getObject("hora_fin", LocalTime.class)));
                }
            }
        } catch (SQLException e) {
            throw ErroresSQL.traducir(e, "listar horarios");
        }
        return lista;
    }
}
