
<h1 align="center">Employee Management</h1>
<p align="center">A simple Employee Database Management System using OOP</p>

![Coverage](https://raw.githubusercontent.com/misraX/employee-management/gh-pages/coverage.svg)
[![Python Tests](https://github.com/misraX/employee-management/actions/workflows/test.yml/badge.svg)](https://github.com/misraX/employee-management/actions/workflows/test.yml)
[![Lint](https://github.com/misraX/employee-management/actions/workflows/lint.yml/badge.svg)](https://github.com/misraX/employee-management/actions/workflows/lint.yml)

## Packaging

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

## Code Quality

This project uses several tools to ensure code quality, style consistency, and best practices.

**Tools and configuration**

1. pre-commit ensure that the code is commited with the standards configuration which can be found
   in `.pre-commit-config.yaml`
2. conventional-pre-commit ensure that the commit follows the [Conventional Commits
   ](https://www.conventionalcommits.org/en/v1.0.0/)
3. ruff ⚡️ The fastest linter and formatter [ruff](https://docs.astral.sh/ruff/) with a configuration which can be found
   in `ruff.toml`

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

# Employee Management CLI

This project includes a command-line interface (CLI) for managing employee records. It allows you to add, update,
delete, and list employees.

## Usage

```text
Usage: main.py [OPTIONS] COMMAND [ARGS]...

  ✨ Employee Management CLI ✨

Options:
  --help  Show this message and exit.

Commands:
  add     Add a new employee ✨
  delete  Delete an employee by ID 🗑️
  get     Get an employee by ID 🔍
  list    List all employees 📋
  update  Update an existing employee ✨
```

### Example Commands

- **Add a new employee [Prompt] 🚀:**
    ```sh
    python main.py add
    ```

- **Get an employee by ID:**
    ```sh
    python main.py get "employee_id"
    ```

- **Delete an employee by ID:**
    ```sh
    python main.py delete "employee_id"
    ```

- **Update an employee's details [Prompt] 🚀:**
    ```sh
    python main.py update "employee_id"
    ```

- **List all employees:**
    ```sh
    python main.py list
    ```
