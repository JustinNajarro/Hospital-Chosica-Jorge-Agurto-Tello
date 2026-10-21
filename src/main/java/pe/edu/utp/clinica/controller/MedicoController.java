package pe.edu.utp.clinica.controller;

import java.util.List;
import java.util.Set;

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
import pe.edu.utp.clinica.dao.ConsultorioDAO;
import pe.edu.utp.clinica.dao.HorarioDAO;
import pe.edu.utp.clinica.dao.MedicoDAO;
import pe.edu.utp.clinica.model.Consultorio;
import pe.edu.utp.clinica.model.HorarioMedico;
import pe.edu.utp.clinica.model.Medico;

/** Gestion de medicos, sus horarios y consultorios (panel del administrador). */
@RestController
@RequestMapping("/api")
public class MedicoController {

    private static final Set<String> DIAS =
            Set.of("LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES", "SABADO");

    private final MedicoDAO medicoDAO;
    private final HorarioDAO horarioDAO;
    private final ConsultorioDAO consultorioDAO;

    public MedicoController(MedicoDAO medicoDAO, HorarioDAO horarioDAO, ConsultorioDAO consultorioDAO) {
        this.medicoDAO = medicoDAO;
        this.horarioDAO = horarioDAO;
        this.consultorioDAO = consultorioDAO;
    }

    // ---------- Medicos ----------
    @GetMapping("/medicos")
    public List<Medico> listar() {
        return medicoDAO.listarTodos();
    }

    @PostMapping("/medicos")
    @ResponseStatus(HttpStatus.CREATED)
    public Medico registrar(@RequestBody Medico m) {
        validar(m);
        return medicoDAO.registrar(m);
    }

    @PutMapping("/medicos/{id}")
    public Medico actualizar(@PathVariable("id") int id, @RequestBody Medico m) {
        validar(m);
        if (!medicoDAO.actualizar(id, m)) {
            throw new ApiException(HttpStatus.NOT_FOUND, "El medico no existe.");
        }
        return medicoDAO.buscarPorId(id);
    }

    @DeleteMapping("/medicos/{id}")
    public void eliminar(@PathVariable("id") int id) {
        if (!medicoDAO.eliminar(id)) {
            throw new ApiException(HttpStatus.NOT_FOUND, "El medico no existe.");
        }
    }

    // ---------- Horarios ----------
    @GetMapping("/medicos/{id}/horarios")
    public List<HorarioMedico> horarios(@PathVariable("id") int idMedico) {
        return horarioDAO.listarPorMedico(idMedico);
    }

    @PostMapping("/medicos/{id}/horarios")
    @ResponseStatus(HttpStatus.CREATED)
    public HorarioMedico agregarHorario(@PathVariable("id") int idMedico, @RequestBody HorarioMedico h) {
        String dia = h.diaSemana() == null ? "" : h.diaSemana().toUpperCase();
        if (!DIAS.contains(dia)) {
            throw new ApiException(HttpStatus.BAD_REQUEST, "Elige un dia de lunes a sabado.");
        }
        if (h.horaInicio() == null || h.horaFin() == null || !h.horaFin().isAfter(h.horaInicio())) {
            throw new ApiException(HttpStatus.BAD_REQUEST, "La hora de fin debe ser mayor que la hora de inicio.");
        }
        if (h.idConsultorio() <= 0) {
            throw new ApiException(HttpStatus.BAD_REQUEST, "Elige un consultorio.");
        }
        if (medicoDAO.buscarPorId(idMedico) == null) {
            throw new ApiException(HttpStatus.NOT_FOUND, "El medico no existe.");
        }
        if (horarioDAO.medicoOcupado(idMedico, dia, h.horaInicio(), h.horaFin())) {
            throw new ApiException(HttpStatus.CONFLICT, "El medico ya tiene un horario que se cruza ese dia.");
        }
        if (horarioDAO.consultorioOcupado(h.idConsultorio(), dia, h.horaInicio(), h.horaFin())) {
            throw new ApiException(HttpStatus.CONFLICT, "Ese consultorio ya esta ocupado por otro medico en ese horario.");
        }
        return horarioDAO.registrar(new HorarioMedico(0, idMedico, h.idConsultorio(), dia, h.horaInicio(), h.horaFin()));
    }

    @DeleteMapping("/horarios/{id}")
    public void eliminarHorario(@PathVariable("id") int idHorario) {
        if (!horarioDAO.eliminar(idHorario)) {
            throw new ApiException(HttpStatus.NOT_FOUND, "El horario no existe.");
        }
    }

    // ---------- Consultorios ----------
    @GetMapping("/consultorios")
    public List<Consultorio> consultorios() {
        return consultorioDAO.listar();
    }

    private void validar(Medico m) {
        if (m == null || vacio(m.nombres()) || vacio(m.apellidos()) || vacio(m.codigoDoctor())) {
            throw new ApiException(HttpStatus.BAD_REQUEST, "Completa nombres, apellidos y codigo CMP.");
        }
        if (m.dni() == null || !m.dni().matches("\\d{8}")) {
            throw new ApiException(HttpStatus.BAD_REQUEST, "El DNI debe tener 8 digitos.");
        }
        if (m.idEspecialidad() <= 0) {
            throw new ApiException(HttpStatus.BAD_REQUEST, "Elige una especialidad.");
        }
    }

    private boolean vacio(String s) {
        return s == null || s.isBlank();
    }
}
