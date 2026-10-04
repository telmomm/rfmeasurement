# IEEE TIM Paper — `rfmeasurement`

## 1. Objetivo del estudio

### Objetivo principal

Evaluar experimentalmente si un framework software orientado a mediciones, como `rfmeasurement`, puede proporcionar una capa reproducible y trazable para el análisis de medidas RF, integrando:

* representación estructurada de medidas;
* procedencia (*measurement provenance*);
* evaluación de calidad;
* modelado y propagación de incertidumbre;
* validación;
* reproducibilidad computacional;
* integración con herramientas convencionales de análisis RF.

El objetivo **no** es demostrar simplemente que `rfmeasurement` procesa correctamente datos de un VNA, sino evaluar si su arquitectura permite transformar un resultado RF convencional en un **resultado metrológicamente contextualizado, trazable y reproducible**.

---

# 2. Posicionamiento científico

## Hipótesis de trabajo

Los workflows convencionales de análisis RF suelen separar:

1. adquisición;
2. calibración;
3. almacenamiento de datos;
4. análisis;
5. estimación de incertidumbre;
6. documentación del experimento.

Esto puede dificultar la reconstrucción completa de cómo se obtuvo un resultado y la comparación de resultados obtenidos bajo diferentes condiciones experimentales.

`rfmeasurement` propone integrar estos elementos dentro de una representación software explícita de la medición.

### Hipótesis principal

> An uncertainty-aware and provenance-preserving software layer can improve the traceability, reproducibility, and quality assessment of RF measurement workflows without replacing established RF analysis tools.

---

# 3. Encaje con IEEE Transactions on Instrumentation and Measurement

## Enfoque recomendado

El artículo debe posicionarse principalmente como un trabajo de:

* instrumentation;
* measurement methodology;
* metrological characterization;
* uncertainty analysis;
* measurement quality;
* reproducibility;
* software-assisted measurement.

El software es el **medio de implementación**, no la contribución científica principal.

### Evitar

No presentar el trabajo como:

> "`rfmeasurement`: a Python package for RF measurements"

ni como una simple descripción de arquitectura software.

### Presentar como

> A measurement-aware software methodology for integrating uncertainty, quality assessment, provenance, and reproducibility into RF measurement workflows.

---

# 4. Relación con trabajos científicos existentes

`rfmeasurement` ya se está utilizando en dos líneas experimentales independientes.

## 4.1. Trabajo 1 — actualmente en revisión

**Experimental Error Modeling and Post-Processing Correction of NanoVNA Measurements Using Low-Cost Calibration Standards**

Estado:

> En revisión.

Este trabajo demuestra el uso de `rfmeasurement` en:

* caracterización experimental del error;
* medidas con NanoVNA;
* estándares de calibración de bajo coste;
* modelado del error;
* corrección post-procesado;
* análisis cuantitativo de las medidas.

### Función dentro del ecosistema de investigación

Este artículo constituye evidencia de que `rfmeasurement` puede utilizarse en un workflow experimental real de caracterización y corrección de medidas.

Sin embargo, **no debe ser simplemente reutilizado como experimento principal del paper de TIM**.

Puede utilizarse como:

* evidencia previa;
* caso de uso publicado/en revisión;
* fuente de datasets o metodología;
* validación externa del framework;
* referencia a aplicaciones previas.

---

# 5. Trabajo 2 — actualmente en redacción

**Metrological characterization of a low-cost vector network analyzer for open-ended coaxial probe dielectric spectroscopy of biological materials**

Estado:

> En redacción.

Este trabajo extiende el uso del framework hacia:

* caracterización metrológica;
* VNA de bajo coste;
* sondas coaxiales abiertas;
* espectroscopia dieléctrica;
* materiales biológicos;
* evaluación de incertidumbre;
* aplicación experimental multidominio.

### Función dentro del ecosistema

Este trabajo es especialmente importante para demostrar que `rfmeasurement` no está limitado a un único experimento de NanoVNA o a una única aplicación de S-parameters.

Puede servir para demostrar:

> **generality across measurement scenarios.**

El artículo de TIM debería utilizar ambos trabajos como antecedentes de aplicación, pero aportar una contribución diferente y de nivel superior.

---

# 6. Diferencia respecto a los dos papers de aplicación

El paper de TIM **no debe ser un tercer paper que simplemente utilice `rfmeasurement`**.

