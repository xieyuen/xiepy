from mcdreforged import PluginServerInterface


def on_load(server: PluginServerInterface, _prev_module):
    server.logger.info("Loaded XiePy(MCDR)")
