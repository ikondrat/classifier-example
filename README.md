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

```
classifier_demo/
├── classifier_demo/     # Main application package
├── tests/              # Test files
├── pyproject.toml      # Project configuration and dependencies
├── Makefile           # Development commands
└── README.md          # This file
```
