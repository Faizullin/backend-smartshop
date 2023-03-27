from django.apps import AppConfig

#from monitoring.management.commands import save_system_data


class MonitoringConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'monitoring'

    def ready(self):
        import os
        if 'RUN_MAIN' not in os.environ:
            # Only run this code once, not in child processes
            # (when using the autoreload feature)
            from django.core.management import execute_from_command_line
            execute_from_command_line(['manage.py', 'save_system_data'])
    #     #Register the new management command
    #     from monitoring.management.commands.save_system_data import Command
    #     from monitoring.management.commands import save_system_data
    #     print("Aync Monitoring Ready")
    #     save_system_data.Command().register(self)
    #     self.commands['save_system_data'] = Command()
    #     self.add_command('save_system_data', Command())
