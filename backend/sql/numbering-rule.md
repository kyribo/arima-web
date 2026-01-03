# SQL Numbering Rules

1.  **Login / Auth**: `01-(sequense)-(name).sql`
    *   Example: `01-01-init-auth.sql`, `01-07-password-history.sql`
2.  **User Management**: `02-(sequence)-(name).sql`
    *   Example: `02-01-add-access-column.sql`
3.  **Risk Event**: `03-(sequence)-(name).sql`
    *   All tables related to Risk Event features (Schema `riske`).
4.  **Seeders**: `99-(sequence)-(name).sql`
    *   Example: `99-01-superadmin.sql`
