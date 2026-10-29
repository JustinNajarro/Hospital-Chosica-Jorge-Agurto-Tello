package pe.edu.utp.clinica.controller;

import java.util.regex.Pattern;

import org.springframework.http.HttpStatus;

import pe.edu.utp.clinica.config.ApiException;

/**
 * Validaciones comunes de los controladores.
 * <p>
 * Junta en un solo lugar las comprobaciones que antes estaban repetidas
 * en varios controladores (texto vacío, formato de DNI, registro no encontrado,
 * conflictos), para que cada endpoint se lea en pocas líneas.
 *
 * @author Justin Najarro
 * @version 1.0
 */
final class Validar {

    /** Formato del DNI peruano: 8 dígitos. Se compila una sola vez. */
    private static final Pattern DNI = Pattern.compile("\\d{8}");

    /**
     * Constructor privado: clase de utilidad, no se instancia.
     */
    private Validar() {
    }

    /**
     * Lanza un error 400 si la condición no se cumple.
     *
     * @param condicion condición que deben cumplir los datos
     * @param mensaje   texto para el usuario si no se cumple
     * @throws ApiException 400 si la condición es falsa
     */
    static void exigir(boolean condicion, String mensaje) {
        if (!condicion) {
            throw new ApiException(HttpStatus.BAD_REQUEST, mensaje);
        }
    }

    /**
     * Lanza un error 404 si la operación no encontró el registro.
     *
     * @param encontrado resultado de la operación en el DAO
     * @param mensaje    texto para el usuario si no existe
     * @throws ApiException 404 si {@code encontrado} es falso
     */
    static void existe(boolean encontrado, String mensaje) {
        if (!encontrado) {
            throw new ApiException(HttpStatus.NOT_FOUND, mensaje);
        }
    }

    /**
     * Lanza un error 409 si hay un conflicto con datos ya registrados.
     *
     * @param hayConflicto {@code true} si el dato choca con otro existente
     * @param mensaje      texto para el usuario
     * @throws ApiException 409 si hay conflicto
     */
    static void sinConflicto(boolean hayConflicto, String mensaje) {
        if (hayConflicto) {
            throw new ApiException(HttpStatus.CONFLICT, mensaje);
        }
    }

    /**
     * Indica si todos los textos tienen contenido (no nulos ni en blanco).
     *
     * @param textos textos a revisar
     * @return {@code true} si ninguno está vacío
     */
    static boolean conTexto(String... textos) {
        for (String t : textos) {
            if (t == null || t.isBlank()) {
                return false;
            }
        }
        return true;
    }

    /**
     * Indica si el texto es un DNI válido de 8 dígitos.
     *
     * @param dni texto a revisar
     * @return {@code true} si tiene el formato correcto
     */
    static boolean esDni(String dni) {
        return dni != null && DNI.matcher(dni).matches();
    }

    /**
     * Quita espacios y pasa a mayúsculas; devuelve cadena vacía si es nulo.
     * Se usa para comparar estados y días de la semana.
     *
     * @param texto texto a normalizar
     * @return texto normalizado
     */
    static String normalizar(String texto) {
        return texto == null ? "" : texto.trim().toUpperCase();
    }
}
