package pe.edu.utp.clinica.controller;

import java.util.List;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

import pe.edu.utp.clinica.config.ApiException;
import pe.edu.utp.clinica.dao.EspecialidadDAO;
import pe.edu.utp.clinica.dao.MedicoDAO;
import pe.edu.utp.clinica.model.Especialidad;
import pe.edu.utp.clinica.model.Medico;

@RestController
@RequestMapping("/api/especialidades")
public class EspecialidadController {

    private final EspecialidadDAO especialidadDAO;
    private final MedicoDAO medicoDAO;

    public EspecialidadController(EspecialidadDAO especialidadDAO, MedicoDAO medicoDAO) {
        this.especialidadDAO = especialidadDAO;
        this.medicoDAO = medicoDAO;
    }

    @GetMapping
    public List<Especialidad> listar() {
        return especialidadDAO.listar();
    }

    @GetMapping("/{id}/medicos")
    public List<Medico> medicos(@PathVariable("id") int id) {
        return medicoDAO.listarPorEspecialidad(id);
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Especialidad registrar(@RequestBody Especialidad e) {
        validar(e);
        return especialidadDAO.registrar(new Especialidad(0, e.nombre().trim(), e.descripcion()));
    }

    @PutMapping("/{id}")
    public Especialidad actualizar(@PathVariable("id") int id, @RequestBody Especialidad e) {
        validar(e);
        Especialidad datos = new Especialidad(id, e.nombre().trim(), e.descripcion());
        if (!especialidadDAO.actualizar(id, datos)) {
            throw new ApiException(HttpStatus.NOT_FOUND, "La especialidad no existe.");
        }
        return datos;
    }

    @DeleteMapping("/{id}")
    public void eliminar(@PathVariable("id") int id) {
        if (!especialidadDAO.eliminar(id)) {
            throw new ApiException(HttpStatus.NOT_FOUND, "La especialidad no existe.");
        }
    }

    private void validar(Especialidad e) {
        if (e == null || e.nombre() == null || e.nombre().isBlank()) {
            throw new ApiException(HttpStatus.BAD_REQUEST, "El nombre de la especialidad es obligatorio.");
        }
    }
}
