import sys

from django.core.management.base import BaseCommand
from django.db import DEFAULT_DB_ALIAS, connections
from django.db.migrations.loader import MigrationLoader
from django.conf import settings


class Command(BaseCommand):
    help = 'Checking if all migrations have been applied.'

    def handle(self, *args, **options):
        connection = connections[DEFAULT_DB_ALIAS]
        # Load migrations from disk/DB
        loader = MigrationLoader(connection)
        graph = loader.graph
        targets = graph.leaf_nodes()

        plan = []
        seen = set()
        to_apply = []

        # Generate the plan
        for target in targets:
            for migration in graph.forwards_plan(target):
                if migration not in seen:
                    node = graph.node_map[migration]
                    plan.append(node)
                    seen.add(migration)

        for node in plan:
            deps = ""
            if not node.key in loader.applied_migrations:
                to_apply.append("%s.%s%s" % (node.key[0], node.key[1], deps))
                self.stdout.write("[ ]  %s.%s%s" % (node.key[0], node.key[1], deps))
        if not plan:
            self.stdout.write('(no migrations)', self.style.ERROR)

        if settings.DJANGO_CHECK_MIGRATION:
            if to_apply:
                return sys.exit(-1)
            else:
                self.stdout.write('(all migrations have been applied)', self.style.SUCCESS)
                return sys.exit(0)
        return sys.exit(0)
