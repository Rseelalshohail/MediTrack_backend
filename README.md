# MediTrack_backend

## Database Design (ERD):

![image](https://github.com/user-attachments/assets/3cc93460-5461-4126-baca-de419817748a)

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


**User Stories (Included in Implementation Plan)**
- As an Admin, I want to log in to the system.
- As an Admin, I want to add, view, edit, and delete medical devices.
- As an Admin, I want to view all work orders.
- As an Admin, I want to view all spare part requests.
- As an Engineer, I want to log in to the system.
- As an Engineer, I want to view devices assigned to me or in my area.
- As an Engineer, I want to edit device details.
- As an Engineer, I want to create Corrective Maintenance (CM) and Preventive Planned Maintenance (PPM) work orders.
- As an Engineer, I want to update the status of my work orders.
- As an Engineer, I want to request spare parts for a device.
- As an Engineer, I want to perform annual inventory by updating a device's location.
- As a Nurse, I want to log in to the system.
- As a Nurse, I want to view devices in my department/location.
- As a Nurse, I want to create a Corrective Maintenance (CM) work order for a device.
- As a Nurse, I want to view work orders for my department.
- As a Nurse, I want to close a work order when the issue is resolved.
