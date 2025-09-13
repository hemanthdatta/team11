# Overview

This is a comprehensive Micro-Entrepreneur Growth App designed to help small business owners in India scale their operations. The application combines customer relationship management, referral systems, digital presence building, and AI-powered marketing assistance to provide an all-in-one growth platform for micro-entrepreneurs.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
The frontend is built using modern React with TypeScript and follows a component-based architecture:

- **Framework**: React 18 with TypeScript and Vite for fast development
- **UI Components**: Radix UI primitives with custom styling for accessibility and consistency
- **Styling**: Tailwind CSS with custom design tokens and dark mode support
- **State Management**: React hooks for local state, with API service layer for server communication
- **Navigation**: Single-page application with screen-based routing managed through React state

The application follows a mobile-first design approach with responsive layouts, organized into main functional areas: Dashboard, Customers, Referrals, Digital Presence Builder, Analytics, and AI Marketing Assistant.

## Backend Architecture
The backend is implemented using FastAPI with a modular, API-first design:

- **Framework**: FastAPI for high-performance async API endpoints
- **Database**: SQLAlchemy ORM with SQLite for development (easily scalable to PostgreSQL)
- **Authentication**: JWT-based authentication with bcrypt password hashing
- **Background Tasks**: Celery with Redis for asynchronous processing of notifications and social media posts
- **Rate Limiting**: SlowAPI integration to prevent abuse, especially on AI endpoints
- **Security**: Comprehensive input validation, XSS prevention, and security headers middleware

The API is organized into domain-specific routers (auth, customers, referrals, dashboard, social, AI assistant) with proper separation of concerns and dependency injection for database sessions.

## Data Storage Architecture
The system uses a relational database approach with the following core entities:

- **Users**: Store entrepreneur profiles with authentication credentials
- **Customers**: Customer relationship management with contact information and interaction history
- **Referrals**: Track referral chains with reward points and status management
- **Social Accounts**: Store OAuth tokens for social media platform integrations
- **Interactions**: Log all customer communications across different channels

The database schema supports multi-tenant architecture where each user's data is properly isolated while maintaining referential integrity.

## Authentication and Authorization
Security is implemented through multiple layers:

- **JWT Tokens**: Stateless authentication with configurable expiration
- **Password Security**: bcrypt hashing with salt for secure password storage
- **Input Validation**: Pydantic models for request/response validation with custom validators for Indian phone numbers and email formats
- **Rate Limiting**: Platform-wide and endpoint-specific rate limiting to prevent abuse
- **CORS Configuration**: Properly configured cross-origin resource sharing for frontend-backend communication

## AI Integration Architecture
The application integrates Google Gemini AI for marketing assistance:

- **Content Generation**: AI-powered creation of social media posts, email campaigns, and customer outreach messages
- **Context Awareness**: Utilizes user profiles and customer data to generate personalized content
- **Platform Optimization**: Content formatting specific to different social media platforms (WhatsApp, Facebook, Instagram, LinkedIn, Twitter)
- **Rate Limiting**: Special rate limits on AI endpoints to manage API costs and prevent abuse
- **Fallback Handling**: Graceful error handling when AI services are unavailable

# External Dependencies

## Core Technologies
- **React 18** - Frontend framework with hooks and concurrent features
- **TypeScript** - Type safety across frontend and backend
- **FastAPI** - Modern Python web framework for building APIs
- **SQLAlchemy** - Python ORM for database operations
- **Vite** - Fast build tool and development server

## UI and Styling
- **Radix UI** - Accessible component primitives for React
- **Tailwind CSS** - Utility-first CSS framework
- **Lucide React** - Icon library with consistent design
- **Recharts** - Chart library for analytics visualization
- **React Hook Form** - Form handling and validation

## Backend Services
- **Celery** - Distributed task queue for background processing
- **Redis** - In-memory data store for caching and task queuing
- **python-jose** - JWT token handling
- **passlib** - Password hashing utilities
- **slowapi** - Rate limiting middleware
- **bleach** - HTML sanitization for security

## AI and External APIs
- **Google Gemini API** - AI-powered content generation and marketing assistance
- **Social Media APIs** - Integration points for WhatsApp Business, Facebook, Instagram (OAuth flows implemented)
- **Email Services** - Prepared for integration with email service providers
- **SMS Gateways** - Architecture supports SMS notification services

## Development and Testing
- **pytest** - Testing framework for backend
- **httpx** - HTTP client for API testing
- **python-dotenv** - Environment variable management
- **Alembic** - Database migration tool (prepared for production scaling)

The architecture is designed to be easily deployable on cloud platforms with containerization support and environment-based configuration management.