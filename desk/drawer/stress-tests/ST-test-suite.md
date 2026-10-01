# ST-test-suite: Test suite health and developer experience

**Basado en:** UC-01, UC-02, UC-03, UC-06

## Script

```bash
# 1. List all test files
ls tests/*.py
echo "Exit: $?"

# 2. Run full test suite with verbose output
python -m pytest tests/ -v --tb=short 2>&1
echo "Exit: $?"

# 3. Run tests with warnings (check for deprecation warnings)
python -m pytest tests/ -v --tb=short -W all 2>&1 | grep -E "warning|Warning|deprecated|Deprecation" | head -10 || echo "No warnings"
echo "Exit: $?"

# 4. Run a specific test file: test_models
python -m pytest tests/test_models.py -v 2>&1
echo "Exit: $?"

# 5. Run a specific test file: test_solver_graph
python -m pytest tests/test_solver_graph.py -v 2>&1
echo "Exit: $?"

# 6. Run a specific test file: test_handlers
python -m pytest tests/test_handlers.py -v 2>&1
echo "Exit: $?"

# 7. Check test coverage (if pytest-cov is installed)
python -m pytest tests/ --cov=repopackage --cov-report=term 2>&1 | tail -30
echo "Exit: $?"

# 8. Check conftest.py fixtures
cat tests/conftest.py | head -60
echo "Exit: $?"

# 9. Run tests with xdist (parallel) if installed
python -m pytest tests/ -n auto -v --tb=short 2>&1 | tail -20
echo "Exit: $?"

# 10. Test discovery: which tests are async?
grep -rn "async def" tests/ --include="*.py" || echo "No async tests"

# 11. Test isolation: does running individual tests change global state?
python -m pytest tests/test_models.py tests/test_solver_graph.py -v --tb=short 2>&1
echo "Exit: $?"

# 12. Check pytest configuration in pyproject.toml
grep -A 10 "\[tool.pytest" pyproject.toml
echo "Exit: $?"
```

## Puntos de estrés

| Paso | Qué observar |
|------|-------------|
| 1 | ¿Tests están organizados? |
| 2 | ¿Suite completa pasa? (1 known failure expected — RP-30) |
| 3 | ¿Deprecation warnings? |
| 4 | ¿Model tests aislados? |
| 5 | ¿Solver tests aislados? |
| 6 | ¿Handler tests aislados? |
| 7 | ¿Test coverage reporteable? |
| 8 | ¿Fixtures compartidas en conftest.py? |
| 9 | ¿Tests soportan paralelización? |
| 10 | ¿Tests async? |
| 11 | ¿Tests son aislados (no state leaking)? |
| 12 | ¿Config de pytest completa? |

## Modos de fracaso

- Suite no pasa completamente (test failures)
- Tests no aislados (orden de ejecución importa)
- Sin cobertura de tests (no hay métrica)
- Fixtures compartidas causan side effects entre tests
- Tests lentos (sin markers de slow/integration)
- No hay tests para edge cases
- Config de pytest incompleta (no hay testpaths, asyncio_mode, etc.)
