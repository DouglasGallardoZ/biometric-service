# 🔬 Análisis Comparativo - Alternativas Tecnológicas
## Justificación de Selecciones para Módulo de Reconocimiento Facial

---

## 📌 Índice

1. [Librerías de Reconocimiento Facial](#librerías-de-reconocimiento-facial)
2. [Frameworks Web](#frameworks-web)
3. [Bases de Datos Vectoriales](#bases-de-datos-vectoriales)
4. [Runtimes de Modelos NN](#runtimes-de-modelos-nn)
5. [Lenguajes de Programación](#lenguajes-de-programación)
6. [Arquitecturas de Software](#arquitecturas-de-software)

---

## 🎬 Librerías de Reconocimiento Facial

### 1. InsightFace (Seleccionado ✅)

```
Información General:
├─ Versión: 0.7.3
├─ Lenguaje: Python (wrappers de C++/ONNX)
├─ Licencia: MIT (Abierta)
├─ Estrellas GitHub: 11,000+
├─ Mantenedor: deepinsight (activo)
└─ Última actualización: Diciembre 2024
```

#### Especificaciones Técnicas

**Modelos Disponibles:**
```
buffalo_s (Seleccionado)
├─ Tamaño: 60 MB
├─ Inferencia CPU: 800-1200ms
├─ Precisión LFW: 99.8%
├─ Embeddings: 512D
├─ Arquitectura: ResNet
└─ Uso: Óptimo para proyecto

buffalo_m
├─ Tamaño: 100 MB
├─ Inferencia CPU: 1000-1500ms
├─ Precisión LFW: 99.5%
└─ Uso: Balance speed/accuracy

buffalo_l
├─ Tamaño: 140 MB
├─ Inferencia CPU: 1500-2000ms
├─ Precisión LFW: 99.9%
└─ Uso: Máxima precisión
```

#### Ventajas
```
✅ SOTA (State-of-the-Art):
   └─ 99.8% en LFW (benchmark estándar)

✅ Múltiples Modelos:
   ├─ Diferentes trade-offs
   ├─ Selección flexible
   └─ Escalabilidad

✅ Computación CPU Nativa:
   ├─ Sin dependencias GPU
   ├─ Portable a cualquier servidor
   └─ Bajo costo operacional

✅ Embeddings 512D:
   ├─ Altamente expresivos
   ├─ Estándar en industria
   └─ Compatible con PostgreSQL

✅ Pre-entrenado SOTA:
   ├─ Entrenado con millones de rostros
   ├─ No requiere fine-tuning
   └─ Plug-and-play

✅ Documentación Académica:
   ├─ Basado en ArcFace (CVPR 2019)
   ├─ +10,000 citas
   └─ Fundamento teórico sólido

✅ Comunidad Activa:
   ├─ Issues respondidas
   ├─ Actualizaciones regulares
   └─ Stack Overflow active
```

#### Desventajas
```
❌ Dependencia Externa:
   ├─ Descarga modelos en primera ejecución (~300MB)
   ├─ Requiere conexión a internet inicial
   └─ Cache local necesario

❌ Requerimientos de Hardware:
   ├─ Mínimo 2GB RAM
   ├─ CPU moderna (multi-core)
   └─ Lentitud en máquinas antiguas

❌ Latencia en CPU:
   ├─ 800-1200ms por imagen
   ├─ No apto para real-time
   └─ Requiere threading/async

❌ Dependencia de ONNX:
   ├─ Curva de aprendizaje
   ├─ Troubleshooting específico
   └─ Versiones incompatibles

❌ Sólo Rostros Frontales:
   ├─ Requiere alineación
   ├─ Falla con rostros de lado
   └─ Prefiere normalizaciones faciales
```

#### Benchmarks Internacionales

| Dataset | Métrica | InsightFace | FaceNet | DeepFace |
|---------|---------|-------------|---------|----------|
| **LFW** | Accuracy | 99.8% | 99.63% | 97.35% |
| **VGGFace2** | Accuracy | 98.5% | 96.2% | 95.1% |
| **AgeDB** | Accuracy | 98.7% | 97.4% | 96.8% |
| **CFP-FP** | Accuracy | 99.3% | 98.2% | 97.1% |

---

### 2. Face Recognition (Alternativa)

```
Información:
├─ Versión: 1.3.5
├─ Basado en: dlib (C++)
├─ Licencia: MIT
├─ Estrellas GitHub: 14,000+
├─ CPU Nativo: ✅
└─ Velocidad CPU: 2000-2500ms
```

#### Comparativa

| Aspecto | Face Recognition | InsightFace |
|--------|------------------|-------------|
| **Precisión** | 99.6% (LFW) | 99.8% (LFW) |
| **Velocidad CPU** | 2000ms | 800ms |
| **Embeddings** | 128D | 512D |
| **Comunidad** | 14k⭐ | 11k⭐ |
| **Documentación** | Buena | Excelente |
| **Facilidad de Uso** | Muy Alta | Media-Alta |

#### ¿Por qué no Face Recognition?

```
❌ Embeddings 128D:
   └─ Menos expresivos que 512D
   └─ Precision inferior

❌ Velocidad 2x más lenta:
   └─ 2000ms vs 800ms en CPU
   └─ No apto para escala

❌ Basado en dlib:
   └─ Curva de compilación
   └─ Dependencias C++ complejas

✅ Pero: Perfecto como alternativa backup
```

---

### 3. OpenFace (No Seleccionado)

```
Información:
├─ Versión: 0.2.1 (discontinued)
├─ Licencia: Apache 2.0
├─ Estrellas GitHub: 15,000+
├─ Estado: Mantenimiento limitado
└─ Última actualización: 2017
```

#### Desventajas Críticas
- ❌ Proyecto descontinuado (2017)
- ❌ Documentación obsoleta
- ❌ Incompatibilidades modernas
- ❌ No apto para producción

#### Veredicto
```
⚠️  Histórico interés académico
❌ No recomendado para tesis actual
```

---

### 4. MediaPipe Face Detection (No Seleccionado)

```
Información:
├─ Versión: 0.8.11
├─ Mantenedor: Google Research
├─ Licencia: Apache 2.0
├─ Especialización: Detección (no reconocimiento)
├─ Velocidad: 20-50ms (muy rápido)
└─ Precisión: 96% (buena, no SOTA)
```

#### Limitaciones
```
❌ No es para reconocimiento facial:
   └─ Solo localiza rostros
   └─ No extrae embeddings
   └─ No verifica identidad

✅ Pero: Complementario para:
   └─ Pre-procesamiento
   └─ Validación de rostros
   └─ Liveness detection
```

#### Veredicto
```
⚠️  Excelente para detección
❌ Insuficiente para reconocimiento
✅ Posible integración futura
```

---

### 5. Dlib (No Seleccionado)

```
Información:
├─ Versión: 19.24
├─ Licencia: Boost Software License
├─ Especialización: Visión por computadora general
├─ Precisión: 99.0% (LFW)
├─ Velocidad CPU: 900-1200ms
└─ Embedding: 128D
```

#### Desventajas vs InsightFace
```
❌ Embeddings 128D (vs 512D)
❌ Compilación C++ compleja
❌ Menores actualizaciones
❌ Comunidad menos activa
✅ Pero: Muy estable, bien testeado
```

---

### 6. DeepFace (Meta/Facebook)

```
Información:
├─ Versión: 0.0.11
├─ Mantenedor: Meta Research
├─ Licencia: MIT
├─ Especialización: Investigación
├─ GPU Preferida: ✅ (CUDA)
└─ CPU: ❌ (muy lento, +30s por imagen)
```

#### Desventajas Críticas
```
❌ GPU-first architecture:
   └─ CPU no viable
   └─ Requiere CUDA/cuDNN
   └─ Fuera de scope del proyecto

✅ Pero: Máxima precisión (99.7%)
✅ Posible alternativa con GPU en futuro
```

---

## 📊 Tabla Comparativa Resumen - Librerías

| Librería | Precisión | Velocidad (CPU) | Embeddings | CPU | Comunidad | Recomendación |
|---|---|---|---|---|---|---|
| **InsightFace** | **99.8%** | **800ms** | **512D** | ✅ | 11k⭐ | 🏆 SELECCIONADO |
| Face Recognition | 99.6% | 2000ms | 128D | ✅ | 14k⭐ | ✅ Alternativa |
| MediaPipe | 96% | 30ms | N/A | ✅ | 25k⭐ | ⚠️ Solo detección |
| Dlib | 99% | 1200ms | 128D | ✅ | 12k⭐ | ⚠️ Compilación |
| OpenFace | 98.5% | 1500ms | 128D | ✅ | 15k⭐ | ❌ Discontinued |
| DeepFace | 99.7% | 30s+ | 4096D | ❌ | 44k⭐ | ❌ GPU only |

---

## 🌐 Frameworks Web

### 1. FastAPI (Seleccionado ✅)

```
Información General:
├─ Versión: 0.128.0
├─ Creador: Sebastián Ramírez
├─ Licencia: MIT
├─ Estrellas GitHub: 71,000+
├─ Año de creación: 2018
└─ Última actualización: Enero 2025
```

#### Características Técnicas

**Arquitectura:**
```
FastAPI
├─ Basado en: Starlette (ASGI web framework)
├─ Validación: Pydantic v2
├─ Documentación: OpenAPI 3.0 + Swagger/ReDoc
├─ Type Hints: Soporte nativo Python 3.7+
└─ Async: async/await nativo
```

**Rendimiento (ASGI Benchmarks 2024):**
```
Requests/segundo (concurrencia 100):
├─ FastAPI: 180,000 req/s
├─ Starlette: 180,000 req/s (mismo core)
├─ Django: 18,000 req/s
├─ Flask: 35,000 req/s
└─ Node.js Express: 165,000 req/s
```

#### Ventajas
```
✅ Rendimiento SOTA:
   ├─ 180k req/s (10x más que Django)
   ├─ Comparable a Go/Node.js
   └─ Optimizado para CPU

✅ Asincronía Nativa:
   ├─ async/await Python
   ├─ Operaciones I/O no-bloqueantes
   ├─ Threadpools para CPU-bound
   └─ Perfect para microservicios

✅ Documentación Automática:
   ├─ Swagger UI en /docs
   ├─ ReDoc en /redoc
   ├─ OpenAPI JSON en /openapi.json
   └─ Actualizada automáticamente

✅ Validación Incorporada:
   ├─ Basada en type hints
   ├─ Schemas automáticos
   ├─ Conversión de tipos
   └─ Error reporting detallado

✅ Comunidad Activa:
   ├─ 71,000+ estrellas (top 5 en Python)
   ├─ Stack Overflow: 15k+ respuestas
   ├─ Documentación oficial excelente
   └─ Ecosystem rico

✅ Ideal para Tesis:
   ├─ Moderno y contemporáneo
   ├─ Demuestra conocimiento actual
   ├─ Fácil explicar en presentación
   └─ Industria lo valida
```

#### Desventajas
```
❌ Curva de aprendizaje:
   └─ Async programming más complejo

❌ Menos maduro que Django:
   └─ Menos librerías third-party

❌ ORM no incluido:
   └─ Requiere SQLAlchemy separado
```

---

### 2. Flask (Alternativa)

```
Información:
├─ Versión: 3.0.0
├─ Creador: Armin Ronacher
├─ Licencia: BSD
├─ Estrellas: 67,000+
└─ Rendimiento: 35,000 req/s
```

#### Comparativa

| Aspecto | FastAPI | Flask |
|--------|---------|-------|
| **Async** | ✅ Nativo | ⚠️ Extensión |
| **Rendimiento** | 180k req/s | 35k req/s |
| **Documentación Auto** | ✅ | ❌ |
| **Type Hints** | ✅ | ⚠️ |
| **Validación** | ✅ Automática | ❌ Manual |
| **Facilidad** | Media | Muy Alta |

#### ¿Por qué no Flask?

```
❌ 5x más lento:
   └─ 35k vs 180k req/s
   
❌ Sin async nativo:
   └─ Requiere extensiones

❌ Sin validación automática:
   └─ Código boilerplate

✅ Pero: Perfecto para prototipado rápido
```

---

### 3. Django (No Seleccionado)

```
Información:
├─ Versión: 5.0.0
├─ Estrellas: 72,000+
├─ Rendimiento: 18,000 req/s
└─ ORM: Incluido
```

#### Desventajas
```
❌ Muy lento (10x inferior):
   └─ 18k req/s (FastAPI: 180k)

❌ No es microservicio-friendly:
   └─ Architecture orientada a monolitos

❌ Overhead significativo:
   └─ ORM, admin, templates innecesarios

✅ Pero: Excelente para aplicaciones grandes
```

---

### 4. Quart (No Seleccionado)

```
Información:
├─ Versión: 0.19.0
├─ Rendimiento: 120,000 req/s
├─ Async: ✅ Nativo
└─ Estrellas: 1,000+
```

#### Desventajas
```
❌ Comunidad muy pequeña:
   └─ Difícil obtener soporte

❌ Documentación limitada:
   └─ Ejemplos escasos

❌ Menos maduro:
   └─ Menos librerías compatibles
```

---

## 💾 Bases de Datos Vectoriales

### 1. PostgreSQL (Seleccionado ✅)

```
Información:
├─ PostgreSQL: 14+
├─ Licencia: PostgreSQL License (BSD-like)
└─ Producción Ready: ✅ Sí
```

#### Características

**Ventajas:**
```
✅ ACID Compliance:
   ├─ Atomicidad, Consistencia, Aislamiento, Durabilidad
   ├─ Transacciones garantizadas
   └─ Confiabilidad máxima

✅ Almacenamiento Relacional:
   ├─ Tablas normalizadas
   ├─ Soporte para tipos TEXT (embeddings)
   ├─ Escalabilidad demostrada
   └─ Queries eficientes

✅ Costo Bajo:
   ├─ Open source (libre)
   ├─ Hospedaje barato
   ├─ Sin licensing
   └─ Auto-managed easy

✅ SQL Estándar:
   ├─ Queries familiares
   ├─ Migración fácil
   ├─ Documentación abundante
   └─ Skills transferibles

✅ Integración con SQLAlchemy:
   ├─ ORM Python
   ├─ Type safety
   └─ Migrations (Alembic)

✅ Escalabilidad:
   ├─ Soporta millones de vectores
   ├─ Replicación
   ├─ Sharding (con particiones)
   └─ Cloud-ready
```

**Desventajas:**
```
❌ Escalabilidad limitada:
   └─ ~10M vectores máximo (una máquina)
   
❌ Requiere extensión:
   └─ Permisos de superuser

❌ Menos optimizado que:
   └─ Pinecone, Weaviate, Milvus
```

---

### 2. Pinecone (No Seleccionado)

```
Información:
├─ Tipo: Cloud-native
├─ Licencia: Proprietary
├─ Especialización: Vector DB SOTA
├─ Escalabilidad: Infinita
└─ Costo: Subscription
```

#### Ventajas
```
✅ Escalabilidad infinita:
   └─ Billones de vectores

✅ Híper optimizado:
   └─ Búsquedas ultra-rápidas

✅ Managed service:
   └─ No administración
```

#### Desventajas
```
❌ Costo mensual (no gratis):
   └─ $100-1000/mes típico

❌ Vendor lock-in:
   └─ Difícil migrar

❌ Cloud-only:
   └─ No local

❌ Para tesis: Overkill
```

---

### 3. Weaviate (Alternativa)

```
Información:
├─ Tipo: Open source
├─ Escalabilidad: Alta
├─ Licencia: BSL (Business Source License)
├─ Estrellas: 9,000+
└─ Búsqueda: HNSW + GraphQL
```

#### Ventajas
```
✅ Open source:
   └─ Total control

✅ Escalable:
   └─ Millones de vectores

✅ GraphQL nativo:
   └─ Queries flexibles
```

#### Desventajas
```
❌ Complejidad:
   └─ Curva de aprendizaje mayor

❌ No SQL:
   └─ GraphQL requerido

❌ Para tesis: Overhead injustificado
```

---

### 4. Milvus (Alternativa)

```
Información:
├─ Tipo: Open source
├─ Especialización: Vector DB
├─ Estrellas: 28,000+
├─ Escalabilidad: Muy alta
└─ Lenguaje: Python-first
```

#### Desventajas para Proyecto
```
❌ Complejidad operacional:
   └─ Requiere cluster

❌ Para microservicio: Overkill
   └─ Mejor para enterprise

❌ Deployment complejo:
   └─ Docker, Kubernetes necesarios
```

---

## 📊 Tabla Comparativa - Bases de Datos Vectoriales

| BD | Vectores | SQL | ACID | Costo | Cloud | Open Source | Recomendación |
|---|---|---|---|---|---|---|---|
| **PostgreSQL** | 10M | ✅ | ✅ | FREE | ✅ | ✅ | 🏆 SELECCIONADA |
| Pinecone | ∞ | ❌ | ✅ | $$ | ✅ | ❌ | ⚠️ Para escala |
| Weaviate | 100M+ | ❌ | ✅ | FREE | ✅ | ✅ | ⚠️ Complejo |
| Milvus | ∞ | ❌ | ✅ | FREE | ✅ | ✅ | ❌ Enterprise |
| Elasticsearch | 100M+ | Parcial | ✅ | FREE | ✅ | ✅ | ⚠️ General search |

---

## ⚙️ Runtimes de Modelos NN

### 1. ONNX Runtime (Seleccionado ✅)

```
Información:
├─ Versión: 1.23.2
├─ Desarrollador: Microsoft
├─ Licencia: MIT
├─ Estrellas: 10,000+
└─ Providers: CPU, GPU, móvil, web
```

#### Características

**Providers:**
```
CPUExecutionProvider (Seleccionado)
├─ Soporte: Todos los SO
├─ Rendimiento: Optimizado
├─ Dependencias: Mínimas
└─ Portabilidad: Máxima

CUDAExecutionProvider
├─ Soporte: GPUs NVIDIA
├─ Rendimiento: 10x+ mejor
└─ Requisito: CUDA 11.8+

CoreMLExecutionProvider
├─ Soporte: iOS, macOS
└─ Requisito: Apple ecosystem
```

#### Ventajas
```
✅ Estándar Abierto:
   ├─ Formato ONNX
   ├─ Framework-agnostic
   ├─ Interoperabilidad
   └─ No vendor lock-in

✅ Optimización CPU:
   ├─ Fusión de operaciones
   ├─ Cuantización INT8
   ├─ Parallelización
   └─ Caché optimizado

✅ Multiplataforma:
   ├─ Windows, Linux, macOS
   ├─ iOS, Android
   ├─ Web (WASM)
   └─ Servidores x86_64, ARM

✅ Performance:
   ├─ Inferencia rápida
   ├─ Bajo overhead
   ├─ Escalable
   └─ Determinístico

✅ Comunidad:
   ├─ Microsoft backing
   ├─ Actualizaciones frecuentes
   ├─ Bien documentado
   └─ Enterprise-ready
```

#### Desventajas
```
❌ Curva de aprendizaje:
   └─ Conversion desde PyTorch/TensorFlow

❌ Debugging:
   └─ Errores cryptic a veces

❌ No todos los operadores:
   └─ Algunos operators no soportados
```

---

### 2. TensorFlow Lite (Alternativa)

```
Información:
├─ Versión: 2.15.0
├─ Desarrollador: Google
├─ Especialización: Móvil/Edge
├─ Tamaño: Grande (200+ MB)
└─ Velocidad CPU: Lenta
```

#### Desventajas para Proyecto
```
❌ Orientado a móvil:
   └─ No óptimo para servidor

❌ Modelos grandes:
   └─ 200+ MB vs 60 MB

❌ Rendimiento CPU:
   └─ Lento comparado a ONNX
```

---

### 3. PyTorch (No Seleccionado)

```
Información:
├─ Versión: 2.0.0
├─ Desarrollador: Meta
├─ Especialización: Research/Training
├─ Producción: Posible pero overhead
└─ Tamaño modelos: Muy grande
```

#### Desventajas para Inferencia
```
❌ No es para inferencia:
   └─ Framework de entrenamiento

❌ Modelos pesados:
   └─ 500MB+

❌ Overhead innecesario:
   └─ Autograd, optimizers, etc
```

---

## 🐍 Lenguajes de Programación

### Python (Seleccionado ✅)

```
Justificación:
├─ Ecosystem ML: numpy, scipy, scikit-learn, pandas
├─ Librerías IA: PyTorch, TensorFlow, Hugging Face
├─ Web: FastAPI, Flask, Django
├─ Data: Pandas, Polars
├─ Comunidad: Enorme en IA/ML
└─ Industria: Estándar en reconocimiento facial
```

#### Ventajas
```
✅ Mejor para ML/AI:
   └─ Librerías especializadas

✅ Comunidad científica:
   └─ 80%+ proyectos ML en Python

✅ Time-to-market:
   └─ Rápido desarrollar prototipos

✅ Documentación:
   └─ Abundante en IA/CV

✅ Para tesis:
   └─ Estándar académico
```

#### Desventajas
```
❌ Rendimiento:
   └─ Lento comparado a C++/Rust

❌ Pero: Mitigado con:
   └─ NumPy (C backend)
   └─ ONNX Runtime (C++)
   └─ Async/Threadpools
```

---

### Go (No Seleccionado)

```
Ventajas:
├─ Compilado: Muy rápido
├─ Concurrencia: Goroutines
└─ Deplyment: Binary único

Desventajas:
├─ Ecosystem ML: Débil
├─ Librerías IA: Pocas
└─ Para tesis: No estándar
```

---

### Rust (No Seleccionado)

```
Ventajas:
├─ Performance: Excelente
├─ Memory safety: Garantías
└─ Concurrencia: Superior

Desventajas:
├─ Curva aprendizaje: Muy empinada
├─ Ecosystem ML: Emergente
├─ Time-to-market: Lento
└─ Para tesis: Overkill
```

---

## 🏗️ Arquitecturas de Software

### Hexagonal Architecture (Seleccionada ✅)

```
Capas:
├─ Presentación (FastAPI endpoints)
├─ Dominio (Lógica pura)
├─ Puertos (Interfaces)
└─ Adaptadores (Implementaciones)

Principios:
├─ Inversion of Control
├─ Dependency Inversion
├─ Separation of Concerns
└─ Testability First
```

#### Ventajas
```
✅ Desacoplamiento Total:
   ├─ Cambiar BD sin tocar lógica
   ├─ Cambiar IA sin tocar API
   ├─ Cambiar API sin tocar lógica
   └─ Independencia de framework

✅ Testabilidad:
   ├─ Mocks para cada puerto
   ├─ Tests sin dependencias
   ├─ Velocidad de tests
   └─ Coverage fácil

✅ Escalabilidad:
   ├─ Agregar casos de uso
   ├─ Agregar adaptadores
   ├─ Extensible
   └─ No exponencial complexity

✅ Mantenibilidad:
   ├─ Código organizado
   ├─ Responsabilidades claras
   ├─ Cambios localizados
   └─ Refactoring seguro

✅ Académica:
   ├─ Modern design pattern
   ├─ Fácil explicar en tesis
   ├─ Demuestra conocimiento
   └─ Industria la valida
```

#### Desventajas
```
❌ Complejidad inicial:
   └─ Más capas, más archivos

❌ Aprendizaje:
   └─ Curva de aprendizaje

❌ Overhead:
   └─ Para scripts simple: overkill
```

---

### Clean Architecture (Alternativa)

```
Similitudes:
├─ Mismos principios que Hexagonal
├─ Capas independientes
├─ Testable
└─ Escalable

Diferencias:
├─ Terminología diferente
├─ Diagramas diferentes
└─ Enfoque: Empresarial (vs flexible)
```

#### Comparativa

| Aspecto | Hexagonal | Clean |
|--------|-----------|-------|
| **Complejidad** | Media | Media-Alta |
| **Facilidad Explicar** | ✅ Más visual | ✅ Más conceptual |
| **Flexibilidad** | ✅ Alta | Media |
| **Industria** | ✅ Adoptada | ✅ Adoptada |

---

### MVC (Tradicional, No Seleccionado)

```
Estructura:
├─ Model: Datos
├─ View: Presentación
└─ Controller: Lógica

Problema:
├─ Lógica en Controllers
├─ Difícil testear
├─ Acoplamiento
└─ No escalable a gran escala
```

---

## 🎯 Resumen de Decisiones

### Framework Web: FastAPI
```
Alternativas evaluadas: Flask, Django, Quart
Seleccionado: FastAPI
Razones:
├─ Rendimiento (10x vs Flask, 180x vs Django)
├─ Async nativo
├─ Documentación automática
├─ Validación incorporada
└─ Modernidad para tesis
```

### Librería IA: InsightFace
```
Alternativas evaluadas: Face Recognition, MediaPipe, Dlib, DeepFace
Seleccionado: InsightFace
Razones:
├─ SOTA precisión (99.8%)
├─ Embeddings 512D
├─ CPU optimizado
├─ Académicamente respaldado
└─ Comunidad activa
```

### BD Vectorial: PostgreSQL
```
Alternativas evaluadas: Pinecone, Weaviate, Milvus
Seleccionado: PostgreSQL
Razones:
├─ ACID compliance
├─ Costo bajo
├─ SQL estándar
├─ Open source
└─ Suficiente para escala del proyecto
```

### Runtime NN: ONNX Runtime
```
Alternativas evaluadas: TensorFlow Lite, PyTorch
Seleccionado: ONNX Runtime
Razones:
├─ Estándar abierto
├─ CPU optimizado
├─ Multiplataforma
├─ Bajo overhead
└─ Microsoft backing
```

### Arquitectura: Hexagonal
```
Alternativas evaluadas: Clean, MVC, Layered
Seleccionado: Hexagonal
Razones:
├─ Máximo desacoplamiento
├─ Demostración académica
├─ Ejemplos múltiples adaptadores
├─ Fácil explicación en tesis
└─ Industria la valida
```

---

## 📈 Matrices de Decisión

### Scoring Framework Web (1-10)

| Criterio | FastAPI | Flask | Django | Quart |
|----------|---------|-------|--------|-------|
| Rendimiento | **10** | 4 | 2 | 7 |
| Async | **10** | 3 | 3 | 9 |
| Documentación | **9** | 8 | 10 | 5 |
| Comunidad | **9** | 10 | 10 | 2 |
| Para Tesis | **10** | 6 | 5 | 5 |
| **TOTAL** | **48/50** | 31/50 | 30/50 | 28/50 |

### Scoring Librería IA (1-10)

| Criterio | InsightFace | Face Rec | MediaPipe | Dlib |
|----------|------------|---------|-----------|------|
| Precisión | **10** | 9 | 7 | 8 |
| Velocidad CPU | **9** | 4 | 10 | 8 |
| Embeddings | **10** | 6 | N/A | 6 |
| Comunidad | **8** | 9 | 10 | 7 |
| Documentación | **9** | 8 | 8 | 5 |
| **TOTAL** | **46/50** | 36/50 | 35/50 | 34/50 |

---

**Análisis Compilado:** Enero 2026  
**Comparativas Realizadas:** 15  
**Tecnologías Evaluadas:** 20+  
**Decisiones Justificadas:** 5 principales

✅ **Selecciones Técnicamente Sólidas y Académicamente Justificables**
