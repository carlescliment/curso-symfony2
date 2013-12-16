# Ejercicios

**Ejercicio 1:**
Añade algunas vistas a tu aplicación. Puedes utilizar tu propio diseño o descargarte un framework CSS como Foundation, Twitter Bootstrap o HTML5 Boilerplate, entre otros.


**Ejercicio 2:**
En el footer queremos mostrar nuestra dirección e-mail de contacto, pero para facilitar que la web sea utilizada por otros programadores queremos que la dirección sea configurable.

Añade un parámetro `contact_email` a la configuración de tu aplicación Symfony. Averigua cómo añadir ese parámetro a las variables globales de Twig para que cualquier plantilla pueda acceder a su valor. Al final, tu plantilla debería contener un fragmento similar al siguiente:

```
<footer>
	Contacto: {{ contact_email }}
</footer>
```