La jerarquía científica debería ser:

```text
                         rfmeasurement
                               │
             ┌─────────────────┼─────────────────┐
             │                 │                 │
             ▼                 ▼                 ▼
       Application 1      Application 2       TIM study
       NanoVNA error      OCP dielectric      Framework
       modeling           spectroscopy       evaluation
             │                 │                 │
             ▼                 ▼                 ▼
       Error correction   Metrological       General
                          characterization   methodology
```

Los dos primeros trabajos demuestran aplicaciones concretas.

El paper de TIM demuestra y evalúa la **metodología general**.

---

# 7. Preguntas de investigación

## RQ1 — Traceability

> Can `rfmeasurement` preserve sufficient measurement metadata and provenance to reconstruct the origin and processing history of an RF result?

Evaluar:

* instrumento;
* configuración;
* calibración;
* frecuencia;
* parámetros;
* condiciones;
* timestamp;
* procesamiento;
* versión del software;
* versión del dataset;
* parámetros utilizados.

---

## RQ2 — Reproducibility

> Can an independent researcher reproduce an RF analysis from the measurement record and associated computational workflow?

Evaluar:

* ejecución desde cero;
* mismo dataset;
* mismo resultado;
* misma versión del software;
* mismo pipeline;
* reconstrucción del entorno.

Métrica posible:

$$
E_{rep} =
\frac{|y_{rep}-y_{ref}|}{|y_{ref}|}
$$

adaptándola al tipo de measurand.

Para parámetros complejos como S11/S21, utilizar métricas apropiadas en magnitud/fase o representación compleja.

---

## RQ3 — Uncertainty

> Can the framework explicitly represent and propagate measurement uncertainty through RF analysis workflows?

Evaluar:

* fuentes de incertidumbre;
* incertidumbre de entrada;
* propagación;
* incertidumbre combinada;
* intervalos de cobertura;
* sensibilidad a las variables de entrada.

---

## RQ4 — Measurement quality

> Can the framework identify and quantify differences in measurement quality that are not visible in the nominal RF result alone?

Ejemplos:

* diferencias de calibración;
* repetibilidad;
* reconexión;
* ruido;
* deriva;
* instrumento;
* condiciones experimentales.

---

## RQ5 — Generality

> Can the same measurement representation and software methodology be applied across different RF measurement scenarios?

Utilizar como evidencia:

1. NanoVNA error modeling;
2. low-cost VNA characterization;
3. open-ended coaxial probe measurements;
4. otros datasets controlados.

---

## RQ6 — Overhead

> What computational and workflow overhead is introduced by the proposed measurement-aware approach?

Medir:

* tiempo de procesamiento;
* memoria;
* tamaño de datos;
* número de pasos;
* complejidad del workflow.

El objetivo no es necesariamente minimizar el overhead, sino cuantificarlo.

---

# 8. Diseño experimental propuesto

## 8.1. Baseline

Definir un workflow convencional:

```text
VNA
 ↓
Touchstone / measurement file
 ↓
RF analysis software
 ↓
Result
```

Por ejemplo:

```text
VNA
 ↓
.s1p / .s2p
 ↓
scikit-rf
 ↓
S11 / S21
```

---

## 8.2. Proposed workflow

```text
VNA
 ↓
Measurement acquisition
 ↓
rfmeasurement
 ├── Measurement metadata
 ├── Instrument information
 ├── Calibration information
 ├── Provenance
 ├── Quality assessment
 ├── Uncertainty
 └── Validation
 ↓
Reproducible result
```

---

# 9. Experimento 1 — Repeatability

## Objetivo

Cuantificar la variabilidad de una medida cuando se repite bajo condiciones nominalmente idénticas.

## Procedimiento

Realizar:

* N = 30–50 medidas;
* mismo instrumento;
* mismo DUT;
* mismo rango;
* misma calibración;
* mismo operador;
* condiciones controladas.

Posibles DUT:

* 50 Ω load;
* attenuator;
* coaxial cable;
* filter;
* calibration standard.

## Variables

Para cada medida:

* S11;
* S21;
* magnitud;
* fase;
* frecuencia;
* timestamp;
* metadata.

## Resultados

Calcular:

* media;
* desviación estándar;
* coeficiente de variación;
* distribución;
* repeatability uncertainty.

---

# 10. Experimento 2 — Reproducibility

Modificar deliberadamente condiciones:

