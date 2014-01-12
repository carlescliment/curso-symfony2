# Ejercicios

**Ejercicio 1:**

Crea una zona segura de administración en tu aplicación que requiera un usuario autenticado. Puede ser una url o la web completa. Utiliza el provider `in_memory` especificando la lista de usuarios y passwords disponibles en tu archivo `security.yml`. Utiliza autenticación básica HTTP.


**Ejercicio 2:**

Modifica tu aplicación para usar un formulario de acceso en lugar de autenticación HTTP.

**Ejercicio 3:**

Modifica tu aplicación para usar usuarios de la base de datos en lugar del provider `in_memory`. Crea algunos usuarios directamente en la base de datos (puedes usar conversores online sha1) para comprobar que funciona.


**Ejercicio 4:**

Crea un formulario de registro en el que los usuarios puedan registrarse en tu aplicación. Los usuarios creados tendrán el rol `ROLE_USER`.

**Ejercicio 5:**

Crea una sección para administrar usuarios. Esta sección solo estará disponible para el rol `ROLE ADMIN` y permitirá modificar los roles de cualquier usuario y marcarlos como inactivos.
