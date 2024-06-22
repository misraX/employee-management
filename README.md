
<h1 style="text-align: center">Employee Management</h1>

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

## Overview
This project follows a client-server architecture, where the server contains the `employee_management` project and its related applications, and the client is a Command-Line Interface (CLI) client that consumes the server's services.

### Server
The server contains the `employee_management` project, which includes various applications. The server exposes its services, allowing the client to interact with them.

### Client
The client is a CLI application that can use any of the server's services by importing them. The client has its own data modeling, which handles data transformation for the local environment (e.g., date and time conversion).

This approach can be easily transformed to support different types of interfaces, such as a web application or mobile app, that can consume the server's APIs. The services are loosely coupled, using underlying repositories, and can be easily adjusted to work with various serializers.

## Key Features
1. **Server-Client Architecture**: The project follows a client-server approach, where the server hosts the `employee_management` project and the client consumes the server's services.
2. **Loose Coupling**: The services are loosely coupled, using underlying repositories, which allows for easy adjustments and adaptations to different serializers.
3. **Data Transformation**: The client handles data transformation, such as date and time conversion, to ensure compatibility with the local environment.
4. **Scalability**: The server-client architecture allows for easy scaling and expansion of the system, as the client can be adapted to different types of interfaces (web, mobile, etc.) while consuming the same server-side services.
5. **Schedulers**: Using celery and celery beat with a redis broker to handle recurring email notification or async operation

## Installation

```shell
docker compose up -d # Build and run docker compose
docker compose exec cli bash -c "python miscellaneous/build_tools/db.py" # Run The DB migrations
```

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
    ├── notifications/ # Notifications like NotifyByEmail
    ├── scheduler/ # Celery beat or crontabs
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
  add                           Add a new employee ✨
  delete                        Delete an employee by ID 🗑️
  get                           Get an employee by ID 🔍
  get-current-employee-holiday  Get the current week public holidays 🍹
  list                          List all employees 📋
  update                        Update an existing employee ✨
```

### Example Commands

All the below commands can run inside the docker containers by pre-appending `docker compose exec cli`

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

- **Get current employee's holidays:**
    ```sh
    python main.py get-current-employee-holiday "employee_id"
    ```


### Example outputs

- **List all employees:**
```text
[
    {
        "name": "Darrell Boyer",
        "salary": 1675.8,
        "position": "Software Developer",
        "email": "weberjamie@example.org",
        "country": "TL",
        "employee_id": "3fc4e19c-0101-4dae-bd41-ecaa1c0cd6d8",
        "created_at": "2024-06-19 20:03:42.746949-0400",
        "updated_at": "2024-06-19 20:03:42.746949-0400"
    },
    {
        "name": "Anthony Calderon",
        "salary": 288.15646,
        "position": "Software Developer",
        "email": "david21@example.org",
        "country": "PY",
        "employee_id": "48eedaf8-8aad-41a4-aa69-b7a86781d949",
        "created_at": "2024-06-19 20:03:42.746949-0400",
        "updated_at": "2024-06-19 20:03:42.746949-0400"
    },
    {
        "name": "Rodney Foster",
        "salary": 1034.2,
        "position": "Software Developer",
        "email": "ybuck@example.org",
        "country": "AG",
        "employee_id": "dea7ba72-4338-447f-a945-d8616015d12a",
        "created_at": "2024-06-19 20:03:42.746949-0400",
        "updated_at": "2024-06-19 20:03:42.746949-0400"
    },
    {
        "name": "Gary Cooley",
        "salary": 1302.3419,
        "position": "Software Developer",
        "email": "daniel53@example.net",
        "country": "BF",
        "employee_id": "d9049a8e-911d-4710-9ede-6ba94092f127",
        "created_at": "2024-06-19 20:03:42.746949-0400",
        "updated_at": "2024-06-19 20:03:42.746949-0400"
    },
    {
        "name": "Lisa Davila",
        "salary": 1825.7181082,
        "position": "Software Developer",
        "email": "westgina@example.com",
        "country": "MG",
        "employee_id": "cc8989ee-a547-4270-a96e-d58dcff141ef",
        "created_at": "2024-06-19 20:03:42.746949-0400",
        "updated_at": "2024-06-19 20:03:42.746949-0400"
    },
    {
        "name": "Yolanda Johnson",
        "salary": 1621.79069837,
        "position": "Software Developer",
        "email": "johnclarke@example.org",
        "country": "KG",
        "employee_id": "764c3208-f01e-4987-a68b-f63ee6b334c6",
        "created_at": "2024-06-19 20:03:42.746949-0400",
        "updated_at": "2024-06-19 20:03:42.746949-0400"
    }
]
Press enter to continue <enter>, current offset 4000, current count 4239, fetched employees 239.
Found 4239 employees!
```

- **Get an employee by ID**
```text
🔍 Employee found:
{
    "name": "Maysra Gamal",
    "salary": 11111.0,
    "position": "Software Developer",
    "email": "maysra@gmail.com",
    "employee_id": "47470cce-f2e7-41ef-b891-4afec06b87f1",
    "country": "EG",
    "created_at": "2024-06-20 23:28:16.142435-0400",
    "updated_at": "2024-06-20 23:28:16.142435-0400"
}
```

- **Get current employee's holidays:**
```text
🍹 List of employee's current week holidays
[{
    "date": "2024-06-18",
    "holiday": "Eid al-Adha Holiday (estimated)"
}]
```