* operador;
* reconexión;
* sesión;
* día;
* calibración;
* instrumento, si es posible.

Comparar:

$$
u_{repeatability}
$$

frente a:

$$
u_{reproducibility}
$$

El objetivo es demostrar que el framework puede representar y analizar explícitamente estas diferencias.

---

# 11. Experimento 3 — Calibration influence

Evaluar diferentes condiciones de calibración:

```text
Calibration A
Calibration B
Calibration C
```

o:

* calibración reciente;
* calibración reutilizada;
* estándares de diferente calidad;
* calibración de bajo coste.

Analizar el efecto sobre:

* S11;
* S21;
* magnitud;
* fase;
* incertidumbre;
* quality indicators.

---

# 12. Experimento 4 — Uncertainty propagation

Definir un modelo de medición:

$$
y=f(x_1,x_2,\ldots,x_n)
$$

Identificar fuentes de incertidumbre:

* instrumento;
* calibración;
* repetibilidad;
* conectores;
* cables;
* estándares;
* ruido;
* procesamiento.

Evaluar:

$$
u_c(y)
$$

y, cuando proceda:

$$
U=k u_c
$$

con el factor de cobertura definido explícitamente.

La metodología concreta debe justificarse según la magnitud y el procedimiento de medida.

---

# 13. Experimento 5 — Provenance

Crear dos datasets que produzcan resultados similares:

```text
Dataset A
Dataset B
```

pero que procedan de:

* diferentes calibraciones;
* diferentes sesiones;
* diferentes instrumentos;
* diferentes condiciones.

Demostrar que el resultado numérico por sí solo no contiene toda la información necesaria para distinguir ambos workflows.

`rfmeasurement` debe permitir reconstruir:

```text
Measurement
    ↓
Instrument
    ↓
Calibration
    ↓
Acquisition
    ↓
Processing
    ↓
Analysis
    ↓
Result
```

---

# 14. Experimento 6 — Reproducible analysis

Congelar:

* versión `rfmeasurement`;
* commit Git;
* dataset;
* notebooks/scripts;
* dependencias;
* parámetros.

Publicar:

* GitHub;
* release;
* Zenodo;
* DOI.

Un investigador externo debería poder ejecutar:

```bash
git clone ...
pip install ...
python reproduce.py
```

y obtener los resultados publicados dentro de tolerancias previamente definidas.

---

# 15. Experimento 7 — Generalization

Utilizar como casos independientes:

### Case A

**Experimental Error Modeling and Post-Processing Correction of NanoVNA Measurements Using Low-Cost Calibration Standards**

### Case B

**Metrological characterization of a low-cost vector network analyzer for open-ended coaxial probe dielectric spectroscopy of biological materials**

### Case C

Dataset controlado creado específicamente para el paper de TIM.

El caso C debería ser el experimento principal.

A y B deben funcionar como **external application evidence**, no como sustitutos del experimento central.

---

# 16. Comparación con herramientas existentes

Comparar conceptualmente y, cuando sea posible, experimentalmente con:

* scikit-rf;
* Touchstone;
* notebooks convencionales;
* scripts Python propios;
* workflows sin provenance explícito.

No presentar estas herramientas como incorrectas.

La comparación debe responder:

> ¿Qué información y capacidades adicionales aporta `rfmeasurement`?

---

# 17. Métricas

## Metrological metrics

* repeatability;
* reproducibility;
* bias;
* standard uncertainty;
* expanded uncertainty;
* coverage factor;
* sensitivity coefficients;
* confidence/coverage intervals.

## Measurement metrics

* S11 error;
* S21 error;
* magnitude error;
* phase error;
* frequency-dependent deviation.

## Software metrics

* execution time;
* memory;
* dataset size;
* test coverage;
* reproducibility error;
* environment reconstruction success.

## Provenance metrics

Definir, si resulta viable:

* porcentaje de información necesaria registrada;
* porcentaje de resultados reproducibles;
* número de variables necesarias para reconstrucción;
* pérdida de metadata entre workflows.

---

# 18. Criterios de éxito

El estudio debe definir los criterios **antes de ejecutar los experimentos**.

Ejemplos:

### Reproducibilidad

El resultado reproducido debe estar dentro de una tolerancia definida:

$$
|y_{rep}-y_{ref}| < \epsilon
$$

### Provenance

Debe poder reconstruirse:

