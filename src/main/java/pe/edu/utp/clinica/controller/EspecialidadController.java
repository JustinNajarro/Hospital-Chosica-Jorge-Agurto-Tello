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

/**
 * Controlador REST de especialidades ({@code /api/especialidades}).
 * <p>
 * El paciente lo usa para elegir especialidad al agendar y el administrador
 * para registrar, editar y eliminar especialidades.
 *
 * @author Justin Najarro
 * @version 1.1
 */
@RestController
@RequestMapping("/api/especialidades")
public class EspecialidadController {

    /** Mensaje cuando la especialidad buscada no existe. */
    private static final String NO_EXISTE = "La especialidad no existe.";

    private final EspecialidadDAO especialidadDAO;
    private final MedicoDAO medicoDAO;

    /**
     * Crea el controlador con los DAO que necesita.
     *
     * @param especialidadDAO acceso a especialidades
     * @param medicoDAO       acceso a médicos
     */
    public EspecialidadController(EspecialidadDAO especialidadDAO, MedicoDAO medicoDAO) {
        this.especialidadDAO = especialidadDAO;
        this.medicoDAO = medicoDAO;
    }

    /**
     * Lista las especialidades. Endpoint: {@code GET /api/especialidades}.
     *
     * @return todas las especialidades
     */
    @GetMapping
    public List<Especialidad> listar() {
        return especialidadDAO.listar();
    }

    /**
     * Lista los médicos de una especialidad. Endpoint: {@code GET /api/especialidades/{id}/medicos}.
     *
     * @param id id de la especialidad
     * @return médicos de esa especialidad
     */
    @GetMapping("/{id}/medicos")
    public List<Medico> medicos(@PathVariable("id") int id) {
        return medicoDAO.listarPorEspecialidad(id);
    }

    /**
     * Registra una especialidad. Endpoint: {@code POST /api/especialidades}.
     *
     * @param e datos de la especialidad
     * @return la especialidad creada
     * @throws ApiException 400 si no tiene nombre; 409 si el nombre ya existe
     */
    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Especialidad registrar(@RequestBody Especialidad e) {
        return especialidadDAO.registrar(limpiar(0, e));
    }

    /**
     * Actualiza una especialidad. Endpoint: {@code PUT /api/especialidades/{id}}.
     *
     * @param id id de la especialidad
     * @param e  nuevos datos
     * @return la especialidad actualizada
     * @throws ApiException 404 si no existe
     */
    @PutMapping("/{id}")
    public Especialidad actualizar(@PathVariable("id") int id, @RequestBody Especialidad e) {
        Especialidad datos = limpiar(id, e);
        Validar.existe(especialidadDAO.actualizar(id, datos), NO_EXISTE);
        return datos;
    }

    /**
     * Elimina una especialidad. Endpoint: {@code DELETE /api/especialidades/{id}}.
     *
     * @param id id de la especialidad
     * @throws ApiException 404 si no existe; 409 si tiene médicos asignados
     */
    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void eliminar(@PathVariable("id") int id) {
        Validar.existe(especialidadDAO.eliminar(id), NO_EXISTE);
    }

    /**
     * Valida que la especialidad tenga nombre y devuelve una copia con el
     * id indicado y el nombre sin espacios sobrantes.
     *
     * @param id id que tendrá la especialidad (0 si es nueva)
     * @param e  datos recibidos
     * @return especialidad lista para guardar
     * @throws ApiException 400 si el nombre está vacío
     */
    private static Especialidad limpiar(int id, Especialidad e) {
        Validar.exigir(e != null && Validar.conTexto(e.nombre()), "El nombre de la especialidad es obligatorio.");
        return new Especialidad(id, e.nombre().trim(), e.descripcion());
    }
}
