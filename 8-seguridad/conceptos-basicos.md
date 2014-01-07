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



### Autenticación

Autenticación básica HTTP

Autenticación con un formulario


### Autorización

Matching options: 
 path
 ip
 host
 methods
