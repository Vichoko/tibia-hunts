# Flujo de Trabajo con Pull Requests

Este proyecto utiliza pull requests para todos los cambios a la rama `main`.

## Proceso de Desarrollo

### 1. Crear una nueva rama
```bash
git checkout -b feat/nombre-de-la-funcionalidad
# o
git checkout -b fix/descripcion-del-bug
```

### 2. Realizar cambios y commits
```bash
git add .
git commit -m "feat: agregar nueva funcionalidad"
```

Usar conventional commits:
- `feat:` - Nueva funcionalidad
- `fix:` - Corrección de bugs
- `docs:` - Cambios en documentación
- `style:` - Cambios de formato (no afectan funcionalidad)
- `refactor:` - Refactoring de código
- `test:` - Agregar o modificar tests
- `chore:` - Tareas de mantenimiento

### 3. Hacer push de la rama
```bash
git push origin feat/nombre-de-la-funcionalidad
```

### 4. Crear Pull Request
- Ir a GitHub y crear un PR desde tu rama hacia `main`
- Completar el template de PR con toda la información necesaria
- Asegurarse de que todos los checks pasen

## Checks Automáticos

Cada PR ejecuta automáticamente:

### Code Quality Check
- ✅ Ruff linter (`ruff check .`)
- ✅ Ruff formatter (`ruff format --check .`)
- ✅ Django system check (`python src/manage.py check`)
- ✅ Django deployment check (`python src/manage.py check --deploy`)

### Django Tests  
- ✅ Check de migraciones (`makemigrations --check`)
- ✅ Tests de Django (`python src/manage.py test`)
- ✅ Verificación de migraciones faltantes

## Requisitos para Merge

Todos los checks deben pasar antes de hacer merge:
- ✅ Code Quality Check exitoso
- ✅ Django Tests exitoso
- ✅ Review aprobado (si es requerido)

## Semantic Release

Una vez que el PR se mergea a `main`:
- 🚀 Semantic-release ejecuta automáticamente
- 📝 Genera CHANGELOG.md automáticamente
- 🏷️ Crea tags de versión automáticamente
- 📦 Actualiza la versión en `pyproject.toml`

## Comandos Útiles para Desarrollo Local

```bash
# Verificar calidad de código
poetry run ruff check .
poetry run ruff format --check .

# Verificar Django
poetry run python src/manage.py check
poetry run python src/manage.py check --deploy

# Ejecutar tests
poetry run python src/manage.py test

# Aplicar autofix de Ruff
poetry run ruff check . --fix
poetry run ruff format .
```
