# Diagrama de Arquitectura Hexagonal

## Estructura en Capas

```
┌─────────────────────────────────────────────────────────────────┐
│                   CAPA DE PRESENTACIÓN                          │
│                      (app/main.py)                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │  /enroll     │  │  /verify     │  │  /validate   │           │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘           │
└─────────┼──────────────────┼──────────────────┼──────────────────┘
          │                  │                  │
          └──────────────────┼──────────────────┘
                             │
┌─────────────────────────────▼──────────────────────────────────┐
│              CAPA DE APLICACIÓN (Casos de Uso)                │
│                  (app/domain/casos_uso.py)                    │
│  ┌──────────────────┐  ┌──────────────────┐                   │
│  │ CasoDeUsoEnroll. │  │ CasoDeUsoVerif.  │                   │
│  └────────┬─────────┘  └────────┬─────────┘                   │
│           │                     │                              │
└───────────┼─────────────────────┼──────────────────────────────┘
            │                     │
┌───────────▼─────────────────────▼──────────────────────────────┐
│                    CAPA DE DOMINIO                             │
│              (app/domain/models.py + puertos.py)              │
│                                                                │
│  MODELOS:                    PUERTOS (Interfaces):           │
│  • Embedding                 • PuertoAnalizadorRostros        │
│  • PersonaFoto               • PuertoAlmacenamientoFotos      │
│  • PersonaEmbedding          • PuertoAlmacenamientoEmbeddings │
│  • VerificacionFacial        • PuertoSistemaArchivos         │
└───────────┬──────────────────────┬──────────────────────────────┘
            │                      │
            │ implementa           │ implementa
            │                      │
┌───────────▼────────┐  ┌──────────▼─────────────────────────────┐
│ CAPA DE ADAPTADORES│  │ CAPA DE INFRAESTRUCTURA                │
│ (app/adaptadores/) │  │ (app/infraestructura/)                 │
│                    │  │                                        │
│ Adaptadores:       │  │ ConfiguradorAplicacion:               │
│ • InsightFace      │  │ • Crea adaptadores                    │
│ • PostgreSQL       │  │ • Inyecta dependencias                │
│ • SistemaArchivos  │  │ • Gestiona configuración              │
└────────┬───────────┘  └────────────┬─────────────────────────┘
         │                           │
         │ usa                       │ configura
         │                           │
         └──────────────┬────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
    ┌───▼────┐  ┌──────▼────┐  ┌──────▼──────┐
    │PostgreSQL  │ InsightFace  │ Sistema     │
    │           │            │ Archivos    │
    └───────────┘  └───────────┘  └────────────┘
```

## Flujo de Mensajes - Caso de Uso Enrollamiento

```
Cliente HTTP
    │
    │ POST /enroll
    │
    ▼
┌─────────────────────────────────┐
│ main.py                         │
│ registrar_residente()           │
└────────────┬────────────────────┘
             │
             ├─ Leer imágenes
             │
             ▼
┌─────────────────────────────────┐
│ ConfiguradorAplicacion          │
│ crear_caso_enrollamiento()      │
└────────────┬────────────────────┘
             │
             ▼
┌──────────────────────────────────────────┐
│ CasoDeUsoEnrollamiento.ejecutar()        │
└──┬────────────────────────────────────┬──┘
   │                                    │
   │ Para cada imagen:                 │
   │                                    │
   ├─► PuertoSistemaArchivos           │
   │   guardar_imagen()                 │
   │   │                                │
   │   └─► AdaptadorSistemaArchivosLocal
   │                                    │
   ├─► PuertoAnalizadorRostros         │
   │   obtener_embedding()              │
   │   │                                │
   │   └─► AdaptadorInsightFace        │
   │                                    │
   └─► PuertoAlmacenamientoFotos       │
       guardar_foto()                   │
       │                                │
       └─► AdaptadorPostgresFotos      │
                                       │
                        ┌──────────────┘
                        │
                        │ Embedding promedio
                        │
                        ▼
              ┌──────────────────────┐
              │ PuertoAlmacenamiento │
              │ Embeddings.guardar() │
              │                      │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │ AdaptadorPostgres    │
              │ Embeddings           │
              └──────────┬───────────┘
                         │
                         ▼
                    PostgreSQL
```

## Independencia de Adaptadores

```
┌─────────────────────────────────────────┐
│   LÓGICA DE NEGOCIO (Casos de Uso)      │ ◄── NO CAMBIA
│   Totalmente independiente              │
└─────────────────────────────────────────┘
                    ▲
         ┌──────────┼──────────┐
         │          │          │
    Cambio A    Cambio B   Cambio C
         │          │          │
         ▼          ▼          ▼
  ┌──────────┐ ┌──────────┐ ┌──────────┐
  │InsightFace │ │Face Recog│ │DeepFace  │ ◄── ADAPTADORES
  │           │ │          │ │          │     INTERCAMBIABLES
  └──────────┘ └──────────┘ └──────────┘
  
Cambiar de InsightFace a Face Recognition:
- Solo crear nuevo AdaptadorFaceRecognitionLib
- Implementar PuertoAnalizadorRostros
- Actualizar ConfiguradorAplicacion
- ¡El dominio NO se ve afectado!
```

## Inyección de Dependencias

```
┌──────────────────────────┐
│ ConfiguradorAplicacion   │
└────────────┬─────────────┘
             │
    ┌────────┴────────┬────────────┬──────────────┐
    │                 │            │              │
    ▼                 ▼            ▼              ▼
Analizador         FotoStore    EmbeddingStore  Archivos
    │                 │            │              │
    ├─┐               ├─┐          ├─┐            ├─┐
    │ └─ Puerto        │ └─ Puerto  │ └─ Puerto    │ └─ Puerto
    │ └─ Adaptador     │ └─ Adaptador           │ └─ Adaptador
    │                 │            │              │
    └─ Inyectar en ────┴────────────┴──────────────┘
       CasoDeUsoEnrollamiento
```

## Beneficios Visuales

```
ANTES (Acoplado):
┌─────────────────────────┐
│   main.py              │
│ ├─ database.py         │ ◄─ Fuerte acoplamiento
│ ├─ face_engine.py      │ ◄─ Difícil de testear
│ └─ image_proc.py       │ ◄─ Cambios cascada
└─────────────────────────┘

DESPUÉS (Desacoplado):
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Presentación │  │   Dominio    │  │ Adaptadores  │
│  (main.py)   │  │  (negocio)   │  │ (externos)   │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                  │
       └────────────────►│◄─────────────────┘
          Usa       Implementan
       CasoDeUso    Puertos
       
✅ Bajo acoplamiento
✅ Fácil de testear
✅ Cambios localizados
```
