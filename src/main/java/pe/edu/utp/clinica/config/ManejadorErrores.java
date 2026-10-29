package pe.edu.utp.clinica.config;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.web.HttpRequestMethodNotSupportedException;
import org.springframework.web.bind.MissingServletRequestParameterException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.method.annotation.MethodArgumentTypeMismatchException;
import org.springframework.web.servlet.resource.NoResourceFoundException;

import jakarta.servlet.http.HttpServletRequest;

/**
 * Manejador global de errores de la API.
 * <p>
 * Captura las excepciones que salen de los controladores y las devuelve
 * en formato JSON con {@link ErrorRespuesta}. Los errores de negocio
 * (4xx) solo se registran como aviso; los inesperados (5xx) se registran
 * completos en el log, pero al usuario se le muestra un mensaje genérico
 * para no exponer detalles internos del servidor.
 *
 * @author Justin Najarro
 * @version 1.1
 */
@RestControllerAdvice
public class ManejadorErrores {

    /** Logger de la clase (reemplaza a {@code printStackTrace}). */
    private static final Logger LOG = LoggerFactory.getLogger(ManejadorErrores.class);

    /** Mensaje que se muestra al usuario cuando ocurre un error no previsto. */
    private static final String MENSAJE_GENERICO = "Ocurrió un error inesperado. Intenta nuevamente.";

    /**
     * Maneja los errores de negocio lanzados por controladores, servicios y DAO.
     *
     * @param e       excepción con el código HTTP y el mensaje
     * @param request petición que falló
     * @return respuesta con el código de la excepción y el mensaje
     */
    @ExceptionHandler(ApiException.class)
    public ResponseEntity<ErrorRespuesta> api(ApiException e, HttpServletRequest request) {
        if (e.getStatus().is5xxServerError()) {
            LOG.error("{} {} -> {}", request.getMethod(), request.getRequestURI(), e.getMessage(), e);
        } else {
            LOG.warn("{} {} -> {} {}", request.getMethod(), request.getRequestURI(), e.getStatus().value(), e.getMessage());
        }
        return responder(e.getStatus(), e.getMessage(), request);
    }

    /**
     * Cuerpo JSON mal escrito o vacío (por ejemplo, falta una coma o una fecha no válida).
     *
     * @param e       excepción de Spring al leer el JSON
     * @param request petición que falló
     * @return respuesta 400
     */
    @ExceptionHandler(HttpMessageNotReadableException.class)
    public ResponseEntity<ErrorRespuesta> jsonInvalido(HttpMessageNotReadableException e, HttpServletRequest request) {
        LOG.warn("{} {} -> JSON invalido: {}", request.getMethod(), request.getRequestURI(), e.getMessage());
        return responder(HttpStatus.BAD_REQUEST, "Los datos enviados no tienen el formato correcto.", request);
    }

    /**
     * Parámetro de la URL con un tipo incorrecto (por ejemplo, {@code /api/medicos/abc}
     * o una fecha con formato distinto a AAAA-MM-DD).
     *
     * @param e       excepción de conversión de tipo
     * @param request petición que falló
     * @return respuesta 400 indicando el parámetro
     */
    @ExceptionHandler(MethodArgumentTypeMismatchException.class)
    public ResponseEntity<ErrorRespuesta> tipoInvalido(MethodArgumentTypeMismatchException e, HttpServletRequest request) {
        LOG.warn("{} {} -> parametro invalido: {}", request.getMethod(), request.getRequestURI(), e.getName());
        return responder(HttpStatus.BAD_REQUEST, "El valor de '" + e.getName() + "' no es válido.", request);
    }

    /**
     * Falta un parámetro obligatorio en la URL (por ejemplo, {@code ?fecha=}).
     *
     * @param e       excepción de parámetro faltante
     * @param request petición que falló
     * @return respuesta 400 indicando el parámetro
     */
    @ExceptionHandler(MissingServletRequestParameterException.class)
    public ResponseEntity<ErrorRespuesta> parametroFaltante(MissingServletRequestParameterException e,
                                                            HttpServletRequest request) {
        LOG.warn("{} {} -> falta parametro: {}", request.getMethod(), request.getRequestURI(), e.getParameterName());
        return responder(HttpStatus.BAD_REQUEST, "Falta el parámetro '" + e.getParameterName() + "'.", request);
    }

    /**
     * Método HTTP no permitido en la ruta (por ejemplo, un GET donde solo hay POST).
     *
     * @param e       excepción de método no soportado
     * @param request petición que falló
     * @return respuesta 405
     */
    @ExceptionHandler(HttpRequestMethodNotSupportedException.class)
    public ResponseEntity<ErrorRespuesta> metodoNoPermitido(HttpRequestMethodNotSupportedException e,
                                                            HttpServletRequest request) {
        LOG.warn("{} {} -> metodo no permitido", request.getMethod(), request.getRequestURI());
        return responder(HttpStatus.METHOD_NOT_ALLOWED,
                "El método " + e.getMethod() + " no está permitido en esta ruta.", request);
    }

    /**
     * Responde 404 a peticiones de archivos que no existen, como {@code favicon.ico},
     * sin llenar la consola de errores.
     *
     * @return respuesta 404 sin cuerpo
     */
    @ExceptionHandler(NoResourceFoundException.class)
    public ResponseEntity<Void> sinRecurso() {
        return ResponseEntity.notFound().build();
    }

    /**
     * Maneja cualquier error no previsto. El detalle completo queda en el log
     * y al usuario se le devuelve un mensaje genérico.
     *
     * @param e       excepción inesperada
     * @param request petición que falló
     * @return respuesta 500
     */
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorRespuesta> general(Exception e, HttpServletRequest request) {
        LOG.error("{} {} -> error inesperado", request.getMethod(), request.getRequestURI(), e);
        return responder(HttpStatus.INTERNAL_SERVER_ERROR, MENSAJE_GENERICO, request);
    }

    /**
     * Arma la respuesta HTTP con el cuerpo de error.
     *
     * @param status  código HTTP
     * @param mensaje texto para el usuario
     * @param request petición que falló
     * @return respuesta lista para enviarse
     */
    private ResponseEntity<ErrorRespuesta> responder(HttpStatus status, String mensaje, HttpServletRequest request) {
        return ResponseEntity.status(status).body(ErrorRespuesta.de(status, mensaje, request.getRequestURI()));
    }
}
