# Conceptos básicos

Symfony 2 dispone de su propio [componente de seguridad](http://symfony.com/doc/current/components/security/introduction.html) que puede ser utilizado de forma independiente en cualquier aplicación PHP.

La seguridad en Symfony 2 se realiza en dos pasos: la *autenticación*, donde el sistema reconoce quién realiza la petición, y la *autorización*, donde se aplicarán las reglas que decidirán si el usuario puede o no acceder al recurso especificado.


## Autenticación y autorización

### Firewalls (autenticación)

Los firewalls son reglas que se aplican a las rutas de la aplicación y definen áreas seguras. 

```
# app/config/security.yml
security:
    firewalls:
        secured_area:
            pattern:    ^/
            anonymous: ~
            http_basic:
                realm: "Mis recetas"

    # ...
```

El firewall del ejemplo anterior de security.yml se está aplicando a toda la web, por lo que cualquier petición será gestinada por dicho firewall. Existen diversas formas de autenticar a un usuario. La más sencilla de ellas es la autenticación básica del protocolo HTTP (usuario/contraseña), que es la utilizada en el firewall del ejemplo


### Control de acceso (autorización)

Cuando se accede a una ruta bajo un firewall, se aplican las reglas de control de acceso que se hayan definido en el mismo.

```
# app/config/security.yml
security:
    firewalls:
        secured_area:
            pattern:    ^/
            anonymous: ~
            http_basic:
                realm: "Mis recetas"

    access_control:
        - { path: ^/secured, roles: ROLE_ADMIN }

    # ...
```

En el anterior ejemplo hemos definido una zona segura en `/secured`. Cualquier ruta que siga el patrón `/secured/*` se puede acceder solo por aquellos usuarios con el rol `ROLE_ADMIN`. Pero ¿dónde se definen los usuarios?.


### Usuarios

El componente de seguridad de Symfony utiliza *user providers* para obtener los usuarios del sistema. El user provider más sencillo se denomina `in_memory` y permite especificar usuarios que se almacenan directamente en memoria.

```
# app/config/security.yml
security:
    firewalls:
        secured_area:
            pattern:    ^/
            anonymous: ~
            http_basic:
                realm: "Mis recetas"

    access_control:
        - { path: ^/secured, roles: ROLE_ADMIN }

	providers:
        in_memory:
            memory:
                users:
                    user:  { password: user, roles: 'ROLE_USER' }
                    admin: { password: admin, roles: 'ROLE_ADMIN' }

    encoders:
        Symfony\Component\Security\Core\User\User: plaintext
```

En el ejemplo anterior se definen dos usuarios; por una parte el usuario `user` identificado por el password `user`, que tiene el rol `ROLE_USER`,  y por la otra el usuario `admin` identificado por `admin` con el rol `ROLE_ADMIN`.

La última linea bajo `encoders` define la clase a utilizar para nuestros usuarios y la forma en que se codifica su password. Está definida como `plaintext`, por lo que no hay ninguna codificación.

Con esta configuración ya tendremos definida una zona segura. Accediendo a ella veremos que el navegador solicita autenticación mediante la comentada autenticación básica HTTP.


### Autenticación con un formulario

Aunque la autenticación HTTP puede bastar en algunos casos, lo habitual en los sitios web es utilizar un formulario de login.

Para utilizar un formulario, en primer lugar necesitaremos establecer dos rutas; `login` y `check`. La primera se encargará del renderizado del formulario y la segunda de la validación del mismo. Sustituiremos la anterior clave `http_basic` por una nueva `form_login` tal y como se muestra en el ejemplo siguiente.

```
# app/config/security.yml
security:
    firewalls:
        secured_area:
            pattern:    ^/
            anonymous: ~
            form_login:
                login_path:  login
                check_path:  login_check
```


Una vez establecidas estas rutas en el firewall, las añadiremos a nuestro router. Es importante que los nombres de las rutas (`login` y `login_check`) coincidan con los valores introducidos en `security.yml`.

```
# app/config/routing.yml
login:
    path:   /login
    defaults:  { _controller: MyRecipesBundle:Security:login }
login_check:
    path:   /login_check 
```

El siguiente paso es completar el controlador `MyRecipesBundle:Security:login`.

```
// src/My/RecipesBundle/Controller/SecurityController.php;
namespace My\RecipesBundle\Controller;

use Sensio\Bundle\FrameworkExtraBundle\Configuration\Template;
use Symfony\Bundle\FrameworkBundle\Controller\Controller;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\Security\Core\SecurityContext;

class SecurityController extends Controller
{
    /**
     * @Template()
     */
    public function loginAction(Request $request)
    {
        $session = $request->getSession();

        // get the login error if there is one
        if ($request->attributes->has(SecurityContext::AUTHENTICATION_ERROR)) {
            $error = $request->attributes->get(
                SecurityContext::AUTHENTICATION_ERROR
            );
        } else {
            $error = $session->get(SecurityContext::AUTHENTICATION_ERROR);
            $session->remove(SecurityContext::AUTHENTICATION_ERROR);
        }

        return array(
            // last username entered by the user
            'last_username' => $session->get(SecurityContext::LAST_USERNAME),
            'error'         => $error,
        );
    }
}
```

Y finalmente crearemos la plantilla correspondiente.

```twig
{# src/My/RecipesBundle/Resources/views/Security/login.html.twig #}
{% if error %}
    <div>{{ error.message }}</div>
{% endif %}

<form action="{{ path('login_check') }}" method="post">
    <label for="username">Username:</label>
    <input type="text" id="username" name="_username" value="{{ last_username }}" />

    <label for="password">Password:</label>
    <input type="password" id="password" name="_password" />

    <button type="submit">login</button>
</form>
```


¡Y ya está! Por supuesto podemos personalizar nuestro formulario tanto como queramos, siempre que se mantengan los nombres de los input fields. Tras estos cambios, cuando intentemos acceder a una ruta segura, el framework redirigirá la petición al formulario de entrada.


### Cierre de sesión

Los cambios necesarios para ofrecer logout a los usuarios del sistema son bastante más sencillos, dado que el componente de seguridad ya tiene un comportamiento por defecto que se encarga de ello, basta con activarlo añadiedo la siguiente linea al archivo `security.yml`.

```
# app/config/security.yml
security:
    firewalls:
        secured_area:
            # ...
            logout: ~
    # ...
```

De esta manera, cualquier usuario autenticado que acceda a la ruta `/logout` dará por cerrada su sesión y será redirigido a la ruta índice `/`.

Para personalizar las rutas de salida y redirección posterior podemos añadir los parámetros de configuración `path` y `target` inmediatamente bajo `logout`.

```
# app/config/security.yml
security:
    firewalls:
        secured_area:
            # ...
            logout:
                path:   /quit
                target: /recipes
    # ...
```


En ambos casos será necesario que añadamos esta ruta de salida a nuestro archivo `routing.yml`.

```
# app/config/routing.yml
logout:
    path:   /logout
```
