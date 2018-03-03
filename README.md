# Vault.io

Vault.io is an open source project that creates a server which serves as the collective notebook of a group of users.

## Docs

Vault.io is written using Python and PostgreSQL.  It is a normal Django app, with no special caveats.  Anywhere that runs Django and Python 3.6+ can run Vault.io.  Before running, run `export $(cat .env)` to export any necessary environment variables.

Note that the PostgreSQL database is required over any alternative databases because of the way in which Vault.io utilizes PostgreSQL full text search.

## Contributors

* Michael Helvey (development, design)
* Michael Jones (design)

### License

MIT