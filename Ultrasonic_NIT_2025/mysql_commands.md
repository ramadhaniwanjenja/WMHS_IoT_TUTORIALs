# MySQL Quick Reference Guide

A simple cheat sheet for basic MySQL commands.

## Table of Contents
- [Login & Logout](#login--logout)
- [Database Commands](#database-commands)
- [Table Commands](#table-commands)
- [Viewing Data (SELECT)](#viewing-data-select)
- [Adding Data (INSERT)](#adding-data-insert)
- [Modifying Data (UPDATE)](#modifying-data-update)
- [Deleting Data (DELETE)](#deleting-data-delete)
- [User Management](#user-management)
- [Altering Tables](#altering-tables)
- [Server Info](#server-info)
- [Tips](#tips)

## Login & Logout

```bash
mysql -u root -p          # Login (enter your password when prompted)
```

```sql
EXIT;                     -- Leave MySQL
QUIT;                     -- Same as EXIT
```

## Database Commands

```sql
SHOW DATABASES;                    -- List all databases
CREATE DATABASE my_database;       -- Create new database
USE my_database;                   -- Switch into a database
SELECT DATABASE();                 -- Check current database
DROP DATABASE my_database;         -- Delete a database
```

## Table Commands

```sql
SHOW TABLES;                       -- List all tables in current DB
DESCRIBE my_table;                 -- Show columns and types
DESC my_table;                     -- Short form of DESCRIBE
SHOW CREATE TABLE my_table;        -- Show full CREATE statement
DROP TABLE my_table;               -- Delete a table
TRUNCATE TABLE my_table;           -- Empty table but keep structure
```

### Create a table example

```sql
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(150) UNIQUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Viewing Data (SELECT)

```sql
SELECT * FROM users;                          -- All rows, all columns
SELECT name, email FROM users;                -- Specific columns
SELECT * FROM users LIMIT 5;                  -- First 5 rows
SELECT * FROM users ORDER BY created_at DESC; -- Newest first
SELECT * FROM users ORDER BY name ASC;        -- Alphabetical order
SELECT * FROM users WHERE id = 3;             -- Filter by ID
SELECT * FROM users WHERE name LIKE '%john%'; -- Text search
SELECT COUNT(*) FROM users;                   -- Count all rows
SELECT COUNT(*) FROM users WHERE id > 10;     -- Count with filter
```

## Adding Data (INSERT)

```sql
-- Single row
INSERT INTO users (name, email) VALUES ('John Doe', 'john@example.com');

-- Multiple rows
INSERT INTO users (name, email) VALUES
  ('Alice', 'alice@example.com'),
  ('Bob', 'bob@example.com'),
  ('Carol', 'carol@example.com');
```

## Modifying Data (UPDATE)

```sql
UPDATE users SET name = 'New Name' WHERE id = 1;
UPDATE users SET email = 'new@email.com' WHERE name = 'John Doe';
```

> Always use `WHERE` — without it, ALL rows are updated.

## Deleting Data (DELETE)

```sql
DELETE FROM users WHERE id = 1;     -- Delete one row
DELETE FROM users WHERE id > 100;   -- Delete filtered rows
DELETE FROM users;                  -- Delete ALL rows (dangerous!)
```

## User Management

```sql
SELECT user, host FROM mysql.user;                                              -- List users
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '1234';  -- Change password
CREATE USER 'newuser'@'localhost' IDENTIFIED BY 'pass123';                      -- Create user
GRANT ALL PRIVILEGES ON my_database.* TO 'newuser'@'localhost';                 -- Grant access
REVOKE ALL PRIVILEGES ON my_database.* FROM 'newuser'@'localhost';              -- Remove access
DROP USER 'newuser'@'localhost';                                                -- Delete user
FLUSH PRIVILEGES;                                                               -- Apply changes
```

## Altering Tables

```sql
ALTER TABLE users ADD COLUMN phone VARCHAR(20);          -- Add column
ALTER TABLE users DROP COLUMN phone;                     -- Remove column
ALTER TABLE users MODIFY name VARCHAR(200);              -- Change column type
ALTER TABLE users RENAME COLUMN name TO full_name;       -- Rename column
ALTER TABLE users RENAME TO customers;                   -- Rename table
```

## Server Info

```sql
STATUS;                           -- Server information
SHOW PROCESSLIST;                 -- Active queries
SHOW VARIABLES LIKE 'port';       -- Server settings
SHOW ENGINES;                     -- Available storage engines
\h                                -- Help menu
\c                                -- Cancel current command
```

## Common Workflow Example

```sql
-- After: mysql -u root -p
SHOW DATABASES;
USE my_database;
SHOW TABLES;
DESCRIBE users;
SELECT * FROM users ORDER BY created_at DESC LIMIT 10;
SELECT COUNT(*) FROM users;
EXIT;
```

## Tips

1. **Every command ends with a semicolon `;`** — if MySQL seems to hang, you forgot it. Just type `;` and press Enter.
2. **Stuck in `'>` or `">` prompt?** You have an unclosed quote. Type `';` or `";` then Enter to escape.
3. **Press ↑ arrow** to recall previous commands.
4. **Commands aren't case-sensitive** — `select` = `SELECT`. Use UPPERCASE for keywords by convention.
5. **Database and table names ARE case-sensitive on Linux** — `MyDB` ≠ `mydb`.
6. **Use `\c` to cancel** a command mid-typing.
7. **Always use `WHERE`** with `DELETE` and `UPDATE` — double-check before pressing Enter.
8. **Backup first** before running destructive commands in production.

## Common Data Types

| Type | Description | Example |
|------|-------------|---------|
| `INT` | Whole number | `42` |
| `VARCHAR(n)` | Text up to n characters | `'Hello'` |
| `TEXT` | Long text | `'A long paragraph...'` |
| `DATE` | Date only | `'2025-01-15'` |
| `DATETIME` | Date + time | `'2025-01-15 14:30:00'` |
| `TIMESTAMP` | Auto-updating date/time | `CURRENT_TIMESTAMP` |
| `BOOLEAN` | True/false | `TRUE` or `FALSE` |
| `DECIMAL(m,n)` | Decimal number | `99.99` |

## Useful Links

- [Official MySQL Documentation](https://dev.mysql.com/doc/)
- [MySQL Tutorial](https://www.mysqltutorial.org/)
- [W3Schools MySQL](https://www.w3schools.com/mysql/)

## License

Free to use and share.