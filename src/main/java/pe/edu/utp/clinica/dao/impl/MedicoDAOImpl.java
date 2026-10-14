package pe.edu.utp.clinica.dao.impl;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

import org.springframework.stereotype.Repository;

import pe.edu.utp.clinica.config.Conexion;
import pe.edu.utp.clinica.config.ErroresSQL;
import pe.edu.utp.clinica.dao.MedicoDAO;
import pe.edu.utp.clinica.model.Medico;

@Repository
public class MedicoDAOImpl implements MedicoDAO {

    private static final String COLUMNAS =
            "id_medico, dni, nombres, apellidos, telefono, correo, codigo_doctor, id_especialidad";

    @Override
    public List<Medico> listarTodos() {
        return consultar("SELECT " + COLUMNAS + " FROM medico ORDER BY apellidos, nombres");
    }

    @Override
    public List<Medico> listarPorEspecialidad(int idEspecialidad) {
        return consultar("SELECT " + COLUMNAS + " FROM medico WHERE id_especialidad = ? ORDER BY apellidos", idEspecialidad);
    }

    @Override
    public Medico buscarPorId(int idMedico) {
        List<Medico> r = consultar("SELECT " + COLUMNAS + " FROM medico WHERE id_medico = ?", idMedico);
        return r.isEmpty() ? null : r.get(0);
    }

    @Override
    public Medico registrar(Medico m) {
        String sql = "INSERT INTO medico (dni, nombres, apellidos, telefono, correo, codigo_doctor, id_especialidad) "
                + "VALUES (?, ?, ?, ?, ?, ?, ?)";
        try (Connection cn = Conexion.getInstancia().getConnection();
             PreparedStatement ps = cn.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {
            llenar(ps, m);
            ps.executeUpdate();
            try (ResultSet rs = ps.getGeneratedKeys()) {
                rs.next();
                return buscarPorId(rs.getInt(1));
            }
        } catch (SQLException e) {
            throw ErroresSQL.traducir(e, "registrar medico");
        }
    }

    @Override
    public boolean actualizar(int idMedico, Medico m) {
        String sql = "UPDATE medico SET dni = ?, nombres = ?, apellidos = ?, telefono = ?, correo = ?, "
                + "codigo_doctor = ?, id_especialidad = ? WHERE id_medico = ?";
        try (Connection cn = Conexion.getInstancia().getConnection();
             PreparedStatement ps = cn.prepareStatement(sql)) {
            llenar(ps, m);
            ps.setInt(8, idMedico);
            return ps.executeUpdate() > 0;
        } catch (SQLException e) {
            throw ErroresSQL.traducir(e, "actualizar medico");
        }
    }

    /** Borra primero sus horarios y luego al medico. Si tiene citas, MySQL lo impide. */
    @Override
    public boolean eliminar(int idMedico) {
        try (Connection cn = Conexion.getInstancia().getConnection()) {
            cn.setAutoCommit(false);
            try (PreparedStatement ps1 = cn.prepareStatement("DELETE FROM horario_medico WHERE id_medico = ?");
                 PreparedStatement ps2 = cn.prepareStatement("DELETE FROM medico WHERE id_medico = ?")) {
                ps1.setInt(1, idMedico);
                ps1.executeUpdate();
                ps2.setInt(1, idMedico);
                int filas = ps2.executeUpdate();
                cn.commit();
                return filas > 0;
            } catch (SQLException e) {
                cn.rollback();
                throw e;
            }
        } catch (SQLException e) {
            throw ErroresSQL.traducir(e, "eliminar medico");
        }
    }

    private void llenar(PreparedStatement ps, Medico m) throws SQLException {
        ps.setString(1, m.dni());
        ps.setString(2, m.nombres());
        ps.setString(3, m.apellidos());
        ps.setString(4, m.telefono());
        ps.setString(5, m.correo());
        ps.setString(6, m.codigoDoctor());
        ps.setInt(7, m.idEspecialidad());
    }

    private List<Medico> consultar(String sql, Object... params) {
        List<Medico> lista = new ArrayList<>();
        try (Connection cn = Conexion.getInstancia().getConnection();
             PreparedStatement ps = cn.prepareStatement(sql)) {
            for (int i = 0; i < params.length; i++) {
                ps.setObject(i + 1, params[i]);
            }
            try (ResultSet rs = ps.executeQuery()) {
                while (rs.next()) {
                    lista.add(new Medico(
                            rs.getInt("id_medico"),
                            rs.getString("dni"),
                            rs.getString("nombres"),
                            rs.getString("apellidos"),
                            rs.getString("telefono"),
                            rs.getString("correo"),
                            rs.getString("codigo_doctor"),
                            rs.getInt("id_especialidad")));
                }
            }
        } catch (SQLException e) {
            throw ErroresSQL.traducir(e, "consultar medicos");
        }
        return lista;
    }
}
