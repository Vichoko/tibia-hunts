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
- **IMPORTANTE**: El título del PR debe seguir el formato conventional commits
- Completar el template de PR con toda la información necesaria
- Asegurarse de que todos los checks pasen

## Formato de Títulos de PR

Los títulos de Pull Request **DEBEN** seguir el formato conventional commits para que semantic-release funcione correctamente:

### **Formato requerido:**
```
type(scope): description
```

### **Tipos válidos:**
- `feat` - Nueva funcionalidad
- `fix` - Corrección de bugs  
- `docs` - Documentación
- `style` - Formato/estilo de código
- `refactor` - Refactoring
- `perf` - Mejoras de performance
- `test` - Tests
- `build` - Sistema de build
- `ci` - CI/CD
- `chore` - Tareas de mantenimiento
- `revert` - Revertir cambios

### **Ejemplos de títulos válidos:**
- ✅ `feat: add user authentication system`
- ✅ `fix(auth): resolve login redirect issue` 
- ✅ `docs: update API documentation`
- ✅ `chore(deps): update dependencies to latest versions`
- ✅ `perf: optimize database queries for hunt search`

### **Ejemplos de títulos NO válidos:**
- ❌ `Add user authentication` (no type)
- ❌ `feat: Add user authentication` (descripción empieza con mayúscula)
- ❌ `update docs` (no type, descripción muy corta)

### **Reglas adicionales:**
- La descripción debe empezar con minúscula
- Longitud mínima: 10 caracteres
- Longitud máxima: 120 caracteres
- El scope es opcional pero recomendado

### **Validación automática:**
Si el título no cumple el formato, el PR será bloqueado y recibirás un comentario automático con instrucciones para corregirlo.

## Checks Automáticos

Cada PR ejecuta automáticamente:

### Code Quality Check
- ✅ Ruff linter (`ruff check .`)
- ✅ Ruff formatter (`ruff format --check .`)
- ✅ Django system check (`python src/manage.py check`)

### Django Tests  
- ✅ Check de migraciones (`makemigrations --check`)
- ✅ Tests de Django (`python src/manage.py test`)
- ✅ Verificación de migraciones faltantes

### PR Title Validation
- ✅ Formato conventional commits
- ✅ Tipos válidos de commit
- ✅ Longitud apropiada del título

## Requisitos para Merge

Todos los checks deben pasar antes de hacer merge:
- ✅ Code Quality Check exitoso
- ✅ Django Tests exitoso
- ✅ PR Title Validation exitoso
- ✅ Review aprobado (si es requerido)

## Semantic Release

Una vez que el PR se mergea a `main`:
- 🚀 Semantic-release ejecuta automáticamente basado en el título del PR
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

# Ejecutar tests
poetry run python src/manage.py test

# Aplicar autofix de Ruff
poetry run ruff check . --fix
poetry run ruff format .
```
