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

*Note: Permissions indicate the minimum role required. Admins typically have access to all endpoints.* 
*Filtering (e.g., `/devices/?room=1`, `/workorders/?status=Open`) and searching (e.g., `/devices/?search=XYZ`) will be implemented on list views.*

## Frontend Routing (React Router)

| Path                   | Component/Page             | Description                                         | Access Control      |
| :--------------------- | :------------------------- | :-------------------------------------------------- | :------------------ |
| `/login`               | `LoginPage`                | User login form                                     | Public              |
| `/signup`              | `SignupPage`               | User registration form                              | Public              |
| `/`                    | `Dashboard` / Redirector   | Main dashboard after login, redirects based on role | Authenticated       |
| `/devices`             | `DeviceListPage`           | Display list of devices (view depends on role)      | Authenticated       |
| `/devices/new`         | `DeviceCreatePage`         | Form to create a new device                         | Admin               |
| `/devices/:id`         | `DeviceDetailPage`         | Display details of a specific device                | Authenticated       |
| `/devices/:id/edit`    | `DeviceEditPage`           | Form to edit a specific device                      | Admin, Engineer     |
| `/devices/:id/inventory`| `DeviceInventoryPage`      | Form to update device location during inventory     | Engineer            |
| `/workorders`          | `WorkOrderListPage`        | Display list of work orders (view depends on role)  | Authenticated       |
| `/workorders/new`      | `WorkOrderCreatePage`      | Form to create a new work order                     | Engineer, Nurse     |
| `/workorders/:id`      | `WorkOrderDetailPage`      | Display details of a specific work order            | Authenticated       |
| `/workorders/:id/edit` | `WorkOrderEditPage`        | Form to update work order status, etc.              | Admin, Engineer, Nurse |
| `/spareparts`          | `SparePartListPage`        | Display list of spare part requests                 | Admin, Engineer     |
| `/spareparts/new`      | `SparePartCreatePage`      | Form to create a new spare part request             | Engineer            |
| `/spareparts/:id`      | `SparePartDetailPage`      | Display details of a specific spare part request    | Admin, Engineer     |
| `/profile`             | `ProfilePage`              | View/edit user profile                              | Authenticated       |
| `/admin/users`         | `UserManagementPage`       | (Optional) Manage users                             | Admin               |
| `/*`                   | `NotFoundPage`             | Displayed for any undefined routes                  | Public              |

*Note: Access Control indicates whether a route is public or requires authentication. Specific role-based rendering/redirection will happen within components based on the logged-in user's role.*
