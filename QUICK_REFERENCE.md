# ⚡ Quick Reference - Datos Técnicos Clave
## Tarjeta de referencia rápida para memorizar

---

## 🔢 Números Clave

| Métrica | Valor | Descripción |
|---------|-------|-------------|
| **Precisión LFW** | 99.8% | Benchmark estándar |
| **Embeddings** | 512D | Dimensionalidad |
| **Latencia Enrol** | 3s | 3 imágenes |
| **Latencia Verify** | 1.2s | 1 imagen |
| **Latencia Validate** | 2s | 2 imágenes |
| **Umbral** | 0.6 | Distancia coseno |
| **FAR** | 0.1% | Falsos positivos |
| **TAR** | 98.5% | Verdaderos positivos |
| **Throughput Max** | 2-3 req/s | CPU 8-core |
| **Memoria RAM** | 600MB | Operación típica |

---

## 🏗️ Arquitectura

```
FastAPI Endpoints
    ↓
Domain Logic (Puro)
    ↓
Puertos (Interfaces)
    ↓
Adaptadores
├─ InsightFace
├─ PostgreSQL
└─ FileSystem
```

**Patrón:** Hexagonal (Puertos y Adaptadores)

---

## 🛠️ Stack Mínimo Criticar

| Layer | Herramienta | Versión |
|-------|------------|---------|
| API | FastAPI | 0.128.0 |
| IA | InsightFace | 0.7.3 |
| DB | PostgreSQL | 14+ |
| Runtime | ONNX Runtime | 1.23.2 |
| Server | Uvicorn | 0.40.0 |
| ORM | SQLAlchemy | 2.0.45 |

---

## 📊 Operaciones Principales

### Enrollamiento (3 fases)
```
Individual:  Extracción embedding de cada foto (800ms x 3)
Agregación:  Cálculo embedding promedio + normalización
Persistencia: Guardar 3 fotos + 1 embedding promedio
Total: 2.7-3.5s
```

### Verificación (3 fases)
```
Extracción:  Embedding de imagen de verificación (800ms)
Recuperación: Embedding promedio almacenado (50ms)
Comparación: Distancia coseno vs umbral (5ms)
Total: 0.9-1.2s
```

### Validación (2 fases)
```
Dual:        Embedding de cédula + rostro vivo (1600ms)
Comparación: Distancia coseno vs umbral (5ms)
Total: 1.7-2.2s
```

---

## 🧮 Fórmulas Matemáticas

### Normalización L2
```
v_norm = v / ||v||
donde ||v|| = sqrt(sum(v_i²))
```

### Distancia Coseno
```
distance = 1 - (v1·v2 / (||v1|| * ||v2||))
```

### Embedding Promedio
```
promedio = mean([e1, e2, e3])
promedio_norm = promedio / ||promedio||
```

---

## 🎯 Casos de Uso

| Endpoint | Método | Entrada | Salida | Umbral |
|----------|--------|---------|--------|--------|
| `/enroll` | POST | 3+ imgs | Confirmación | N/A |
| `/verify` | POST | ID + img | Match + dist | 0.6 |
| `/validate` | POST | 2 imgs | Match + dist | 0.6 |
| `/health` | GET | Nada | Status | N/A |

---

## 📈 Decisiones Justificadas

| Decisión | Alternativa | ¿Por qué elegimos? |
|----------|-------------|-------------------|
| **InsightFace** | Face Rec | 99.8% vs 99.6%, 512D vs 128D |
| **FastAPI** | Flask | 180k vs 35k req/s, async nativo |
| **PostgreSQL** | Pinecone | ACID, costo bajo, SQL estándar |
| **ONNX** | TensorFlow | CPU optimizado, portabilidad |
| **Hexagonal** | MVC | Desacoplamiento máximo, testeable |

---

## 🔑 Conceptos Clave

**Embedding:** Vector 512D que representa características faciales únicas  
**Normalización:** Proceso que garantiza magnitud 1.0 en esfera unitaria  
**Distancia Coseno:** Métrica de similitud entre 0 (idéntico) y 1 (opuesto)  
**Umbral:** Valor límite (0.6) que determina si es match o no  
**PostgreSQL:** Base de datos relacional ACID  
**ONNX:** Formato estándar abierto para modelos de redes neuronales  
**Hexagonal:** Arquitectura que separa dominio de dependencias externas  

