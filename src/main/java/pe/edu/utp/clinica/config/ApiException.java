package pe.edu.utp.clinica.config;

import java.io.Serial;

import org.springframework.http.HttpStatus;

/**
 * Excepción de negocio que lleva el código HTTP que debe devolverse al cliente.
 * <p>
 * Se lanza desde controladores, servicios y DAO cuando una validación falla
 * (por ejemplo, horario ocupado o DNI repetido). {@link ManejadorErrores}
 * la convierte en una respuesta JSON.
 *
 * @author Justin Najarro
 * @version 1.1
 */
public class ApiException extends RuntimeException {

    @Serial
    private static final long serialVersionUID = 1L;

    /**
     * Código HTTP de la respuesta (400, 401, 404, 409...).
     */
    private final HttpStatus status;

    /**
     * Crea la excepción con su código HTTP y el mensaje para el usuario.
     *
     * @param status  código HTTP que se devolverá; si es {@code null} se usa 400
     * @param mensaje texto que verá el usuario en el frontend
     */
    public ApiException(HttpStatus status, String mensaje) {
        super(mensaje);
        this.status = status != null ? status : HttpStatus.BAD_REQUEST;
    }

    /**
     * Crea la excepción guardando el error original que la causó.
     * Útil para no perder el detalle técnico en los logs.
     *
     * @param status  código HTTP que se devolverá; si es {@code null} se usa 400
     * @param mensaje texto que verá el usuario en el frontend
     * @param causa   excepción original
     */
    public ApiException(HttpStatus status, String mensaje, Throwable causa) {
        super(mensaje, causa);
        this.status = status != null ? status : HttpStatus.BAD_REQUEST;
    }

    /**
     * Devuelve el código HTTP asociado al error.
     *
     * @return código HTTP
     */
    public HttpStatus getStatus() {
        return status;
    }
}
