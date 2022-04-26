from src.graphic_handlers.object_frame import ObjectFrame
from src.utils.logger import Logger
from src.utils.regex_checker import matches


class ObjectFrameHandler():

    def __init__(self, object_frame: ObjectFrame, logger: Logger) -> None:
        self.object_frame: ObjectFrame = object_frame
        self.logger: Logger = logger
        self.config_events()

    def config_events(self) -> None:
        self.config_to_previous()
        self.config_to_main_menu()
        self.config_exit()

        self.config_network_information()
        self.config_manipulation()

    # Always-visible button
    def config_to_previous(self) -> None:
        self.object_frame.previous_menu_button.config(command=self.object_frame.return_to_previous)

    def config_to_main_menu(self) -> None:
        self.object_frame.main_menu_button.config(
            command=self.object_frame.return_to_main_menu)

    def config_exit(self) -> None:
        self.object_frame.exit_button.config(command=self.object_frame.exit)

    # Menu-specific buttons
    def config_network_information(self) -> None:
        # Main Menu
        self.object_frame.network_information_button.config(command=self.object_frame.network_information_menu)

        # Network Information menu
        self.object_frame.hosts_button.config(command=self.object_frame.hosts_information_menu)
        self.object_frame.routers_button.config(command=self.object_frame.routers_information_menu)

    def config_manipulation(self) -> None:
        # Main Menu
        self.object_frame.manipulation_button.config(command=self.object_frame.manipulation_menu)

        # Manipulation Menu
        self.object_frame.placement_button.config(command=self.object_frame.placement_menu)
        self.object_frame.config_button.config(command=self.object_frame.config_menu)

        # Placement Menu
        self.object_frame.host_placement_button.config(command=self.object_frame.host_placement_menu)
        self.object_frame.router_placement_button.config(command=self.object_frame.router_placement_menu)

        # Configuration Menu
        # TODO actually do these things in the Network
        self.object_frame.delete_component_button.config(command=self.object_frame.deletion_prompt)
        self.object_frame.set_application_button.config(command=self.object_frame.set_application_menu)
        self.object_frame.start_sending_button.config(command=self.object_frame.start_sending_menu)
        self.object_frame.add_interface_button.config(command=self.object_frame.add_interface_menu)
        self.object_frame.connect_button.config(command=self.object_frame.connect_menu)
        self.object_frame.disconnect_button.config(command=self.object_frame.disconnect_interface_menu)