# Conceptos teóricos


## El problema del acoplamiento

De entre los tres paradigmas más conocidos, el funcional, el orientado a objetos y el procedural, seguramente sea este último es el más extendido y el que causa más problemas en cuanto a escalabilidad, portabilidad y _testabilidad_ del código. En una aplicación procedural típica, las funciones o procedimientos de más bajo nivel invocan a otras funciones o procedimientos del sistema.

```
function save_account($account_data) {
    // ...
    $success = write_database_row('accounts', $account_data);
    if (!$success) {
        $message = sprintf('An error occurred saving the account for %s', $account_data['name']);
        throw new Exception($message);
    }
}
```

En el código anterior, la función `save_account()` invoca a otro procedimiento `write_database_row`. Como consecuencia se producen dos inconvenientes:

- Es imposible testear la función de manera unitaria, puesto que se invocará el procedimiento que ejecuta la escritura en la base de datos.
- La función `save_account` depende de una función concreta de la aplicación, por lo que para portar este código a otra aplicación necesitaremos arrastrar con él a cada una de sus dependencias y subdependencias.

Aunque este tipo de problemas se asocian a la programación procedural, podemos encontrarlos también en código supuestamente orientado a objetos.

```
class Account {

    public method save() {
        $db = \App::get('DB');
        $success = $db->insertRow('accounts', $this->toArray());
        if (!$success) {
            $message = sprintf('An error occurred saving the account for %s', $this->name);
            throw new \Exception($message);
        }
    }
}
```


## Inversión de control

La [inversión de control](http://en.wikipedia.org/wiki/Inversion_of_control) se basa en el [Principio de Hollywood](http://en.wikipedia.org/wiki/Hollywood_principle), llamado así en referencia al slogan utilizado por los empleadores en Hollywood: _No nos llames, nosotros te llamaremos_.

Es un **principio de diseño** en el cual los componentes de mayor nivel son responsables de proporcionar abstracciones a los de menor nivel. Las instancias concretas de estas abstracciones son reemplazables y necesitan una interfaz común. El flujo por lo tanto se invierte, ahora son las capas superiores las que _controlan_ a las inferiores y no al revés.

Las clases de menor nivel ignoran la implementación del resto del sistema y por lo tanto están desacopladas del mismo. No importa cuál sea el ecosistema en el que se encuentren, funcionarán igualmente siempre que se respeten las interfaces proporcionadas por las abstracciones que se les proporcionan.




## Inyección de dependencias

La [inyección de dependencias](http://en.wikipedia.org/wiki/Dependency_injection) es una **técnica** que facilita la inversión de control, y podemos encontrarla tanto en en el paradigma funcional como en el orientado a objetos. Expuesto en pocas palabras, se basa en pasar instancias como argumentos en lugar de construir estas instancias en el interior del método, realizar invocaciones estáticas o utilizar variables globales. Así, podemos inyectar una dependencia directamente en el método invocado, o bien en el constructor de la clase.


```
function save_account($account_data, $save_callback) {
    // ...
    $success = $save_callback('accounts', $account_data);
    if (!$success) {
        $message = sprintf('An error occurred saving the account for %s', $account_data['name']);
        throw new Exception($message);
    }
}
```

```
class Account {

    public method save(DatabaseInterface $db) {
        $success = $db->insertRow('accounts', $this->toArray());
        if (!$success) {
            $message = sprintf('An error occurred saving the account for %s', $this->name);
            throw new Exception($message);
        }
    }
}
```


## Contenedores de inyección de dependencias

Los contenedores de inyección de dependencias son **herramientas** concretas, a modo de frameworks, que facilitan la inyección automática de instancias en nuestros objetos. Cada implementación utiliza su propia estrategia, ya sea a través de metaprogramación y anotaciones, configuración en ficheros yaml y otros.

Symfony tiene su propio contenedor proporcionado por el [Componente de Inyección de Dependencias](http://symfony.com/doc/current/components/dependency_injection/introduction.html). En Silex se utiliza el contenedor [Pimple](http://pimple.sensiolabs.org/). El contenedor [Twittee](http://twittee.org/) es tan sencillo que su implementación cabe en un tweet.
