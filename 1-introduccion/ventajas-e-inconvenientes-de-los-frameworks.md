# La evolución de PHP y los frameworks MVC

Aunque los frameworks de desarrollo suponen por lo general una gran ventaja en la mayoría de proyectos, también tienen algunos inconvenientes.

## Ventajas

### Productividad
Los frameworks proporcionan soluciones prefabricadas para los problemas más comunes. Atención de peticiones, formularios e interacción con base de datos son ejemplos de soluciones que casi todos los frameworks ofrecen. Esto permite a los desarrolladores centrarse en las necesidades de negocio sin tener que resolver los detalles técnicos de más bajo nivel.

### Organización
Un framework, normalmente, ofrece una estructura clara y organizada a varios niveles, como la estructura de directorios y la separación por capas. En consecuencia es más fácil saber dónde encontrar cualquier recurso cuando sea necesario cambiarlo.

### Convención
Relacionado con el punto anterior, alrededor de un framework se construye una _manera de resolver las cosas_, un estilo. Empezando por los coding styles hasta patrones de diseño concretos, los desarrolladores pueden y deben acogerse a esas convenciones. Así, cualquier desarrollador habituado al framework pueda integrarse en cualquier proyecto con mayor facilidad.

### Documentación
Todos los frameworks disponen de un sitio web con documentación más o menos completa, bloggers que comparten sus soluciones, vídeos, charlas y conferencias.

### Seguridad
Los problemas de seguridad suelen estar resueltos por el mismo framework. En el caso de descubrir amenazas que puedan comprometer la seguridad, es la misma comunidad la que los soluciona de manera más rápida y eficaz que si lo hicieras tú o tu departamento.

### Rendimiento
Cuantos más desarrolladores utilicen el framework, más ojos hay pendientes del rendimiento que les ofrece. Por ello, los frameworks suelen ofrecer implementaciones más rápidas de las que pueda implementar un desarrollador individual.

### Comunidad
Muchas de las ventajas anteriores serían imposibles sin la existencia de las comunidades. Éstas proveen, además, multitud de módulos, plugins, bundles o gemas de manera libre y gratuíta. Antes de enfrentarse a cualquier problema conviene realizar una búsqueda en internet. Seguramente alguien ya lo haya resuelto.

Por otra parte, las comunidades suelen organizarse en grupos locales y reunirse en eventos nacionales e internacionales. ¡Son una buena oportunidad de conocer gente interesante y apasionada!


## Desventajas

### Rendimiento (recursos de proceso y memoria)
Los frameworks consumen, en general, más recursos que una aplicación ad-hoc orientada al rendimiento. En aplicaciones muy exigentes, un framework puede resultar poco apropiado.

### Curva inicial de aprendizaje
Cada framework tiene su ecosistema de componentes que el desarrollador debe aprender, no basta con conocer el lenguaje sobre el que está escrito. Por ello, los frameworks son islas de conocimiento.

### Convención
Aunque normalmente las convenciones constituyen una ventaja, en ocasiones también pueden resultar un impedimento. Algunas veces, ante problemas muy concretos, el establecimiento de convenios obliga a los desarrolladores a _esquivar_ al framework. Algunos desarrolladores sienten también cierta falta de libertad y creatividad al utilizar frameworks muy orientados a los convenios, como Ruby on Rails.

### Sensación de bala de plata
A medida que un desarrollador conoce el framework, se introduce en una _zona de confort_. A la larga es posible que el desarrollador piense que su framework es la mejor solución para todo, sin estudiar otras alternativas. Por ello es muy recomendable actualizarse constantemente y conocer otros frameworks y plataformas que enriquezcan nuestra _caja de herramientas_.

### ¿De verdad necesito un framework?
Ante el impulso inicial de los grandes frameworks monolíticos han surgido alternativas que proporcionan capas más finas de funcionalidad y ofrecen una mayor flexibilidad al desarrollador; son los llamados _microframeworks_. Entre ellos tenemos Sinatra (Ruby), Flask (Python) o Silex (PHP).

Gracias a los gestores de componentes, como Composer en PHP, es sencillo construirse aplicaciones a medida. Por ejemplo, una aplicación PHP podría tomar el componente de inyección de dependencias Pimple, el Event Dispatcher de Symfony 2 y cualquier otro componente que se proporcione aislado. Esta solución puede ser más apropiada para necesidades de negocio complejas o desarrolladores exigentes.

Como ejemplo de esta segregación en paquetes, es interesante estudiar el caso de [The Aurora Project](http://auraphp.com/).


Otros recursos sobre ventajas y desventajas de los frameworks:
- [Software Framework Advantages and Disadvantages](http://nagbhushan.wordpress.com/2010/10/03/framework-advantages-and-disadvantages/)
- [Pros and cons of using frameworks](http://www.1stwebdesigner.com/design/pros-cons-frameworks/)
