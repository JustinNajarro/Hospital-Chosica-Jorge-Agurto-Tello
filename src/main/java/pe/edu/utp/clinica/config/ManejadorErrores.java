package pe.edu.utp.clinica.config;

import java.util.Map;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.servlet.resource.NoResourceFoundException;

/** Devuelve los errores como JSON: { "mensaje": "..." } */
@RestControllerAdvice
public class ManejadorErrores {

    @ExceptionHandler(ApiException.class)
    public ResponseEntity<Map<String, String>> api(ApiException e) {
        return ResponseEntity.status(e.getStatus()).body(Map.of("mensaje", e.getMessage()));
    }

    /** Peticiones a archivos que no existen (por ejemplo favicon.ico) */
    @ExceptionHandler(NoResourceFoundException.class)
    public ResponseEntity<Void> sinRecurso() {
        return ResponseEntity.notFound().build();
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<Map<String, String>> general(Exception e) {
        e.printStackTrace();
        String msg = e.getMessage() != null ? e.getMessage() : "Error interno del servidor";
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(Map.of("mensaje", msg));
    }
}
