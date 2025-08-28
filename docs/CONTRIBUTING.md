# Pull Request Workflow

This project uses pull requests for all changes to the `main` branch.

## Development Process

### 1. Create a new branch
```bash
git checkout -b feat/feature-name
# or
git checkout -b fix/bug-description
```

### 2. Make changes and commits
```bash
git add .
git commit -m "feat: add new functionality"
```

Use conventional commits:
- `feat:` - New functionality
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `style:` - Formatting changes (don't affect functionality)
- `refactor:` - Code refactoring
- `test:` - Add or modify tests
- `chore:` - Maintenance tasks

### 3. Push the branch
```bash
git push origin feat/feature-name
```

### 4. Create Pull Request
- Go to GitHub and create a PR from your branch to `main`
- **IMPORTANT**: The PR title must follow the conventional commits format
- Complete the PR template with all necessary information
- Ensure all checks pass

## PR Title Format

Pull Request titles **MUST** follow the conventional commits format for semantic-release to work correctly:

### **Required format:**
```
type(scope): description
```

### **Valid types:**
- `feat` - New functionality
- `fix` - Bug fixes  
- `docs` - Documentation
- `style` - Code formatting/style
- `refactor` - Refactoring
- `perf` - Performance improvements
- `test` - Tests
- `build` - Build system
- `ci` - CI/CD
- `chore` - Maintenance tasks
- `revert` - Revert changes

### **Examples of valid titles:**
- ✅ `feat: add user authentication system`
- ✅ `fix(auth): resolve login redirect issue` 
- ✅ `docs: update API documentation`
- ✅ `chore(deps): update dependencies to latest versions`
- ✅ `perf: optimize database queries for hunt search`

### **Examples of INVALID titles:**
- ❌ `Add user authentication` (no type)
- ❌ `feat: Add user authentication` (description starts with uppercase)
- ❌ `update docs` (no type, description too short)

### **Additional rules:**
- Description must start with lowercase
- Minimum length: 10 characters
- Maximum length: 120 characters
- Scope is optional but recommended

### **Automatic validation:**
If the title doesn't meet the format, the PR will be blocked and you'll receive an automatic comment with instructions to fix it.

## Automatic Checks

Each PR automatically runs:

### Code Quality Check
- ✅ Ruff linter (`ruff check .`)
- ✅ Ruff formatter (`ruff format --check .`)
- ✅ Django system check (`python src/manage.py check`)

### Django Tests  
- ✅ Migration checks (`makemigrations --check`)
- ✅ Django tests (`python src/manage.py test`)
- ✅ Missing migrations verification

### PR Title Validation
- ✅ Conventional commits format
- ✅ Valid commit types
- ✅ Appropriate title length

## Requirements for Merge

All checks must pass before merging:
- ✅ Code Quality Check successful
- ✅ Django Tests successful
- ✅ PR Title Validation successful
- ✅ Review approved (if required)

## Semantic Release

Once the PR is merged to `main`:
- 🚀 Semantic-release runs automatically based on PR title
- 📝 Generates CHANGELOG.md automatically
- 🏷️ Creates version tags automatically
- 📦 Updates version in `pyproject.toml`

## Useful Commands for Local Development

```bash
# Check code quality
poetry run ruff check .
poetry run ruff format --check .

# Check Django
poetry run python src/manage.py check

# Run tests
poetry run python src/manage.py test

# Apply Ruff autofix
poetry run ruff check . --fix
poetry run ruff format .
```
