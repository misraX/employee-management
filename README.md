# Employee Management

A simple Employee Database Management System using OOP

# Packaging

```text
employee_management/
├── core/ # Core package for reusability
│   └── repositories/ # Base repositories
├── database/ # Database engine and session management
├── employee/ # The Employee module (app)
│   ├── models/ # The Employee's models
│   ├── repositories/ # The Employee's repositories
│   └── services/ # The Employee's services
├── exceptions/ # Custom exceptions like InvalidEmailException
├── logging/ # Logging configuration
├── utilities/ # Transformers, Convertors like TimeUtility
└── validators/ # Object values validators like EmailValidator

tests/
├── core/
│   └── repositories/
└── employee/
    ├── models/
    ├── repositories/
    └── services/
```


# Code Quality

This project uses several tools to ensure code quality, style consistency, and best practices.

**Tools and configuration**

1. pre-commit ensure that the code is commited with the standards configuration which can be found in `.pre-commit-config.yaml`
2. conventional-pre-commit ensure that the commit follows the [Conventional Commits
](https://www.conventionalcommits.org/en/v1.0.0/)
3. ruff ⚡️ The fastest linter and formatter [ruff](https://docs.astral.sh/ruff/) with a configuration which can be found in `ruff.toml`
