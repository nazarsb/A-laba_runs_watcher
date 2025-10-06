Overview
--
The bot operates through multi-step conversational dialogs that guide users through event creation, validation, and scheduling. 
When events are created, the system automatically notifies all authorized laboratory personnel, ensuring team-wide awareness of laboratory operations.

Technology Stack
--
The system is built on a modern, containerized technology stack designed for reliability and scalability:

| Component          | Technology               | Purpose                                           |
|--------------------|--------------------------|---------------------------------------------------|
| Bot Framework      | aiogram3                 | Telegram Bot API wrapper with async support       |
| Dialog System      | aiogram_dialog           | Complex conversational flow management            |
| Database           | PostgreSQL 15 Alpine     | Persistent data storage for events and users      |
| State Management   | Redis 7                  | Dialog state and FSM storage                      |
| ORM                | SQLAlchemy (async)       | Database abstraction and models                   |
| Migrations         | Alembic                  | Database schema version control                   |
| Containerization   | Docker Compose           | Service orchestration and deployment              |
| Administration     | pgAdmin 4                | Database management interface                     |

Key Features
--
**Multi-Step Event Creation**

The system provides guided workflows for creating three types of laboratory events:

    Instrument Runs: Schedule equipment usage with reagent selection and duration calculation
    Power Outages: Plan electrical maintenance with optional time specification
    General Events: Create custom events with user-defined names and scheduling

**Role-Based Security**

The AlbgShieldMiddleware ensures only authorized personnel can access bot functionality, with automatic user role tracking and access denial notifications.

**Real-Time Notifications**

When events are created, the system uses get_users_exept_role to identify active users and broadcasts notifications to the entire laboratory team.

**Persistent Dialog State**

Redis-backed state management ensures dialog sessions survive system restarts and maintain user context across interactions.

**Container-Based Deployment**
Full Docker Compose setup with separate development and production profiles, including health checks and logging configuration.

**TO DO**
--
- add i18n
- add NATS notification service