* instrumento;
* calibración;
* dataset;
* versión;
* procesamiento.

### Uncertainty

La incertidumbre calculada debe ser consistente con la variabilidad experimental observada, dentro de los límites definidos por la metodología utilizada.

### Generalization

El mismo modelo conceptual debe poder utilizarse en más de un escenario experimental.

---

# 19. Arquitectura software que debe documentarse

La versión utilizada para el paper debería congelarse.

Documentar:

```text
rfmeasurement
│
├── measurement model
├── instrument model
├── calibration
├── uncertainty
├── quality
├── provenance
├── validation
├── analysis
└── reporting
```

Para cada módulo:

* responsabilidad;
* interfaces;
* inputs;
* outputs;
* dependencias;
* tests;
* limitaciones.

---

# 20. Reproducibility package

Crear un release específico:

```text
rfmeasurement-tim-study-v1.0
```

Conteniendo:

```text
tim-study/
├── data/
│   ├── raw/
│   ├── processed/
│   └── metadata/
│
├── experiments/
│   ├── repeatability/
│   ├── reproducibility/
│   ├── calibration/
│   └── uncertainty/
│
├── notebooks/
├── scripts/
├── figures/
├── tables/
├── environment/
│   ├── requirements.txt
│   └── environment.yml
│
└── README.md
```

Publicar el release en GitHub y archivarlo en Zenodo.

---

# 21. Relación con GitHub–Zenodo–ORCID

El estudio puede aprovechar la infraestructura de reproducibilidad ya desarrollada en el proyecto del autor:

```text
GitHub
   ↓
Version control
   ↓
Release
   ↓
Zenodo DOI
   ↓
ORCID
```

La versión exacta del software utilizada en el experimento debe quedar identificada.

Esto permite establecer:

> software version → dataset → experiment → results → paper

---

# 22. Posible título

## Opción principal

**An Uncertainty-Aware and Provenance-Preserving Software Framework for Reproducible RF Measurements**

## Alternativa más metrológica

**A Measurement-Aware Software Framework for Uncertainty, Quality Assessment, and Reproducibility in RF Measurements**

## Alternativa centrada en metodología

**Integrating Measurement Uncertainty, Quality Assessment, and Provenance in Reproducible RF Measurement Workflows**

La tercera opción probablemente representa mejor el enfoque de TIM si la contribución científica termina siendo principalmente metodológica.

---

# 23. Estructura propuesta del artículo

## I. Introduction

* importancia de RF measurements;
* problemas de reproducibilidad;
* incertidumbre;
* trazabilidad;
* limitaciones del workflow convencional;
* gap;
* contribution.

## II. Related Work

* RF measurement software;
* scikit-rf;
* uncertainty analysis;
* VNA calibration;
* measurement provenance;
* reproducible scientific software.

## III. Proposed Measurement-Aware Framework

* conceptual model;
* architecture;
* measurement representation;
* provenance;
* uncertainty;
* quality assessment;
* validation.

## IV. Experimental Methodology

* instrumentation;
* DUTs;
* calibration;
* experimental design;
* datasets;
* baseline;
* metrics.

## V. Results

* repeatability;
* reproducibility;
* calibration;
* uncertainty;
* quality;
* provenance;
* computational overhead.

## VI. Discussion

* metrological implications;
* software implications;
* generality;
* limitations;
* relationship with existing RF tools.

## VII. Reproducibility and Open Science

* GitHub;
* version;
* datasets;
* notebooks;
* Zenodo;
* DOI.

## VIII. Conclusion

* findings;
* contribution;
* limitations;
* future work.

---

# 24. Contribuciones que debería declarar el paper

La contribución debería dividirse explícitamente en cuatro partes:

### C1 — Measurement representation

A structured representation of RF measurements that combines measurement data with contextual and provenance information.

### C2 — Uncertainty-aware workflow

A software architecture for incorporating uncertainty information into RF measurement analysis.

### C3 — Quality and provenance

An integrated approach for assessing measurement quality and preserving measurement provenance.

### C4 — Experimental validation

An experimental evaluation across controlled measurements and independent RF application scenarios.

---

# 25. Qué NO debe ser la contribución

No afirmar:

* que `rfmeasurement` sustituye a scikit-rf;
* que el software hace las mediciones más exactas por sí mismo;
* que la incertidumbre calculada es automáticamente correcta;
* que la metodología es universal sin evidencia;
* que el software elimina los errores experimentales.

