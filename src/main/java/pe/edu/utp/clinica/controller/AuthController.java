package pe.edu.utp.clinica.controller;

import java.util.Optional;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

import pe.edu.utp.clinica.config.ApiException;
import pe.edu.utp.clinica.dao.AdministradorDAO;
import pe.edu.utp.clinica.dao.PacienteDAO;
import pe.edu.utp.clinica.model.Administrador;
import pe.edu.utp.clinica.model.Paciente;
import pe.edu.utp.clinica.model.dto.LoginAdminRequest;
import pe.edu.utp.clinica.model.dto.LoginPacienteRequest;
import pe.edu.utp.clinica.model.dto.RegistroPacienteRequest;

/**
 * Controlador REST de autenticación ({@code /api/auth}).
 * <p>
 * Maneja el inicio de sesión de pacientes y del personal administrativo,
 * y el registro de nuevos pacientes.
 *
 * @author Justin Najarro
 * @version 1.1
 */
@RestController
@RequestMapping("/api/auth")
public class AuthController {

    private final PacienteDAO pacienteDAO;
    private final AdministradorDAO administradorDAO;

    /**
     * Crea el controlador con los DAO que necesita.
     *
     * @param pacienteDAO      acceso a pacientes
     * @param administradorDAO acceso al personal administrativo
     */
    public AuthController(PacienteDAO pacienteDAO, AdministradorDAO administradorDAO) {
        this.pacienteDAO = pacienteDAO;
        this.administradorDAO = administradorDAO;
    }

    /**
     * Inicia sesión de un paciente. Endpoint: {@code POST /api/auth/paciente/login}.
     *
     * @param req DNI y contraseña
     * @return datos del paciente
     * @throws ApiException 401 si las credenciales son incorrectas
     */
    @PostMapping("/paciente/login")
    public Paciente loginPaciente(@RequestBody LoginPacienteRequest req) {
        return Optional.ofNullable(pacienteDAO.login(req.dni(), req.password()))
                .orElseThrow(() -> credencialesIncorrectas("DNI o contraseña incorrectos."));
    }

    /**
     * Registra un nuevo paciente. Endpoint: {@code POST /api/auth/paciente/registro}.
     *
     * @param req datos del formulario de registro
     * @return el paciente registrado
     * @throws ApiException 400 si faltan datos o el DNI no tiene 8 dígitos; 409 si el DNI o el correo ya existen
     */
    @PostMapping("/paciente/registro")
    @ResponseStatus(HttpStatus.CREATED)
    public Paciente registrar(@RequestBody RegistroPacienteRequest req) {
        Validar.exigir(Validar.conTexto(req.dni(), req.nombres(), req.apellidos(), req.correo(), req.password()),
                "Completa DNI, nombres, apellidos, correo y contraseña.");
        Validar.exigir(Validar.esDni(req.dni()), "El DNI debe tener 8 dígitos.");
        Validar.sinConflicto(pacienteDAO.existe(req.dni(), req.correo()),
                "Ya existe un paciente con ese DNI o correo.");
        return pacienteDAO.registrar(req);
    }

    /**
     * Inicia sesión del personal administrativo. Endpoint: {@code POST /api/auth/admin/login}.
     *
     * @param req usuario y contraseña
     * @return datos del administrador
     * @throws ApiException 401 si las credenciales son incorrectas
     */
    @PostMapping("/admin/login")
    public Administrador loginAdmin(@RequestBody LoginAdminRequest req) {
        return Optional.ofNullable(administradorDAO.login(req.usuario(), req.password()))
                .orElseThrow(() -> credencialesIncorrectas("Usuario o contraseña incorrectos."));
    }

    /**
     * Crea el error 401 de inicio de sesión fallido.
     *
     * @param mensaje texto para el usuario
     * @return excepción con código 401
     */
    private static ApiException credencialesIncorrectas(String mensaje) {
        return new ApiException(HttpStatus.UNAUTHORIZED, mensaje);
    }
}
