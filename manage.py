#!/usr/bin/env python
from migrate.versioning.shell import main

if __name__ == '__main__':
    main(url='postgresql://localhost/wedding_site', debug='False', repository='wedding_site_migrations')
