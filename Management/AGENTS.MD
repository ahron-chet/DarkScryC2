
# 🚀 FastAPI Management Backend Guidelines

This `Management` directory contains the FastAPI implementation intended to replace the legacy Django backend (django/ folder). As the migration is ongoing, ensure feature parity with the original functionality while adopting modern Python best practices. All new code should leverage asynchronous patterns, object-oriented design principles, and modular structures to enhance readability, maintainability, and ease of testing.

**Database models** should closely match the existing Django models. **Do not omit any columns** from the original schema unless explicitly documented and justified.

---

## 🛠️ Programming Style

**General Practices:**

* Use modern Python (version 3.10+ recommended).
* Embrace asynchronous (`async`) patterns consistently with FastAPI and SQLAlchemy or SQLModel.
* Prioritize object-oriented design principles:

  * Encapsulate business logic within classes or dedicated service modules.
  * Leverage FastAPI’s dependency injection (`Depends`) to clearly manage dependencies and separate concerns.
* **Implement class-based routing** following enterprise-grade FastAPI practices:

  * Define clear controller classes for endpoint logic.
  * Each resource/domain should have its own router, encapsulating related class-based endpoints.
  * Except for the `auth` router, configure each router with `dependencies=[Depends(get_current_user)]` so authentication is enforced globally on its routes.
  * Avoid mixing procedural and class-based endpoints within the same module.
* Organize code into modular directories clearly:

```
Management/app/
├── core/
├── models/
├── schemas/
├── routers/
├── controllers/
└── services/
```

* Place **CRUD operations** and business logic within clearly defined, domain-specific service classes:

  * Example: `services/users.py`
  * Avoid monolithic CRUD or service files.

---

## 📌 Database Model Guidelines

* Ensure all database models closely reflect the original Django models. **Do not omit columns** unless explicitly justified and documented.
* Maintain the same field names, data types, constraints, and relationships as defined originally.
* All time fields must be timezone-aware and stored in UTC.
* Clearly document any deliberate deviations and the reasoning behind them within your PR description.

---

## 📌 Pydantic Schema Best Practices

When creating API endpoints, all schemas must be explicitly defined, validated, and documented with **Pydantic**:

* **Explicit Validation**: Clearly enforce data types, formats, and constraints.
* **Field Descriptions**: Provide clear descriptions (`Field(...)`) for each schema field to clarify their purpose.
* **Comprehensive Documentation**: Schemas must be documented thoroughly, making API usage clear for frontend developers and other API consumers.
* **Consistency**: Use standardized naming conventions and schema structures consistently across the entire API.

---

## 🔐 Security & ⚡ Optimization

* Validate all user input explicitly with **Pydantic schemas** and FastAPI dependencies (`Depends`).
* Secure sensitive endpoints properly using authentication and permission checks.
* **Configurations and secrets** (JWT keys, database URIs, etc.) must be loaded securely via environment variables (`os.getenv`).
* Centralize environment configuration in a dedicated `settings.py` file, leveraging `Pydantic BaseSettings`.
* Optimize database queries proactively to avoid the N+1 problem using appropriate loading techniques (e.g., `.options(selectinload(...))`).
* Ensure asynchronous operations throughout the backend; avoid any synchronous database or I/O calls.

---

## 📚 Documentation & Permissions

* When creating a new API endpoint, thoroughly review equivalent functionality in the legacy Django application.
* Properly implement permissions, authentication, and business logic mirroring the original Django implementation.
* Document all API endpoints extensively using:

  * Clear and descriptive docstrings.
  * Well-defined Pydantic schemas.
  * Complete OpenAPI schema annotations (FastAPI automatically generates these).

---

## 📚 Package Management

Use **Poetry** for dependency management, strictly following Poetry's recommended best practices.

---

## 🧪 Testing Guidelines

* Every new feature or API endpoint **must include comprehensive tests**:

  * Place tests within `backend/tests/`.
  * Ensure tests cover both successful and edge/error scenarios.
  * Use the provided `TEST_DATABASE_URL` environment variable pointing to a dedicated PostgreSQL test database for running tests. **SQLite must never be used, even for tests.**

* Always run tests locally before committing code:

```bash
pytest -v Management/tests/
```

* If tests fail:

  * Fix the issues promptly, or
  * Clearly document and explain the failure in your PR description.

* Proactively address all pytest deprecation warnings. Do not ignore these warnings; fix them promptly unless there's a clearly justified reason not to.


---

## 🎨 Code Quality & Formatting

* Format code consistently using:

```bash
black .
isort .
```

* Use typing annotations clearly and consistently:

```python
def get_user(user_id: int) -> UserSchema:
    ...
```

* Avoid overly long files or methods; refactor complex logic into separate, clear modules and classes.
* Adhere to the naming conventions and detailed structural guidelines outlined in `docs/CONTRIBUTING.md`.

---

## ✅ PR Submission Checklist

Before submitting your pull request, verify that you have:

* [ ] Followed modern OOP, asynchronous programming, and FastAPI best practices.
* [ ] Implemented clear, modular, and well-documented class-based routing.
* [ ] Included comprehensive tests covering new features/endpoints.
* [ ] Successfully run all tests (`pytest`) without any failures or warnings.
* [ ] Formatted your code using `black` and `isort`.
* [ ] Ensured all sensitive logic and security considerations are handled appropriately.
* [ ] Verified your code uses efficient, asynchronous operations with no synchronous blocking calls.

---

## 📌 PR Message Format

Use the following clear PR template when submitting pull requests:

```markdown
### Summary
Briefly describe the changes made.

### Why
Explain the motivation behind these changes clearly.

### Tests
- [x] Added comprehensive tests for the new functionality
- [x] All tests passing successfully (`pytest`)

### Notes
- [Optional] Mention any dependencies, known issues, or future enhancements clearly.
```

---

**✅ Following these guidelines ensures our FastAPI backend aligns with enterprise-level standards, promoting consistency, maintainability, security, and scalability.**
