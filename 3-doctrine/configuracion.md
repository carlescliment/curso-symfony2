# Configuración

Doctrine necesita conocer algunos datos sobre la base de datos. Dónde está, cómo acceder a ella, qué driver utilizar y el juego de caracteres elegido. Todos estos parámetros se configuran en los archivos `config.yml` y `parameters.yml`.

```config.yml
// app/config/config.yml
# Doctrine Configuration
doctrine:
    dbal:
        driver:   %database_driver%
        host:     %database_host%
        port:     %database_port%
        dbname:   %database_name%
        user:     %database_user%
        password: %database_password%
        charset:  UTF8

    orm:
        auto_generate_proxy_classes: %kernel.debug%
        auto_mapping: true
```

```parameters.yml
// app/config/parameters.yml
parameters:
    database_driver: pdo_mysql
    database_host: 127.0.0.1
    database_port: null
    database_name: symfony
    database_user: root
    database_password: mypassword
```

El driver elegido determinará qué base de datos estamos utilizando. Las opciones son:
- `pdo_mysql`: MySQL
- `pdo_sqlite`: SQLite
- `pdo_pgsql`: PostgreSQL
- `pdo_oci`: Oracle
- `pdo_sqlsrv`: Microsoft SQL Server
- `oci8`: Oracle con la extensión oci8 de PHP.

Una vez establecidos los parámetros de nuestra base de datos, disponemos de algunos comandos de consola para administrar la base de datos.

- Crear la base de datos:
`php app/console doctrine:database:create`

- Eliminar la base de datos:
`php app/console doctrine:database:drop --force`

