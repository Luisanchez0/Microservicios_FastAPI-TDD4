# Microservicios - Usuarios y Órdenes

Arquitecut*ura de microservicios con Hexagonal Architecture, usando MySQL para usuarios y PostgreSQL para órdenes, **con comunicación asíncrona vía RabbitMQ**.

## 📋 Estructura del Proyecto

```
src/
├── core/                           # Configuración
│   └── config.py                  # Settings para ambos servicios + RabbitMQ
├── domain/                         # Lógica de negocio (Entidades)
│   ├── user.py                    # Modelo User
│   ├── order.py                   # Modelo Order
│   └── events.py                  # Eventos de dominio
├── application/                    # Casos de uso
│   ├── ports/                     # Interfaces (contratos)
│   │   ├── user_repository.py     # Puerto para usuarios
│   │   └── order_repository.py    # Puerto para órdenes
│   └── services/                  # Servicios de aplicación
│       ├── user_services.py       # Lógica de usuarios + eventos
│       └── order_service.py       # Lógica de órdenes + eventos
├── infrastructure/                 # Implementaciones técnicas
│   ├── database/                  # Conexiones a BD
│   │   ├── user_database.py       # MySQL setup
│   │   ├── order_database.py      # PostgreSQL setup
│   │   ├── user_models.py         # ORM models (MySQL)
│   │   └── order_models.py        # ORM models (PostgreSQL)
│   ├── messaging/                 # Sistema de mensajería
│   │   ├── rabbitmq_client.py     # Cliente RabbitMQ sync/async
│   │   ├── user_event_publisher.py    # Publicador eventos usuarios
│   │   ├── order_event_publisher.py   # Publicador eventos órdenes
│   │   ├── user_event_consumer.py     # Consumidor eventos usuarios
│   │   └── order_event_consumer.py    # Consumidor eventos órdenes
│   ├── adapters/                  # Implementaciones de puertos
│   │   ├── sqlalchemy_user_repository.py      # MySQL adapter
│   │   ├── sqlalchemy_order_repository.py     # PostgreSQL adapter
│   │   ├── in_memory_user_repository.py       # En memoria (legacy)
│   │   └── in_memory_order_repository.py      # En memoria (legacy)
│   └── api/                       # Rutas FastAPI
│       ├── user_routes.py         # Endpoints usuarios
│       └── order_routes.py        # Endpoints órdenes
├── users_main.py                  # App de usuarios (puerto 8001) + consumidores
├── orders_main.py                 # App de órdenes (puerto 8002) + consumidores
├── main.py                        # App combinada (puerto 8000)
└── scripts/                       # Scripts de inicialización
    ├── create_tables.py          # Crear tablas BD
    └── init_rabbitmq.py          # Inicializar RabbitMQ
```

## 🚀 Instalación y Configuración

### 1. Clonar/Descargar el proyecto
```bash
cd Proyect_Micros
```

### 2. Crear base de datos MySQL (Usuarios)
```sql
CREATE DATABASE users CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. Crear base de datos PostgreSQL (Órdenes)
```bash
createdb -U postgres -E UTF8 orders
```

### 4. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 5. Configurar variables de entorno
```bash
cp .env.example .env
# Editar .env con tus credenciales de base de datos si es necesario
```

### 6. Crear las tablas en las bases de datos
```bash
python src/scripts/create_tables.py
```

### 7. Instalar y configurar RabbitMQ
```bash
# Instalar RabbitMQ (Ubuntu/Debian)
sudo apt update
sudo apt install rabbitmq-server
sudo systemctl start rabbitmq-server
sudo systemctl enable rabbitmq-server

# O usando Docker
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management