La afirmación debe ser más precisa:

> `rfmeasurement` provides a structured software layer for representing, analyzing, documenting, and reproducing RF measurements while explicitly incorporating measurement quality, uncertainty, and provenance.

---

# 26. Estado mínimo recomendado antes de submission

## Software

* [ ] v0.2.0 estable.
* [ ] API congelada para el estudio.
* [ ] tests completos.
* [ ] documentación.
* [ ] examples.
* [ ] benchmarks.
* [ ] CI.
* [ ] release.
* [ ] Zenodo DOI.

## Metrology

* [ ] modelo de incertidumbre definido.
* [ ] fuentes de incertidumbre identificadas.
* [ ] procedimiento de propagación definido.
* [ ] repetibilidad medida.
* [ ] reproducibilidad medida.
* [ ] calibración evaluada.
* [ ] criterios de validación definidos.

## Experimental

* [ ] dataset controlado.
* [ ] baseline.
* [ ] medidas repetidas.
* [ ] múltiples condiciones.
* [ ] comparación cuantitativa.
* [ ] análisis estadístico.

## Reproducibility

* [ ] scripts.
* [ ] notebooks.
* [ ] raw data.
* [ ] processed data.
* [ ] environment.
* [ ] exact software version.
* [ ] automated reproduction.

---

# 27. Estrategia de publicación

El paper de TIM debe ocupar una posición superior a los dos trabajos de aplicación.

### Paper 1

**Experimental Error Modeling and Post-Processing Correction of NanoVNA Measurements Using Low-Cost Calibration Standards**

Contribución:

> error modeling + correction.

### Paper 2

**Metrological characterization of a low-cost vector network analyzer for open-ended coaxial probe dielectric spectroscopy of biological materials**

Contribución:

> VNA characterization + dielectric spectroscopy + metrology.

### Paper 3 — TIM

**An Uncertainty-Aware and Provenance-Preserving Software Framework for Reproducible RF Measurements**

Contribución:

> general measurement methodology + software architecture + experimental validation.

---

# 28. Riesgo principal de solapamiento

Debe evitarse que el paper de TIM:

* reutilice las mismas figuras;
* reutilice los mismos resultados;
* presente como nuevos resultados datos ya publicados;
* repita sustancialmente la metodología de los otros papers.

Los trabajos anteriores deben citarse y describirse como **evidencia previa de aplicación**.

El experimento principal del paper de TIM debe ser nuevo.

---

# 29. Resultado esperado

El resultado ideal del estudio no sería demostrar:

> "`rfmeasurement` works."

Sino demostrar:

> **A measurement-aware software architecture can integrate uncertainty, measurement quality, provenance, and reproducibility into RF measurement workflows, and its benefits can be experimentally evaluated across controlled and real-world measurement scenarios.**

Esto sitúa el trabajo en la intersección de:

```text
        RF Instrumentation
               │
               │
        Measurement Science
               │
        ┌──────┴──────┐
        │             │
  Uncertainty    Reproducibility
        │             │
        └──────┬──────┘
               │
       Scientific Software
               │
               ▼
        rfmeasurement
```

---

# 30. Decisión sobre v0.2.0

La v0.2.0 **no necesita ser una versión "final" del software**.

Debe ser:

> **la primera versión suficientemente estable y reproducible para congelar una metodología experimental.**

Por tanto:

```text
v0.2.0
   │
   ├── freeze API
   ├── freeze experiment
   ├── freeze datasets
   └── freeze environment
             │
             ▼
       TIM study release
             │
             ├── GitHub
             ├── Zenodo
             └── DOI
```

La posterior v0.3/v1.0 puede incorporar mejoras sin invalidar el artículo.

---

# 31. Próximo paso recomendado

Antes de redactar el paper:

1. finalizar `rfmeasurement` v0.2.0;
2. revisar específicamente el modelo de incertidumbre;
3. definir el experimento controlado principal;
4. definir las RQs y métricas;
5. ejecutar primero un **pilot experiment**;
6. comprobar si los resultados realmente permiten responder las RQs;
7. ampliar el experimento;
8. congelar dataset + software + entorno;
9. generar las figuras y tablas;
10. redactar el artículo de TIM a partir de los resultados.

El paper debe escribirse **después del diseño y del piloto experimental**, no antes.
