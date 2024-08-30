# Statikk

**Statikk** is an open-source Firebase alternative built with Python and SurrealDB. It offers real-time data management, authentication, and cloud functions in a scalable and maintainable codebase.

## Features

- **Real-time Database**: Manage data in real-time with SurrealDB.
- **Authentication**: Secure user authentication with JWT or OAuth.
- **Cloud Functions**: Run custom backend logic.

### Project Structure

```plaintext
statikk/
│
├── domain/                   # Domain layer: business logic
│   ├── entities/             # Core domain entities
│   ├── value_objects/        # Immutable value objects
│   ├── services/             # Domain services
│   └── repositories/         # Repository interfaces
│
├── application/              # Application layer: use cases and interfaces
│   ├── use_cases/            # Use case implementations
│   └── interfaces/           # Application interfaces
│
├── infrastructure/           # Infrastructure layer: database, API, etc.
│   ├── persistence/          # Database adapters (e.g., SurrealDB)
│   └── web/                  # Web/API server
│       ├── routes/           # API route definitions
│       └── fastapi_app.py    # Main API application
│
├── tests/                    # Tests
│   ├── unit/                 # Unit tests
│   ├── integration/          # Integration tests
│   └── e2e/                  # End-to-end tests
│
├── .gitignore                # Git ignore file
├── README.md                 # Project documentation
└── requirements.txt          # Python dependencies
```

### Contributing

Contributions are welcome! Please fork the repository, create a new branch, and submit a pull request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a pull request

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
