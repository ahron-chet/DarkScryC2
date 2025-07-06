# 🚀 FastAPI Management Backend Guidelines

This `Management` directory contains the FastAPI implementation intended to replace the legacy Django backend. As the migration is ongoing, ensure feature parity with the original functionality while adopting modern Python best practices. All new code should leverage asynchronous patterns, object-oriented design principles, and modular structures to enhance readability, maintainability, and ease of testing.

DB Models should be very like the django part please do not omit columns from the old django
---

## 🛠️ Programming Style

**General Practices:**

* Use modern Python (version 3.10+ recommended).
* Embrace asynchronous (`async`) patterns with FastAPI and SQLAlchemy or SQLModel.
* Prioritize object-oriented design principles:

  * Encapsulate business logic within classes or services rather than procedural code.
  * Use FastAPI's dependency injection (`Depends`) to manage and isolate concerns.
  * Use Class based route following fastapi best practices.
* Organize code into clear and modular directories:

  ```
  Management/app/
  ├── core/
  ├── models/
  ├── schemas/
  ├── routers/
  └── services/
  ```
* **CRUD operations** must reside in domain-specific service modules:

  * Example: `services/users.py`
  * Avoid single monolithic CRUD files.

---

## 📌 Database Model Guidelines

Ensure all database models closely reflect the original Django models. **Do not omit any columns** present in the legacy Django project. Any changes or additions to the existing structure must be explicitly justified and documented.

* Maintain field names, data types, constraints, and relationships from the original Django definitions.
* Clearly document any deliberate deviations and the reasoning behind them within your PR description.

---


## 📌 **Guidelines for Pydantic Schema Best Practices**

When developing and exporting APIs, ensure that **all schemas are clearly defined and documented using Pydantic**. Specifically:

* **Field validation**: Always validate data types and constraints explicitly.
* **Field descriptions**: Provide descriptive metadata (`Field(...)`) for each schema field to clarify intent and usage.
* **Clear documentation**: Schemas should be documented thoroughly, making API interactions transparent and easily understood by frontend and API consumers.
* **Consistency**: Maintain consistency across schemas by using standardized naming conventions and structures.


## 🔐 Security & ⚡ Optimization

* Validate all user input with **Pydantic schemas** or dependencies (`Depends`).
* Secure sensitive endpoints with proper authentication and permission checks.
* **All configurations and secrets** (e.g., JWT keys, database URIs) must be loaded via environment variables using `os.getenv`.
* Centralize all environment settings within a dedicated `settings.py` file leveraging `Pydantic BaseSettings`.
* Optimize database queries; avoid the N+1 problem by using appropriate SQLAlchemy loading techniques (e.g., `.options(selectinload(...))`).
* Maintain consistent asynchronous operations; avoid blocking calls.

---

## 📚 Documentation & Permissions

* When creating a new API endpoint, thoroughly review the equivalent functionality in the legacy Django project.
* Ensure proper implementation of permissions, authentication, and other crucial logic from the original Django backend.
* Document all API endpoints extensively using:

  * Clear docstrings
  * Pydantic schemas
  * OpenAPI schema annotations

---
Here's a clearer, improved version of your text:

---

## 📚 Package Management

Use **Poetry** for dependency management, following Poetry's recommended best practices.

## 🧪 Testing Guidelines

* Every new feature or API endpoint **must include tests**:

  * Place all tests within `backend/tests/`.
  * Ensure your tests cover both success cases and edge/error scenarios.

TEST_DATABASE_URL from envirnment variable will give you a url to postgres database use it for you tests

* Run tests locally before committing:

  ```bash
  pytest -v backend/tests/
  ```
* If tests fail, either:

  * Fix the issue immediately, or
  * Clearly document and explain the failure in your PR description.
* Always address pytest deprecation warnings proactively.

---

## 🎨 Code Quality & Formatting

* Format your code consistently using:

  ```bash
  black .
  isort .
  ```
* Follow typing best practices:

  ```python
  def get_user(user_id: int) -> UserSchema:
      ...
  ```
* Avoid overly long files and functions; split logic clearly across modules and methods.
* Refer to naming conventions and detailed structure guidelines defined in `docs/CONTRIBUTING.md`.

---

## ✅ PR Submission Checklist

Before submitting your pull request, verify that you have:

* [ ] Followed modern OOP and FastAPI best practices.
* [ ] Added comprehensive tests for all new features/endpoints.
* [ ] Successfully run all tests (`pytest`) without failures or warnings.
* [ ] Formatted your code using `black` and `isort`.
* [ ] Handled sensitive logic and security appropriately.
* [ ] Ensured efficient, non-blocking code (no synchronous database calls).

---

## 📌 PR Message Format

Use the following PR template for clarity:

```markdown
### Summary
Briefly describe the changes made.

### Why
Explain the motivation behind these changes.

### Tests
- [x] Added tests covering the new functionality
- [x] All tests passing (`pytest`)

### Notes
- [Optional] Mention dependencies, known issues, or future enhancements
```

---
