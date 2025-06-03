# 🤖 Classifier Demo

This is a demo project for a classifier API. It uses a pre-trained model to classify text into categories.

## ✨ Features

- 🚀 FastAPI framework for high-performance API development
- 🔥 PyTorch integration for machine learning capabilities
- 🤖 Transformers library support for state-of-the-art NLP models
- 🛠️ Modern development tooling:
  - ✨ Ruff for linting and formatting
  - 📝 MyPy for type checking
  - ✅ Pytest for testing
  - 📦 UV for dependency management

## 📋 Prerequisites

- 🐍 Python 3.12 or higher ([Download](https://www.python.org/downloads/))
- 📦 UV package manager ([Installation Guide](https://github.com/astral-sh/uv#installation))

## 🚀 Installation

1. Clone the repository:

```bash
git clone <your-repository-url>
cd classifier_demo
```

2. Install dependencies:

```bash
make install
```

This will install all required dependencies using UV package manager.

## 💻 Development

The project includes several development commands:

- Run the application:

```bash
make run
```

- Run tests:

```bash
make test
```

- Lint code:

```bash
make lint
```

- Check types:

```bash
make type-check
```

- Format code:

```bash
make format
```

- Validate code (runs lint, type-check, and format-check):

```bash
make validate
```

## 📁 Project Structure

The project follows a clean, layered architecture pattern:

```
classifier_demo/
├── src/                    # Source code root
│   └── classifier_demo/    # Main application package
│       ├── api/           # API layer - FastAPI routes and endpoints
│       ├── services/      # Service layer - Business logic and ML model integration
│       ├── middleware/    # Middleware components (auth, logging, etc.)
│       └── main.py        # Application entry point
├── tests/                 # Test files
├── pyproject.toml         # Project configuration and dependencies
├── Makefile              # Development commands
└── README.md             # This file
```

### Architecture Layers

- **API Layer** (`api/`): Handles HTTP requests/responses, input validation, and route definitions
- **Service Layer** (`services/`): Contains business logic, ML model integration, and orchestrates data flow
- **Middleware Layer** (`middleware/`): Provides cross-cutting concerns like authentication, logging, and error handling