---

## ⚠️ Limitaciones Conocidas

- ❌ Solo rostros frontales
- ❌ Requiere iluminación adecuada
- ❌ Sensible a calidad de imagen
- ❌ Escalabilidad BD ~10M vectores
- ❌ Latencia 1-2s (no real-time)
- ⚠️ Requiere CUDA/TensorFlow para GPU

---

## ✅ Fortalezas

- ✅ 99.8% precisión (SOTA)
- ✅ CPU portable
- ✅ Código limpio (SOLID)
- ✅ Architecture modern
- ✅ Documentación exhaustiva
- ✅ APIs REST estándar
- ✅ Docker-ready

---

## 📖 Documentos por Tamaño

| Doc | Páginas | Lectura |
|-----|---------|---------|
| RESUMEN_EJECUTIVO | 3 | 10 min |
| README | 5 | 10 min |
| API_DOCUMENTATION | 15 | 15 min |
| ARQUITECTURA | 15 | 20 min |
| REVISION_TECNICA | 30 | 45 min |
| ANALISIS_COMPARATIVO | 25 | 45 min |

---

## 🎓 Preguntas Tribunal Más Comunes

**Q: ¿Por qué elegiste esta arquitectura?**  
A: Desacoplamiento máximo, testabilidad, industria valida

**Q: ¿Cómo funciona el reconocimiento facial?**  
A: Extrae embedding 512D normalizado, compara con distancia coseno

**Q: ¿Por qué no GPU?**  
A: CPU portable, costo bajo, suficiente para verificación

**Q: ¿Cuál es la precisión?**  
A: 99.8% en LFW, 98.5% TAR, 0.1% FAR

**Q: ¿Cómo escalas esto?**  
A: Instancias múltiples + load balancer, BD replica

---

## 🚀 Deploy Checklist

- [ ] Variables de entorno (.env)
- [ ] PostgreSQL
- [ ] Tablas creadas (DDL)
- [ ] Permisos DB correctos
- [ ] `pip install -r requirements.txt`
- [ ] `uvicorn app.main:app`
- [ ] Probar endpoints
- [ ] Docker build & run
- [ ] Monitoreo (logs)
- [ ] Backup de BD

---

## 💾 Estructura Carpetas

```
app/
├── domain/              # Lógica (sin frameworks)
│   ├── models.py       # Entidades
│   ├── puertos.py      # Interfaces
│   └── casos_uso.py    # Casos
├── adaptadores/        # Implementaciones
│   ├── analizador_rostros.py
│   ├── postgresql.py
│   └── sistema_archivos.py
├── infraestructura/    # DI
│   └── configuracion.py
├── models/             # DTOs
│   └── schemas.py
└── main.py             # Endpoints
```

---

## 🔍 Debugging Tips

| Problema | Causa | Solución |
|----------|-------|----------|
| No detecta rostro | Imagen oscura/borrosa | Mejorar iluminación |
| Conexión BD falla | URL incorrecta | Ver .env |
| ONNX error | Versión incompatible | Reinstalar onnxruntime |
| Memoria insuficiente | Demasiados requests | Aumentar workers |

---

## 📚 Referencias Académicas Clave

1. **ArcFace** (Deng et al., 2018) - Base teórica InsightFace
2. **FaceNet** (Schroff et al., 2015) - Embeddings métricos
3. **DeepFace** (Taigman et al., 2014) - Deep learning FR

---

## 🎯 Para Memoria (Memorizar)

**Números:**
- 99.8% (precisión)
- 512 (dimensiones)
- 0.6 (umbral)
- 800ms (latencia por imagen)

**Tecnologías:**
- InsightFace (IA)
- FastAPI (Web)
- PostgreSQL (BD)
- Hexagonal (Arquitectura)

**Conceptos:**
- Embedding normalizado
- Distancia coseno
- Arquitectura hexagonal
- Inyección de dependencias

---

**Generado:** Enero 27, 2026  
**Propósito:** Quick reference  
**Audiencia:** Presentación rápida

✅ **Imprimible en 2 páginas**
