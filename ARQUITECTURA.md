# Arquitectura Hexagonal - Biometric Service

## Descripción

La aplicación ha sido refactorizada para implementar una **Arquitectura Hexagonal** (también conocida como Puertos y Adaptadores). Este patrón arquitectónico desacopla la lógica de negocio de las dependencias externas, facilitando testing, mantenibilidad y escalabilidad.

## Estructura del Proyecto

```
app/
├── domain/                    # Capa de Dominio (Lógica de negocio pura)
│   ├── models.py             # Modelos de dominio
│   ├── puertos.py            # Interfaces (puertos) que definen contratos
│   └── casos_uso.py          # Casos de uso (orquestadores de negocio)
│
├── adaptadores/              # Capa de Adaptadores (Implementaciones concretas)
│   ├── analizador_rostros.py # Adaptador InsightFace
│   ├── postgresql.py         # Adaptador PostgreSQL
│   └── sistema_archivos.py   # Adaptador Sistema de Archivos
│
├── infraestructura/          # Capa de Infraestructura
│   └── configuracion.py      # Inyección de dependencias
│
├── models/                   # DTOs (Data Transfer Objects)
│   └── schemas.py            # Esquemas FastAPI/Pydantic
│
└── main.py                   # API REST - Capa de presentación
```

## Capas de la Arquitectura

### 1. **Capa de Dominio** (`app/domain/`)

Contiene la **lógica de negocio pura** sin dependencias externas.

- **`models.py`**: Define entidades y modelos del dominio
  - `Embedding`: Representa un vector de embedding normalizado
  - `PersonaFoto`: Datos de una foto de persona
  - `PersonaEmbedding`: Embedding promedio de una persona
  - `VerificacionFacial`: Resultado de comparación facial

- **`puertos.py`**: Define interfaces (contratos) que los adaptadores deben implementar
  - `PuertoAnalizadorRostros`: Para análisis de imágenes
  - `PuertoAlmacenamientoFotos`: Para guardar fotos
  - `PuertoAlmacenamientoEmbeddings`: Para guardar embeddings
  - `PuertoSistemaArchivos`: Para gestión de archivos

- **`casos_uso.py`**: Implementa la lógica de negocio
  - `CasoDeUsoEnrollamiento`: Registrar persona con múltiples fotos
  - `CasoDeUsoVerificacion`: Verificar identidad
  - `CasoDeUsoValidacionVisita`: Validar visita

### 2. **Capa de Adaptadores** (`app/adaptadores/`)

Implementaciones concretas de los puertos definidos en el dominio.

- **`analizador_rostros.py`**: 
  - Implementa `PuertoAnalizadorRostros`
  - Usa InsightFace para análisis de rostros
  - Completamente desacoplado de la lógica de negocio

- **`postgresql.py`**:
  - Implementa `PuertoAlmacenamientoFotos` y `PuertoAlmacenamientoEmbeddings`
  - Usa SQLAlchemy para interacción con BD
  - Traduce modelos de dominio a/desde SQL

- **`sistema_archivos.py`**:
  - Implementa `PuertoSistemaArchivos`
  - Gestiona almacenamiento de imágenes
  - Soporta operaciones síncronas y asincrónicas

### 3. **Capa de Infraestructura** (`app/infraestructura/`)

Gestiona la inyección de dependencias y configuración.

- **`configuracion.py`**: `ConfiguradorAplicacion`
  - Crea instancias de adaptadores
  - Inyecta dependencias en casos de uso
  - Centraliza configuración desde variables de entorno

### 4. **Capa de Presentación** (`app/main.py`)

API REST que expone los casos de uso.

- Define endpoints HTTP
- Convierte requests/responses
- Maneja errores y logging
- Totalmente desacoplada de la lógica de negocio

## Beneficios de esta Arquitectura

### ✅ **Desacoplamiento**
- La lógica de negocio no depende de frameworks
- Los adaptadores pueden cambiar sin afectar el dominio

### ✅ **Testabilidad**
```python
# Fácil crear mocks de puertos para testing
class MockAnalizadorRostros(PuertoAnalizadorRostros):
    def obtener_embedding_desde_bytes(self, contenido: bytes) -> Embedding:
        return Embedding(vector=np.random.rand(512))
```

### ✅ **Extensibilidad**
- Agregar nuevo adaptador no requiere cambiar el dominio
- Ejemplo: Cambiar de InsightFace a otro modelo es solo crear un nuevo adaptador

### ✅ **Mantenibilidad**
- Código organizado y con responsabilidades claras
- Fácil entender qué hace cada componente

### ✅ **Independencia de Frameworks**
- Cambiar de FastAPI a Flask sin tocar lógica de negocio
- Cambiar de PostgreSQL a MongoDB solo requiere nuevo adaptador

## Flujo de Ejecución - Ejemplo: Enrollamiento

```
HTTP POST /enroll
    ↓
main.py (registrar_residente)
    ↓
ConfiguradorAplicacion
    ↓
CasoDeUsoEnrollamiento.ejecutar()  ← Lógica de negocio pura
    ├─ PuertoSistemaArchivos.guardar_imagen()
    │  └─ AdaptadorSistemaArchivosLocal
    │
    ├─ PuertoAnalizadorRostros.obtener_embedding_desde_bytes()
    │  └─ AdaptadorInsightFaceAnalyzer
    │
    ├─ PuertoAlmacenamientoFotos.guardar_foto()
    │  └─ AdaptadorPostgresFotos
    │
    └─ PuertoAlmacenamientoEmbeddings.guardar_embedding()
       └─ AdaptadorPostgresEmbeddings
    ↓
Respuesta HTTP
```

## Variables de Entorno

```bash
# Base de datos
DB_USER=admin
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=5432
DB_NAME=urbanizacion_db

# Verificación
VERIFICATION_THRESHOLD=0.6

# Archivos
UPLOADS_DIR=uploads
```

## Cómo Agregar un Nuevo Adaptador

**Ejemplo: Cambiar de InsightFace a Face Recognition**

1. Crear nuevo archivo: `app/adaptadores/face_recognition.py`

```python
from app.domain.puertos import PuertoAnalizadorRostros
from app.domain.models import Embedding, ErrorSinRostroDetectado
import face_recognition

class AdaptadorFaceRecognitionLib(PuertoAnalizadorRostros):
    def obtener_embedding_desde_bytes(self, contenido: bytes) -> Embedding:
        # Implementación con face_recognition
        pass
```

2. Actualizar `app/infraestructura/configuracion.py`:

```python
def crear_analizador_rostros(self) -> PuertoAnalizadorRostros:
    # return AdaptadorInsightFaceAnalyzer(...)  # Anterior
    return AdaptadorFaceRecognitionLib()  # Nuevo
```

3. ¡Listo! El resto del código no cambia.

## Testing

```python
# Test con mocks
def test_enrollamiento():
    mock_analizador = MockAnalizadorRostros()
    mock_fotos = MockAlmacenamientoFotos()
    mock_embeddings = MockAlmacenamientoEmbeddings()
    mock_archivos = MockSistemaArchivos()
    
    caso = CasoDeUsoEnrollamiento(
        mock_analizador,
        mock_fotos,
        mock_embeddings,
        mock_archivos
    )
    
    resultado = caso.ejecutar(1, "admin", [b"fake_image"])
    assert resultado["fotos_guardadas"] == 1
```

## Conclusión

Esta arquitectura hexagonal proporciona:
- **Separación clara de responsabilidades**
- **Independencia de tecnología**
- **Fácil testing**
- **Escalabilidad y mantenibilidad**
- **Flexibilidad para cambios futuros**
