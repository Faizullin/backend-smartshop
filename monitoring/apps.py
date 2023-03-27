from django.apps import AppConfig

#from monitoring.management.commands import save_system_data


class MonitoringConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'monitoring'

    # def ready(self):
    #     #Register the new management command
    #     from monitoring.management.commands.save_system_data import Command
    #     from monitoring.management.commands import save_system_data
    #     print("Aync Monitoring Ready")
    #     save_system_data.Command().register(self)
    #     self.commands['save_system_data'] = Command()
    #     self.add_command('save_system_data', Command())
