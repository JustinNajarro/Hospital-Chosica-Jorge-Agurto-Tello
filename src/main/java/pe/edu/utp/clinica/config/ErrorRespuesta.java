package pe.edu.utp.clinica.config;

import java.time.LocalDateTime;

import org.springframework.http.HttpStatus;

/**
 * Cuerpo JSON que devuelve la API cuando ocurre un error.
 * <p>
 * Ejemplo:
 * <pre>
 * {
 *   "mensaje": "El medico no existe.",
 *   "estado": 404,
 *   "error": "Not Found",
 *   "ruta": "/api/medicos/99",
 *   "fecha": "2026-10-28T23:30:00"
 * }
 * </pre>
 * El frontend solo usa {@code mensaje}; el resto sirve para depurar.
 *
 * @param mensaje texto que verá el usuario
 * @param estado  código HTTP (400, 404, 409, 500...)
 * @param error   nombre del código HTTP
 * @param ruta    ruta de la petición que falló
 * @param fecha   fecha y hora del error
 * @author Justin Najarro
 * @version 1.0
 */
public record ErrorRespuesta(String mensaje, int estado, String error, String ruta, LocalDateTime fecha) {

    /**
     * Crea la respuesta de error con la fecha y hora actual.
     *
     * @param status  código HTTP
     * @param mensaje texto para el usuario
     * @param ruta    ruta de la petición
     * @return respuesta de error lista para enviarse
     */
    public static ErrorRespuesta de(HttpStatus status, String mensaje, String ruta) {
        return new ErrorRespuesta(mensaje, status.value(), status.getReasonPhrase(), ruta, LocalDateTime.now());
    }
}
