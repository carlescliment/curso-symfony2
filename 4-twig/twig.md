# ¿Qué es Twig?

[Twig](http://twig.sensiolabs.org/) es un motor de plantillas para PHP desarrollado por la empresa que creó Symfony, SensioLabs.

Los motores de plantillas proporcionan un lenguaje simplificado para las vistas y permiten un código más elegante. Además, facilitan la manipulación por parte de diseñadores y maquetadores sin conocimientos específicos del lenguaje.

Twig reúne las siguientes características:

- Uso de variables
- Uso de funciones y métodos
- Inclusión de vistas parciales
- Condicionales
- Bucles
- Asignaciones
- Manejo de errores y excepciones
- Herencia


Existen multitud de motores en el mercado para PHP y otros lenguajes. En el artículo de wikipedia [Comparison of web template engines](http://en.wikipedia.org/wiki/Comparison_of_web_template_engines) se describen los más representativos.

Plantilla en PHP:
```php
<ul id="navigation">
    <?php foreach ($navigation as $item): ?>
        <li>
            <a href="<?php echo $item->getHref() ?>">
                <?php echo $item->getCaption() ?>
            </a>
        </li>
    <?php endforeach; ?>
</ul>
```

Plantilla en Twig:
```twig
<ul id="navigation">
    {% for item in navigation %}
        <li><a href="{{ item.href }}">{{ item.caption }}</a></li>
    {% endfor %}
</ul>
```

Plantilla en HAML:
```haml
%ul#navigation
  - navigation.each do |item|
    %li
      %a{ :href => item['href'] }= item['caption']
```
