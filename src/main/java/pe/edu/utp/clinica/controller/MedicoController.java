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

/**
 * Controlador REST para gestionar médicos, sus horarios y consultorios.
 * <p>
 * Lo usa el panel del administrador. Rutas: {@code /api/medicos},
 * {@code /api/medicos/{id}/horarios}, {@code /api/horarios/{id}} y
 * {@code /api/consultorios}.
 *
 * @author Justin Najarro
 * @version 1.1
 */
@RestController
@RequestMapping("/api")
public class MedicoController {

    /** Días en los que se puede registrar un horario. */
    private static final Set<String> DIAS =
            Set.of("LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES", "SABADO");

    /** Mensaje cuando el médico buscado no existe. */
    private static final String MEDICO_NO_EXISTE = "El médico no existe.";

    private final MedicoDAO medicoDAO;
    private final HorarioDAO horarioDAO;
    private final ConsultorioDAO consultorioDAO;

    /**
     * Crea el controlador con los DAO que necesita.
     *
     * @param medicoDAO      acceso a médicos
     * @param horarioDAO     acceso a horarios
     * @param consultorioDAO acceso a consultorios
     */
    public MedicoController(MedicoDAO medicoDAO, HorarioDAO horarioDAO, ConsultorioDAO consultorioDAO) {
        this.medicoDAO = medicoDAO;
        this.horarioDAO = horarioDAO;
        this.consultorioDAO = consultorioDAO;
    }

    // ==================== Médicos ====================

    /**
     * Lista todos los médicos. Endpoint: {@code GET /api/medicos}.
     *
     * @return todos los médicos
     */
    @GetMapping("/medicos")
    public List<Medico> listar() {
        return medicoDAO.listarTodos();
    }

    /**
     * Registra un médico. Endpoint: {@code POST /api/medicos}.
     *
     * @param m datos del médico
     * @return el médico registrado
     * @throws ApiException 400 si faltan datos; 409 si el DNI o el CMP ya existen
     */
    @PostMapping("/medicos")
    @ResponseStatus(HttpStatus.CREATED)
    public Medico registrar(@RequestBody Medico m) {
        validarMedico(m);
        return medicoDAO.registrar(m);
    }

    /**
     * Actualiza un médico. Endpoint: {@code PUT /api/medicos/{id}}.
     * <p>
     * Devuelve los mismos datos guardados, sin volver a consultar la base de datos.
     *
     * @param id id del médico
     * @param m  nuevos datos
     * @return el médico actualizado
     * @throws ApiException 404 si no existe
     */
    @PutMapping("/medicos/{id}")
    public Medico actualizar(@PathVariable("id") int id, @RequestBody Medico m) {
        validarMedico(m);
        Validar.existe(medicoDAO.actualizar(id, m), MEDICO_NO_EXISTE);
        return new Medico(id, m.dni(), m.nombres(), m.apellidos(), m.telefono(),
                m.correo(), m.codigoDoctor(), m.idEspecialidad());
    }

    /**
     * Elimina un médico y sus horarios. Endpoint: {@code DELETE /api/medicos/{id}}.
     *
     * @param id id del médico
     * @throws ApiException 404 si no existe; 409 si tiene citas
     */
    @DeleteMapping("/medicos/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void eliminar(@PathVariable("id") int id) {
        Validar.existe(medicoDAO.eliminar(id), MEDICO_NO_EXISTE);
    }

    // ==================== Horarios ====================

    /**
     * Lista los horarios de un médico. Endpoint: {@code GET /api/medicos/{id}/horarios}.
     *
     * @param idMedico id del médico
     * @return bloques de atención del médico
     */
    @GetMapping("/medicos/{id}/horarios")
    public List<HorarioMedico> horarios(@PathVariable("id") int idMedico) {
        return horarioDAO.listarPorMedico(idMedico);
    }

    /**
     * Agrega un bloque de atención a un médico. Endpoint: {@code POST /api/medicos/{id}/horarios}.
     * <p>
     * Primero valida los datos (sin tocar la BD) y luego, en este orden, que el
     * médico exista, que no tenga otro horario que se cruce y que el consultorio
     * esté libre en ese rango.
     *
     * @param idMedico id del médico
     * @param h        datos del bloque
     * @return el bloque registrado
     * @throws ApiException 400 si los datos son inválidos; 404 si el médico no existe; 409 si hay cruce
     */
    @PostMapping("/medicos/{id}/horarios")
    @ResponseStatus(HttpStatus.CREATED)
    public HorarioMedico agregarHorario(@PathVariable("id") int idMedico, @RequestBody HorarioMedico h) {
        String dia = Validar.normalizar(h.diaSemana());
        validarHorario(dia, h);

        Validar.existe(medicoDAO.buscarPorId(idMedico) != null, MEDICO_NO_EXISTE);
        Validar.sinConflicto(horarioDAO.medicoOcupado(idMedico, dia, h.horaInicio(), h.horaFin()),
                "El médico ya tiene un horario que se cruza ese día.");
        Validar.sinConflicto(horarioDAO.consultorioOcupado(h.idConsultorio(), dia, h.horaInicio(), h.horaFin()),
                "Ese consultorio ya está ocupado por otro médico en ese horario.");

        return horarioDAO.registrar(
                new HorarioMedico(0, idMedico, h.idConsultorio(), dia, h.horaInicio(), h.horaFin()));
    }

    /**
     * Elimina un bloque de atención. Endpoint: {@code DELETE /api/horarios/{id}}.
     *
     * @param idHorario id del bloque
     * @throws ApiException 404 si no existe
     */
    @DeleteMapping("/horarios/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void eliminarHorario(@PathVariable("id") int idHorario) {
        Validar.existe(horarioDAO.eliminar(idHorario), "El horario no existe.");
    }

    // ==================== Consultorios ====================

    /**
     * Lista los consultorios. Endpoint: {@code GET /api/consultorios}.
     *
     * @return todos los consultorios
     */
    @GetMapping("/consultorios")
    public List<Consultorio> consultorios() {
        return consultorioDAO.listar();
    }

    // ==================== Validaciones ====================

    /**
     * Verifica los datos obligatorios de un médico.
     *
     * @param m médico a validar
     * @throws ApiException 400 si falta algún dato o el DNI no tiene 8 dígitos
     */
    private static void validarMedico(Medico m) {
        Validar.exigir(m != null && Validar.conTexto(m.nombres(), m.apellidos(), m.codigoDoctor()),
                "Completa nombres, apellidos y código CMP.");
        Validar.exigir(Validar.esDni(m.dni()), "El DNI debe tener 8 dígitos.");
        Validar.exigir(m.idEspecialidad() > 0, "Elige una especialidad.");
    }

    /**
     * Verifica el día, el rango de horas y el consultorio de un bloque de atención.
     *
     * @param dia día ya normalizado
     * @param h   bloque a validar
     * @throws ApiException 400 si algún dato no es válido
     */
    private static void validarHorario(String dia, HorarioMedico h) {
        Validar.exigir(DIAS.contains(dia), "Elige un día de lunes a sábado.");
        Validar.exigir(h.horaInicio() != null && h.horaFin() != null && h.horaFin().isAfter(h.horaInicio()),
                "La hora de fin debe ser mayor que la hora de inicio.");
        Validar.exigir(h.idConsultorio() > 0, "Elige un consultorio.");
    }
}
