package pe.edu.utp.clinica.controller;

import java.time.LocalDate;
import java.util.List;
import java.util.Set;

import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

import pe.edu.utp.clinica.config.ApiException;
import pe.edu.utp.clinica.dao.CitaDAO;
import pe.edu.utp.clinica.model.Cita;
import pe.edu.utp.clinica.model.dto.CitaRequest;
import pe.edu.utp.clinica.model.dto.EstadoRequest;
import pe.edu.utp.clinica.model.dto.Turno;
import pe.edu.utp.clinica.service.CitaService;

/**
 * Controlador REST de citas médicas.
 * <p>
 * Atiende la consulta de disponibilidad, la reserva y cancelación de citas
 * del paciente, y la gestión de estados desde el panel del administrador.
 *
 * @author Justin Najarro
 * @version 1.1
 */
@RestController
@RequestMapping("/api")
public class CitaController {

    /** Estados válidos de una cita. */
    private static final Set<String> ESTADOS = Set.of("PENDIENTE", "ATENDIDA", "CANCELADA");

    private final CitaService citaService;
    private final CitaDAO citaDAO;

    /**
     * Crea el controlador con sus dependencias.
     *
     * @param citaService reglas de negocio de las citas
     * @param citaDAO     acceso a citas
     */
    public CitaController(CitaService citaService, CitaDAO citaDAO) {
        this.citaService = citaService;
        this.citaDAO = citaDAO;
    }

    /**
     * Turnos libres de un médico en una fecha.
     * Endpoint: {@code GET /api/medicos/{id}/disponibilidad?fecha=AAAA-MM-DD}.
     *
     * @param idMedico id del médico
     * @param fecha    fecha en formato ISO
     * @return turnos disponibles
     */
    @GetMapping("/medicos/{id}/disponibilidad")
    public List<Turno> disponibilidad(@PathVariable("id") int idMedico,
                                      @RequestParam("fecha") @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate fecha) {
        return citaService.disponibilidad(idMedico, fecha);
    }

    /**
     * Reserva una cita. Endpoint: {@code POST /api/citas}.
     *
     * @param req datos de la reserva
     * @return la cita registrada con su código de confirmación
     */
    @PostMapping("/citas")
    @ResponseStatus(HttpStatus.CREATED)
    public Cita reservar(@RequestBody CitaRequest req) {
        return citaService.reservar(req);
    }

    /**
     * Citas de un paciente. Endpoint: {@code GET /api/citas/paciente/{dni}}.
     *
     * @param dni DNI del paciente
     * @return citas del paciente
     */
    @GetMapping("/citas/paciente/{dni}")
    public List<Cita> citasDelPaciente(@PathVariable("dni") String dni) {
        return citaDAO.listarPorPaciente(dni);
    }

    /**
     * Cancela una cita del paciente. Endpoint: {@code PUT /api/citas/{id}/cancelar?dni=...}.
     * <p>
     * Responde 204 (sin cuerpo): el frontend vuelve a cargar la lista, así que
     * no hace falta consultar otra vez todas las citas del paciente.
     *
     * @param idCita id de la cita
     * @param dni    DNI del paciente dueño de la cita
     * @throws ApiException 400 si no existe o ya no está pendiente
     */
    @PutMapping("/citas/{id}/cancelar")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void cancelar(@PathVariable("id") int idCita, @RequestParam("dni") String dni) {
        Validar.exigir(citaDAO.cancelar(idCita, dni), "La cita no existe o ya no está pendiente.");
    }

    /**
     * Todas las citas, para el panel del administrador. Endpoint: {@code GET /api/citas}.
     *
     * @return todas las citas
     */
    @GetMapping("/citas")
    public List<Cita> listarTodas() {
        return citaDAO.listarTodas();
    }

    /**
     * Cambia el estado de una cita. Endpoint: {@code PUT /api/citas/{id}/estado}.
     *
     * @param idCita id de la cita
     * @param req    nuevo estado
     * @throws ApiException 400 si el estado no es válido; 404 si la cita no existe
     */
    @PutMapping("/citas/{id}/estado")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void cambiarEstado(@PathVariable("id") int idCita, @RequestBody EstadoRequest req) {
        String estado = Validar.normalizar(req.estado());
        Validar.exigir(ESTADOS.contains(estado), "Estado inválido. Usa PENDIENTE, ATENDIDA o CANCELADA.");
        Validar.existe(citaDAO.actualizarEstado(idCita, estado), "La cita no existe.");
    }
}
