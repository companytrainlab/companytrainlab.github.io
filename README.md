# TrainLab · Web de la marca

La web pública de TrainLab, servida por GitHub Pages en la URL raíz:
**https://companytrainlab.github.io/**

## Qué es

Una sola página larga que cuenta el ecosistema completo (Fitness, Velocity,
Control, Force y Signal), la ciencia que hay detrás de cada número, los
precios de lanzamiento y una lista de espera para la beta. Más la política
de privacidad en `privacidad.html`.

## Cómo está hecha

- **Estática a propósito:** HTML, CSS y JS a mano, sin frameworks ni
  dependencias externas. Carga en un instante y no hay nada que compilar.
- **La identidad del manual:** paleta de `EMPRESA/producto/kit/tokens.css`,
  el símbolo siempre sobre azul noche, el wordmark con Train en gris y Lab
  en azul pulso, y el dato protagonista en grande como firma visual.
- **Modo claro y noche automáticos**, siguiendo el ajuste del sistema,
  igual que las apps de la familia.
- **Bilingüe** español e inglés con un conmutador; recuerda la elección y
  arranca en el idioma del navegador.
- **Sin cookies ni analítica ni rastreadores.**

## La lista de espera

El formulario llama a la Edge Function `lista-espera` de Supabase
(repositorio de Fitness, `trainlab-web/supabase/functions/lista-espera/`),
que guarda el alta en la tabla `lista_espera` (migración
`19_lista_espera.sql`). RLS cerrado: solo escribe la función con la
service role. El campo oculto `telefono` es un señuelo antirrobots.

## Cómo se publica

Con un push a `main`: GitHub Pages sirve el contenido tal cual
(`.nojekyll` evita el procesado de Jekyll). El landing NFC de las cajas
vive aparte, en el repositorio `caja`, bajo `/caja/`.
