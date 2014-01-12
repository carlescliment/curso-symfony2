# Usuarios y roles

La mayoría de las aplicaciones web utilizan mecanismos más flexibles para gestionar usuarios que el almacenamiento `in_memory` que hemos visto en el ejemplo del punto anterior. En este capítulo veremos cómo crear una entidad en la base de datos que representará a los usuarios de nuestro sistema.

### Crear la entidad User

En primer lugar generaremos un nuevo bundle encargado de gestionar usuarios. Por consistencia con los ejemplos mostrados hasta ahora lo llamaremos MyUserBundle.

```
app/console generate:bundle --namespace=My/UserBundle
```

Posteriormente crearemos la entidad User.

```
app/console doctrine:generate:entity --entity=MyUserBundle:User --fields="email:string(255) username:string(255) password:string(64) salt:string(64)" --format=yml
```

Como resultado obtendremos la siguiente entidad:

```php
// src/My/UserBundle/Entity/User.php

namespace My\UserBundle\Entity;

use Doctrine\ORM\Mapping as ORM;

/**
 * User
 */
class User
{
    /**
     * @var integer
     */
    private $id;

    /**
     * @var string
     */
    private $email;

    /**
     * @var string
     */
    private $username;

    /**
     * @var string
     */
    private $password;

    /**
     * @var string
     */
    private $salt;


    /**
     * Get id
     *
     * @return integer 
     */
    public function getId()
    {
        return $this->id;
    }

    /**
     * Set email
     *
     * @param string $email
     * @return User
     */
    public function setEmail($email)
    {
        $this->email = $email;
    
        return $this;
    }

    /**
     * Get email
     *
     * @return string 
     */
    public function getEmail()
    {
        return $this->email;
    }

    /**
     * Set username
     *
     * @param string $username
     * @return User
     */
    public function setUsername($username)
    {
        $this->username = $username;
    
        return $this;
    }

    /**
     * Get username
     *
     * @return string 
     */
    public function getUsername()
    {
        return $this->username;
    }

    /**
     * Set password
     *
     * @param string $password
     * @return User
     */
    public function setPassword($password)
    {
        $this->password = $password;
    
        return $this;
    }

    /**
     * Get password
     *
     * @return string 
     */
    public function getPassword()
    {
        return $this->password;
    }

    /**
     * Set salt
     *
     * @param string $salt
     * @return User
     */
    public function setSalt($salt)
    {
        $this->salt = $salt;
    
        return $this;
    }

    /**
     * Get salt
     *
     * @return string 
     */
    public function getSalt()
    {
        return $this->salt;
    }
}
```

Y un fichero `yml` del ORM Doctrine.

```yml
#src/My/UserBundle/Resources/config/doctrine/User.orm.yml
My\UserBundle\Entity\User:
    type: entity
    table: null
    fields:
        id:
            type: integer
            id: true
            generator:
                strategy: AUTO
        email:
            type: string
            length: '255'
        username:
            type: string
            length: '255'
        password:
            type: string
            length: '64'
        salt:
            type: string
            length: '64'
    lifecycleCallbacks: {  }
```

Modificaremos el email para que sea único:

```yml
#src/My/UserBundle/Resources/config/doctrine/User.orm.yml
My\UserBundle\Entity\User:
    type: entity
    table: users
    fields:
    	# ...
        email:
            type: string
            length: '255'
            unique: true
        # ...
```


Y actualizamos la base de datos, creando la tabla correspondiente:

```
$ app/console doctrine:schema:update --force

Updating database schema...
Database schema updated successfully! "1" queries were executed
```


### Implementar la interfaz UserInterface

Symfony necesita que nuestra clase usuario implemente ciertos métodos, que están definidos en la interfaz `UserInterface`. Estos métodos son:

- `getRoles()`
- `getPassword()`
- `getSalt()`
- `getUsername()`
- `eraseCredentials()`

Haremos que nuestra clase implemente la interfaz y añadiremos los métodos pendientes.


```php
// src/My/UserBundle/Entity/User.php

namespace My\UserBundle\Entity;

use Doctrine\ORM\Mapping as ORM;
use Symfony\Component\Security\Core\User\UserInterface;

/**
 * User
 */
class User implements UserInterface
{
	// ...

	public function getRoles()
	{
		return array('ROLE_USER');
	}


	public function eraseCredentials()
	{
	}

}
```


### Configurar el user provider

El último paso consiste en configurar el componente de seguridad de Symfony para que acceda a la base de datos durante la autenticación de los usuarios:

```
#app/config/security.yml
security:
    encoders:
        My\UserBundle\Entity\User:
            algorithm:        sha1
            encode_as_base64: false
            iterations:       1

    role_hierarchy:
        ROLE_ADMIN:       ROLE_USER
        ROLE_SUPER_ADMIN: [ROLE_USER, ROLE_ADMIN, ROLE_ALLOWED_TO_SWITCH]

    providers:
        users:
            entity: { class: MyUserBundle:User, property: username }

    firewalls:
        secured_area:
            pattern:    ^/
            anonymous: ~
            form_login:
                login_path:  login
                check_path:  login_check
            logout: ~

    access_control:
        - { path: ^/secured, roles: ROLE_ADMIN }
```


Insertaremos un usuario de prueba en la base de datos para comprobar su funcionamiento:

```
INSERT INTO users (username, email, password, salt) VALUES ('curso', 'curso@email.es', '5bc4c37a302f3a672c69516df20c6ba644e68356', '');
```

Si accedemos al formulario de login, podemos introducir el usuario `curso` y la contraseña `curso` que corresponden al usuario insertado.

### Roles

En el ejemplo anterior hemos implementado un método getRoles que siempre devuelve el mismo array con el rol `ROLE_USER`. Modificaremos nuestra entidad `User` y el archivo de mapeo del ORM para permitir una gestión de roles más potente.



```php
// src/My/UserBundle/Entity/User.php

/**
 * User
 */
class User implements UserInterface
{

	// ...

    /**
     * @var string
     */
    private $roles = '';


    // ...

    public function getRoles()
    {
        return explode(' ', $this->roles);
    }


}
```

```yml
# src/My/UserBundle/Resources/config/doctrine/User.orm.yml
My\UserBundle\Entity\User:
    type: entity
    table: users
    fields:
    	# ...
        roles:
            type: string
            length: '255'
    lifecycleCallbacks: {  }
```


Actualizaremos la base de datos.

```
app/console doctrine:schema:update --force
```

Ahora ya podemos añadir roles dinámicamente y gestionar el control de acceso a zonas de administración.


Con estas bases podemos implementar sistemas de autenticación tan complejos como necesitemos. Para una mayor información sobre el Componente de Seguridad de Symfony 2, consultad la [documentación oficial](http://symfony.com/doc/current/book/security.html).