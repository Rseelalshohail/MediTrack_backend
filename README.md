# MediTrack_backend

## Backend API Routing (Django REST Framework):

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
