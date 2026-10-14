package pe.edu.utp.clinica.dao.impl;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

import org.springframework.stereotype.Repository;

import pe.edu.utp.clinica.config.Conexion;
import pe.edu.utp.clinica.config.ErroresSQL;
import pe.edu.utp.clinica.dao.ConsultorioDAO;
import pe.edu.utp.clinica.model.Consultorio;

@Repository
public class ConsultorioDAOImpl implements ConsultorioDAO {

    @Override
    public List<Consultorio> listar() {
        String sql = "SELECT id_consultorio, numero_sala, piso, estado FROM consultorio ORDER BY numero_sala";
        List<Consultorio> lista = new ArrayList<>();
        try (Connection cn = Conexion.getInstancia().getConnection();
             PreparedStatement ps = cn.prepareStatement(sql);
             ResultSet rs = ps.executeQuery()) {
            while (rs.next()) {
                lista.add(new Consultorio(
                        rs.getInt("id_consultorio"),
                        rs.getString("numero_sala"),
                        rs.getInt("piso"),
                        rs.getString("estado")));
            }
        } catch (SQLException e) {
            throw ErroresSQL.traducir(e, "listar consultorios");
        }
        return lista;
    }
}
