# MediTrack Backend 

## 🌟 Project Description

MediTrack is a full-stack medical device management system designed for hospitals and clinical environments. It enables engineers, nurses, and administrators to manage medical equipment, work orders, and spare part requests through a secure, role-based interface. The backend is built with Django and Django REST Framework, supporting robust APIs, user authentication (JWT), and multi-role access logic.

## 🔹 Repository Description

This repository contains the backend of the MediTrack project. It handles API endpoints, database models, business logic, and JWT-based authentication for three user types (Admin, Engineer, Nurse).

## 📄 Frontend Repository

https://github.com/Rseelalshohail/MediTrack_frontend

## 🤖 Live Link

http://localhost:5173/signup

## 🌐 Tech Stack

- Django  
- Django REST Framework  
- PostgreSQL  
- SimpleJWT  
- Docker

## 📄 ERD Diagram

![image](https://github.com/user-attachments/assets/3cc93460-5461-4126-baca-de419817748a)

## 📄 Routing Table

Base Path: `/api/`

**Authentication (Simple JWT)**

| Method | Path                 | Description                       | Permissions      |
| :----- | :------------------- | :-------------------------------- | :--------------- |
| POST   | `/token/`            | Obtain JWT access/refresh token   | Public           |
| POST   | `/token/refresh/`    | Refresh JWT access token          | Public           |
| POST   | `/token/verify/`     | Verify JWT access token           | Public           |
| POST   | `/register/`         | User Registration                 | Public           |
| GET    | `/users/me/`         | Get current logged-in user info   | Authenticated    |

**Devices**

| Method      | Path                      | Description                                       | Permissions              |
| :---------- | :------------------------ | :------------------------------------------------ | :----------------------- |
| GET         | `/devices/`               | List devices (All for Admin, assigned for Eng.)   | Admin, Engineer          |
| POST        | `/devices/`               | Create a new device                               | Admin                    |
| GET         | `/devices/<int:pk>/`      | Retrieve details of a specific device             | Admin, Engineer, Nurse   |
| PUT/PATCH   | `/devices/<int:pk>/`      | Update a specific device                          | Admin, Engineer          |
| DELETE      | `/devices/<int:pk>/`      | Delete a specific device                          | Admin                    |
| PATCH       | `/devices/<int:pk>/inventory/` | Update device location during inventory check     | Engineer                 |

**Work Orders**

| Method      | Path                      | Description                                       | Permissions              |
| :---------- | :------------------------ | :------------------------------------------------ | :----------------------- |
| GET         | `/workorders/`            | List work orders (filtered by role/permissions)   | Admin, Engineer, Nurse   |
| POST        | `/workorders/`            | Create a new work order                           | Engineer, Nurse          |
| GET         | `/workorders/<int:pk>/`   | Retrieve details of a specific work order         | Admin, Engineer, Nurse   |
| PUT/PATCH   | `/workorders/<int:pk>/`   | Update a specific work order (e.g., status)       | Admin, Engineer, Nurse   |
| DELETE      | `/workorders/<int:pk>/`   | Delete a specific work order (Admin only)         | Admin                    |

**Spare Part Requests**

| Method      | Path                      | Description                                       | Permissions              |
| :---------- | :------------------------ | :------------------------------------------------ | :----------------------- |
| GET         | `/spareparts/`            | List spare part requests (All for Admin, own for Eng.) | Admin, Engineer          |
| POST        | `/spareparts/`            | Create a new spare part request                   | Engineer                 |
| GET         | `/spareparts/<int:pk>/`   | Retrieve details of a specific request            | Admin, Engineer          |
| PUT/PATCH   | `/spareparts/<int:pk>/`   | Update a specific request                         | Admin, Engineer          |
| DELETE      | `/spareparts/<int:pk>/`   | Delete a specific request                         | Admin                    |

**Supporting Models**

| Method | Path             | Description         | Permissions   |
| :----- | :--------------- | :------------------ | :------------ |
| GET    | `/rooms/`        | List all rooms      | Authenticated |
| GET    | `/roles/`        | List all roles      | Admin         |


## User Stories (Included in Implementation Plan):
- As an Admin, I want to log in to the system.
- As an Admin, I want to add, view, edit, and delete medical devices.
- As an Admin, I want to view all work orders.
- As an Admin, I want to view all spare part requests.
- As an Engineer, I want to log in to the system.
- As an Engineer, I want to view devices assigned to me.
- As an Engineer, I want to update the status of my work orders.
- As an Engineer, I want to request spare parts for a device.
- As a Nurse, I want to log in to the system.
- As a Nurse, I want to view devices assigned to me.
- As a Nurse, I want to create a work order for a device.
- As a Nurse, I want to view work orders created by me.

## 📚 Installation Instructions

```bash
# Clone the repo
$ git clone <MediTrack_backend>
$ cd <MediTrack_backend>

# Set up virtual environment and install dependencies
$ pipenv install
$ pipenv shell
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver
```

**If using Docker:**

```bash
$ docker compose up --build
```

## 🧋 IceBox Features

- Email reminders for overdue work orders  
- Multi-language support
- Work order priority levels
- Ability to export PDF reports for work orders  
- Dark mode toggle