# Verificar que esté corriendo
sudo systemctl status rabbitmq-server
```

### 8. Inicializar RabbitMQ (exchanges y queues)
```bash
python src/scripts/init_rabbitmq.py
```

## 🏃 Ejecutar los servicios

### Opción 1: Ejecutar servicios de forma separada

**Terminal 1 - Microservicio de Usuarios (Puerto 8001)**
```bash
python -m uvicorn src.users_main:app --reload --port 8001 --host 0.0.0.0
```

**Terminal 2 - Microservicio de Órdenes (Puerto 8002)**
```bash
python -m uvicorn src.orders_main:app --reload --port 8002 --host 0.0.0.0
```

### Opción 2: Ejecutar aplicación combinada (Puerto 8000)
```bash
python -m uvicorn src.main:app --reload --port 8000 --host 0.0.0.0
```

## 📚 API Endpoints

### Usuarios (Puerto 8001 o combinado 8000)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/users/` | Crear usuario |
| GET | `/api/users/` | Listar todos los usuarios |
| GET | `/api/users/active` | Listar usuarios activos |
| GET | `/api/users/{user_id}` | Obtener usuario por ID |
| PUT | `/api/users/{user_id}` | Actualizar usuario |
| DELETE | `/api/users/{user_id}` | Eliminar usuario |
| POST | `/api/users/{user_id}/activate` | Activar usuario |
| POST | `/api/users/{user_id}/deactivate` | Desactivar usuario |

### Órdenes (Puerto 8002 o combinado 8000)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/orders/` | Crear orden |
| GET | `/api/orders/` | Listar todas las órdenes |
| GET | `/api/orders/{order_id}` | Obtener orden por ID |
| GET | `/api/orders/user/{user_id}` | Listar órdenes de un usuario |
| GET | `/api/orders/{order_id}/total` | Calcular total de orden |
| PUT | `/api/orders/{order_id}` | Actualizar orden |
| DELETE | `/api/orders/{order_id}` | Eliminar orden |
| POST | `/api/orders/{order_id}/send` | Marcar como enviada |
| POST | `/api/orders/{order_id}/deliver` | Marcar como entregada |
| POST | `/api/orders/{order_id}/cancel` | Cancelar orden |

## 📨 Sistema de Mensajería (RabbitMQ)

### Arquitectura de Eventos

Los microservicios se comunican de forma asíncrona mediante eventos publicados en RabbitMQ:

#### Exchanges y Routing Keys
- **`user.events`** - Eventos de usuarios
  - `user.created` - Usuario creado
  - `user.updated` - Usuario actualizado
  - `user.deleted` - Usuario eliminado

- **`order.events`** - Eventos de órdenes
  - `order.created` - Orden creada
  - `order.updated` - Orden actualizada
  - `order.deleted` - Orden eliminada

#### Flujo de Comunicación

1. **Usuario crea una orden** → Servicio de Órdenes valida usuario vía cache de eventos
2. **Usuario se crea/actualiza** → Evento se publica y es consumido por Servicio de Órdenes
3. **Orden se crea** → Evento se publica y es consumido por Servicio de Usuarios (estadísticas)

#### Beneficios
- ✅ **Desacoplamiento** - Servicios no dependen directamente
- ✅ **Escalabilidad** - Procesamiento asíncrono
- ✅ **Resiliencia** - Fallos en un servicio no afectan otros
- ✅ **Consistencia eventual** - Datos sincronizados vía eventos
## 📖 Documentación interactiva

Una vez que el servidor esté en ejecución, accede a:

- **Swagger UI**: http://localhost:8001/docs (usuarios) o http://localhost:8002/docs (órdenes)
- **ReDoc**: http://localhost:8001/redoc (usuarios) o http://localhost:8002/redoc (órdenes)

## 🗄️ Esquemas de Base de Datos

### MySQL - Tabla `users`
```sql
CREATE TABLE users (
    id CHAR(36) NOT NULL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    status ENUM('ACTIVE', 'INACTIVE', 'SUSPENDED') NOT NULL DEFAULT 'ACTIVE',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

### PostgreSQL - Tabla `orders`
```sql
CREATE TYPE order_status AS ENUM (
    'PENDING',
    'SENT',
    'DELIVERED',
    'CANCELLED'
);

CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_usuario UUID NOT NULL,
    producto VARCHAR(255) NOT NULL,
    cantidad INTEGER NOT NULL CHECK (cantidad > 0),
    precio NUMERIC(10,2) NOT NULL CHECK (precio >= 0),
    status order_status NOT NULL DEFAULT 'PENDING',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER trigger_update_orders_updated_at
