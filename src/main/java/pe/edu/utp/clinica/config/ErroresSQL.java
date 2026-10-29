package pe.edu.utp.clinica.config;

import java.sql.SQLException;
import java.util.Map;

import org.springframework.http.HttpStatus;

/**
 * Utilidad que traduce los errores de MySQL a mensajes entendibles.
 * <p>
 * Errores que maneja:
 * <ul>
 *   <li>1062: registro duplicado (UNIQUE); el mensaje indica qué campo se repite</li>
 *   <li>1451: no se puede borrar porque tiene registros asociados (FK)</li>
 *   <li>1452: el registro relacionado no existe (FK)</li>
 *   <li>1048: falta un campo obligatorio (NOT NULL)</li>
 *   <li>1406: un texto supera el tamaño de la columna</li>
 *   <li>3819: no se cumple una restricción CHECK</li>
 *   <li>1045, 1049 y SQLState 08xxx: no hay conexión con la base de datos</li>
 * </ul>
 *
 * @author Justin Najarro
 * @version 1.1
 */
public final class ErroresSQL {

    /** Registro duplicado (UNIQUE o PRIMARY KEY). */
    private static final int DUPLICADO = 1062;
    /** Columna NOT NULL sin valor. */
    private static final int CAMPO_NULO = 1048;
    /** Texto más largo que la columna. */
    private static final int DATO_MUY_LARGO = 1406;
    /** No se puede borrar: otro registro lo referencia. */
    private static final int TIENE_DEPENDIENTES = 1451;
    /** La clave foránea apunta a un registro que no existe. */
    private static final int REFERENCIA_INEXISTENTE = 1452;
    /** Restricción CHECK no cumplida. */
    private static final int CHECK_FALLIDO = 3819;
    /** Usuario o contraseña de MySQL incorrectos. */
    private static final int ACCESO_DENEGADO = 1045;
    /** La base de datos no existe. */
    private static final int BD_DESCONOCIDA = 1049;

    /**
     * Nombre amigable de cada campo UNIQUE, según el nombre de la columna
     * que aparece en el mensaje de MySQL ({@code for key 'tabla.columna'}).
     */
    private static final Map<String, String> CAMPOS_UNICOS = Map.of(
            "dni", "el DNI",
            "correo", "el correo",
            "codigo_doctor", "el código CMP",
            "nombre_especialidad", "el nombre de la especialidad",
            "numero_sala", "el número de sala",
            "usuario", "el usuario",
            "codigo_confirmacion", "el código de confirmación",
            "uq_medico_horario", "ese horario del médico");

    /**
     * Constructor privado: es una clase de utilidad y no se instancia.
     */
    private ErroresSQL() {
    }

    /**
     * Convierte una {@link SQLException} en la excepción adecuada.
     *
     * @param e      error lanzado por el driver de MySQL
     * @param accion descripción de lo que se intentaba hacer, para el mensaje genérico
     * @return una {@link ApiException} si el error es conocido; si no, una {@link RuntimeException}
     */
    public static RuntimeException traducir(SQLException e, String accion) {
        if (sinConexion(e)) {
            return new ApiException(HttpStatus.SERVICE_UNAVAILABLE,
                    "No se pudo conectar con la base de datos. Revisa que MySQL esté encendido.", e);
        }
        return switch (e.getErrorCode()) {
            case DUPLICADO -> new ApiException(HttpStatus.CONFLICT, mensajeDuplicado(e.getMessage()), e);
            case TIENE_DEPENDIENTES -> new ApiException(HttpStatus.CONFLICT,
                    "No se puede eliminar porque tiene citas u otros registros asociados.", e);
            case REFERENCIA_INEXISTENTE -> new ApiException(HttpStatus.BAD_REQUEST,
                    "Uno de los datos relacionados no existe.", e);
            case CAMPO_NULO -> new ApiException(HttpStatus.BAD_REQUEST,
                    "Falta completar un campo obligatorio.", e);
            case DATO_MUY_LARGO -> new ApiException(HttpStatus.BAD_REQUEST,
                    "Uno de los campos supera la cantidad de caracteres permitida.", e);
            case CHECK_FALLIDO -> new ApiException(HttpStatus.BAD_REQUEST,
                    "La hora de fin debe ser mayor que la hora de inicio.", e);
            default -> new RuntimeException("Error al " + accion + ": " + e.getMessage(), e);
        };
    }

    /**
     * Indica si el error es porque no hay conexión con MySQL: servidor apagado,
     * credenciales incorrectas o base de datos inexistente.
     *
     * @param e error de MySQL
     * @return {@code true} si es un problema de conexión
     */
    private static boolean sinConexion(SQLException e) {
        String estado = e.getSQLState();
        return (estado != null && estado.startsWith("08"))
                || e.getErrorCode() == ACCESO_DENEGADO
                || e.getErrorCode() == BD_DESCONOCIDA;
    }

    /**
     * Arma el mensaje de registro duplicado indicando qué campo se repite.
     * <p>
     * MySQL 8 informa el campo así: {@code Duplicate entry '123' for key 'medico.dni'}.
     *
     * @param detalle mensaje original de MySQL
     * @return mensaje para el usuario
     */
    private static String mensajeDuplicado(String detalle) {
        if (detalle != null) {
            int inicio = detalle.lastIndexOf("for key '");
            if (inicio >= 0) {
                String clave = detalle.substring(inicio + 9).replace("'", "");
                String columna = clave.substring(clave.lastIndexOf('.') + 1);
                String campo = CAMPOS_UNICOS.get(columna);
                if (campo != null) {
                    return "Ya existe un registro con " + campo + " ingresado.";
                }
            }
        }
        return "Ya existe un registro con esos datos (DNI, código CMP, correo o nombre repetido).";
    }
}
