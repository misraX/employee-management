
<h1 style="text-align: center">Employee Management</h1>
<p style="text-align: center">A simple Employee Database Management System</p>

<p style="text-align: center">
  <a href="https://raw.githubusercontent.com/misraX/employee-management/gh-pages/coverage.svg">
    <img src="https://raw.githubusercontent.com/misraX/employee-management/gh-pages/coverage.svg" alt="Coverage">
  </a>
  <a href="https://github.com/misraX/employee-management/actions/workflows/test.yml">
    <img src="https://github.com/misraX/employee-management/actions/workflows/test.yml/badge.svg" alt="Python Tests">
  </a>
  <a href="https://github.com/misraX/employee-management/actions/workflows/lint.yml">
    <img src="https://github.com/misraX/employee-management/actions/workflows/lint.yml/badge.svg" alt="Lint">
  </a>
</p>

The main idea of the project is a python server/client approach.

The server contains the employee_management project with it's related applications.

The client contains a CLI client which consumes the server's services.

The client can use any of the server services, simply by importing the services from the server application.

The client has its own modeling which handles the data transformation to local data, for example a React Client which
consumes APIs from a remote server will take in consideration date and time conversion for local/client laptop,mobile, etc.

This approach can easily transform to a web or any kind of interfaces that will support API's from Rest/GraphQL or any sort of APIs
The services are loosely coupled which uses underlying repositories and can be easily adjusted to any serializers.

## Packaging

```text

server/
└── employee_management/ Main Project package
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

client/ # A CLI client to consume the services
└── employee_management # The employee management client, the currently available client is CLI
    ├── cli/ # A specific CLI for the Employee's service
    └── models/ Serialize and transform the data to local clients
tests/
└── test_server
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