BEFORE UPDATE ON orders
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();
```

## 🧪 Probar Comunicación entre Servicios

Ejecuta el script de prueba para verificar que RabbitMQ funcione correctamente:

```bash
python src/scripts/test_messaging.py
```

Este script:
1. ✅ Verifica que los servicios estén corriendo
2. ✅ Crea un usuario (publica evento `user.created`)
3. ✅ Crea una orden (valida usuario vía cache de eventos)
4. ✅ Actualiza el usuario (publica evento `user.updated`)
5. ✅ Envía la orden (publica evento `order.updated`)

## 💡 Ejemplos de uso

### Crear un usuario
```bash
curl -X POST "http://localhost:8001/api/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "juan",
    "email": "juan@example.com",
    "password": "contraseña123"
  }'
```

### Crear una orden
```bash
curl -X POST "http://localhost:8002/api/orders/" \
  -H "Content-Type: application/json" \
  -d '{
    "id_usuario": "550e8400-e29b-41d4-a716-446655440000",
    "producto": "Laptop",
    "cantidad": 1,
    "precio": 1200.00
  }'
```

## 🏗️ Arquitectura

El proyecto sigue los principios de **Hexagonal Architecture** (Puertos y Adaptadores):

- **Domain**: Contiene la lógica de negocio pura, independiente de cualquier framework
- **Application**: Define los casos de uso y contratos (puertos)
- **Infrastructure**: Implementa los detalles técnicos (adaptadores a bases de datos)
- **API**: Expone los endpoints REST

Esta arquitectura permite:
- ✅ Cambiar fácilmente entre diferentes bases de datos
- ✅ Testear la lógica de negocio sin dependencias externas
- ✅ Mantener el código limpio y organizado

## 📝 Problemas comunes

### Error: "No module named 'pymysql'"
```bash
pip install pymysql
```

### Error: "psycopg2 not found"
```bash
pip install psycopg2-binary
```

### Error: "pika not found" o "aio-pika not found"
```bash
pip install pika aio-pika
```

### Error: "Conexión rechazada a MySQL"
- Verificar que MySQL está corriendo: `sudo systemctl start mysql`
- Verificar credenciales en `.env`

### Error: "Conexión rechazada a PostgreSQL"
- Verificar que PostgreSQL está corriendo: `sudo systemctl start postgresql`
- Verificar credenciales en `.env`

### Error: "Connection to RabbitMQ failed"
- Verificar que RabbitMQ está corriendo: `sudo systemctl status rabbitmq-server`
- Verificar Management UI: http://localhost:15672 (guest/guest)
- Verificar configuración en `.env` (host, port, credentials)

### Error: "Eventos no se propagan entre servicios"
- Asegurarse de que `init_rabbitmq.py` se ejecutó correctamente
- Verificar que los consumidores están corriendo (logs de las aplicaciones)
- Revisar que las queues se crearon: `rabbitmqctl list_queues`

### Error: "Usuario no existe o no está activo" al crear orden
- Los eventos de usuario pueden no haber llegado aún (consistencia eventual)
- Esperar unos segundos y reintentar
- Verificar que el servicio de usuarios esté publicando eventos

## 🐳 Despliegue con Docker (Opcional)

Para un despliegue completo con Docker:

```bash
# Levantar todos los servicios
docker-compose up -d

# Verificar que estén corriendo
docker-compose ps

# Ver logs
docker-compose logs -f
```

### Servicios incluidos:
- **RabbitMQ**: Puerto 5672 (AMQP), 15672 (Management UI)
- **MySQL**: Puerto 3306
- **PostgreSQL**: Puerto 5432

### Acceder a las interfaces:
- **RabbitMQ Management**: http://localhost:15672 (guest/guest)
- **MySQL**: `mysql -h localhost -P 3306 -u app -papp123 users`
- **PostgreSQL**: `psql -h localhost -p 5432 -U postgres orders`

### Limpiar contenedores:
```bash
docker-compose down -v  # Elimina contenedores y volúmenes
```

## 🤝 Contribuciones

Este es un proyecto de aprendizaje. Siéntete libre de modificar y mejorar.

## 📄 Licencia

Proyecto educativo - UNACH
