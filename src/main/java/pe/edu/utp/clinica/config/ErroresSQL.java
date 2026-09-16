package pe.edu.utp.clinica.config;

import java.sql.SQLException;

import org.springframework.http.HttpStatus;

/** Convierte los errores de MySQL en mensajes entendibles para el usuario. */
public final class ErroresSQL {

    private ErroresSQL() {
    }

    public static RuntimeException traducir(SQLException e, String accion) {
        return switch (e.getErrorCode()) {
            case 1062 -> new ApiException(HttpStatus.CONFLICT,
                    "Ya existe un registro con esos datos (DNI, código CMP, correo o nombre repetido).");
            case 1451 -> new ApiException(HttpStatus.CONFLICT,
                    "No se puede eliminar porque tiene citas u otros registros asociados.");
            case 1452 -> new ApiException(HttpStatus.BAD_REQUEST,
                    "Uno de los datos relacionados no existe.");
            case 3819 -> new ApiException(HttpStatus.BAD_REQUEST,
                    "La hora de fin debe ser mayor que la hora de inicio.");
            default -> new RuntimeException("Error al " + accion + ": " + e.getMessage(), e);
        };
    }
}
