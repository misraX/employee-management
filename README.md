# Employee Management

A simple Employee Database Management System using OOP

# Packaging

```text

employee_management/ Main Project package
├── apps/ Applications package like employee, holidays
│   └── employee/ # The Employee app
│       ├── models/ # The Employee's model
│       ├── repositories/ # The Employee's repos
│       └── services/ # The Employee's services
├── core/
│   ├── configurations/ # The project configuration
│   └── repositories/ # The project abstract base repositories where it hold Repositories and CRUDRepositories Interfaces
├── database/ # The DB manager, like sessions, different drivers
├── exceptions/ # Project custom Exceptions like EmailValidationException, and ImmutableAttributeError
├── logging/ # Project logging <logger>
├── utilities/ # Project utilities like TimeUtility
└── validators/ # Project Validators like EmailValidator

tests/
└── test_employee_management/
    ├── apps/
    │   └── employee/
    │       ├── models/
    │       ├── repositories/
    │       └── services/
    ├── core/
    │   ├── configurations/
    │   └── repositories/
    └── database/
```


# Code Quality

This project uses several tools to ensure code quality, style consistency, and best practices.

**Tools and configuration**

1. pre-commit ensure that the code is commited with the standards configuration which can be found in `.pre-commit-config.yaml`
2. conventional-pre-commit ensure that the commit follows the [Conventional Commits
](https://www.conventionalcommits.org/en/v1.0.0/)
3. ruff ⚡️ The fastest linter and formatter [ruff](https://docs.astral.sh/ruff/) with a configuration which can be found in `ruff.toml`


**Key points**

1. The use of ruff ensures that the code pass multiple linters.
2. The used linters are as follows: ```python ['T20', 'INP', 'Q', 'I', 'B', 'SIM', 'E', 'W', 'F']```
3. Line length is caped to 100, and errors will be raised by pre-commit if exceeded.

**Pre-commit checks**

```text
check for added large files..............................................
check toml...........................................
check yaml...........................................
fix end of files.........................................................
trim trailing whitespace.................................................
ruff.....................................................................
ruff-format..............................................................
check toml...........................................
check yaml...........................................
ruff.................................................
ruff-format..........................................
Conventional Commit......................................................
```
