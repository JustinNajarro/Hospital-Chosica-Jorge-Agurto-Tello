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
import pe.edu.utp.clinica.dao.EspecialidadDAO;
import pe.edu.utp.clinica.model.Especialidad;

@Repository
public class EspecialidadDAOImpl implements EspecialidadDAO {

    @Override
    public List<Especialidad> listar() {
        String sql = "SELECT id_especialidad, nombre_especialidad, descripcion FROM especialidad ORDER BY nombre_especialidad";
        List<Especialidad> lista = new ArrayList<>();
        try (Connection cn = Conexion.getInstancia().getConnection();
             PreparedStatement ps = cn.prepareStatement(sql);
             ResultSet rs = ps.executeQuery()) {
            while (rs.next()) {
                lista.add(new Especialidad(
                        rs.getInt("id_especialidad"),
                        rs.getString("nombre_especialidad"),
                        rs.getString("descripcion")));
            }
        } catch (SQLException e) {
            throw ErroresSQL.traducir(e, "listar especialidades");
        }
        return lista;
    }

    @Override
    public Especialidad registrar(Especialidad e) {
        String sql = "INSERT INTO especialidad (nombre_especialidad, descripcion) VALUES (?, ?)";
        try (Connection cn = Conexion.getInstancia().getConnection();
             PreparedStatement ps = cn.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {
            ps.setString(1, e.nombre());
            ps.setString(2, e.descripcion());
            ps.executeUpdate();
            try (ResultSet rs = ps.getGeneratedKeys()) {
                rs.next();
                return new Especialidad(rs.getInt(1), e.nombre(), e.descripcion());
            }
        } catch (SQLException ex) {
            throw ErroresSQL.traducir(ex, "registrar especialidad");
        }
    }

    @Override
    public boolean actualizar(int id, Especialidad e) {
        String sql = "UPDATE especialidad SET nombre_especialidad = ?, descripcion = ? WHERE id_especialidad = ?";
        try (Connection cn = Conexion.getInstancia().getConnection();
             PreparedStatement ps = cn.prepareStatement(sql)) {
            ps.setString(1, e.nombre());
            ps.setString(2, e.descripcion());
            ps.setInt(3, id);
            return ps.executeUpdate() > 0;
        } catch (SQLException ex) {
            throw ErroresSQL.traducir(ex, "actualizar especialidad");
        }
    }

    @Override
    public boolean eliminar(int id) {
        String sql = "DELETE FROM especialidad WHERE id_especialidad = ?";
        try (Connection cn = Conexion.getInstancia().getConnection();
             PreparedStatement ps = cn.prepareStatement(sql)) {
            ps.setInt(1, id);
            return ps.executeUpdate() > 0;
        } catch (SQLException ex) {
            throw ErroresSQL.traducir(ex, "eliminar especialidad");
        }
    }
}
