--
The bot operates through multi-step conversational dialogs that guide users through event creation, validation, and scheduling. 
When events are created, the system automatically notifies all authorized laboratory personnel, ensuring team-wide awareness of laboratory operations.

Technology Stack
--
The system is built on a modern, containerized technology stack designed for reliability and scalability:

  **Component	Technology	Purpose**
**Bot Framework**	aiogram	Telegram Bot API wrapper with async support
Dialog System	aiogram_dialog	Complex conversational flow management
Database	PostgreSQL 15 Alpine	Persistent data storage for events and users
State Management	Redis 7	Dialog state and FSM storage
ORM	SQLAlchemy (async)	Database abstraction and models
Migrations	Alembic	Database schema version control
Containerization	Docker Compose	Service orchestration and deployment
Administration	pgAdmin 4	Database management interface

