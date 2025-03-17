# FunHub Ticketing System

## Project Overview

FunHub Ticketing System is a Django-based support ticket management system that enables efficient handling of user support requests. It provides a structured way for users to submit tickets, receive responses, and track the status of their inquiries.

## Core Features

- User Authentication: Email-based user authentication system
- Ticket Management:
  - Create and view support tickets
  - Reply to existing tickets
  - Attach files to tickets
  - Close tickets when resolved
- Permission System:
  - Regular users can create and manage their tickets
  - Support staff can view and respond to all tickets
  - Role-based access control

## System Architecture

### Apps Structure

1. **Accounts App**

   - Handles user authentication and management
   - Custom user model with email-based authentication
   - User registration and login functionality

2. **Tickets App**

   - Core ticket management functionality
   - Models:
     - Ticket: Stores ticket information and status
     - TicketMessage: Manages ticket replies and attachments
   - Views for ticket operations (create, list, detail, reply)

3. **Pages App**
   - Manages static pages and templates
   - Basic routing for non-dynamic content

### Key Components

- Django-based backend
- Template-based frontend
- File attachment handling
- Permission-based access control

## Installation Guide

### Prerequisites

- Python 3.x
- pip (Python package manager)

### Setup Steps

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:

   - Windows: `activate_env.bat`
   - Linux/Mac: `source venv/bin/activate`

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

6. Create a superuser:

   ```bash
   python manage.py createsuperuser
   ```

7. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Testing

The project includes comprehensive test coverage for all major components:

### Running Tests

- Run all tests:

  ```bash
  python manage.py test
  ```

- Run specific app tests:
  ```bash
  python manage.py test accounts
  python manage.py test tickets
  python manage.py test pages
  ```

### Test Coverage

- Account management tests
- Ticket creation and management tests
- Permission system tests
- Form validation tests

## Usage Guide

### User Roles

1. **Regular Users**

   - Can create new tickets
   - Can view and reply to their own tickets
   - Can close their own tickets

2. **Support Staff**
   - Can view all tickets
   - Can reply to any ticket
   - Can close any ticket

### Ticket Lifecycle

1. **Creation**

   - User creates a ticket with a title
   - Initial message and optional attachments can be added

2. **Management**

   - Staff members can view and respond to tickets
   - Users can add replies and attachments
   - All participants can track the conversation

3. **Resolution**
   - Tickets can be closed by creators or staff
   - Closed tickets cannot receive new replies

### Common Operations

1. **Creating a Ticket**

   - Navigate to 'Create Ticket' page
   - Fill in the title and initial message
   - Add attachments if needed
   - Submit the ticket

2. **Responding to Tickets**

   - Open the ticket detail page
   - Add your reply in the message box
   - Attach files if necessary
   - Submit your response

3. **Closing Tickets**
   - Open the ticket you want to close
   - Click the 'Close Ticket' button
   - Confirm the action

## Security Considerations

- Implemented permission-based access control
- Secure file upload handling
- Protected against unauthorized access
- Email verification for user registration
