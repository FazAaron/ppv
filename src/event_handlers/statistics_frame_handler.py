"""
This module makes StatisticsFrameHandler objects available for use when imported
"""
from src.graphic_handlers.statistics_frame import StatisticsFrame


class StatisticsFrameHandler:
    """
    The class handling any access to the StatisticsFrame object

    Data members:
    statistics_frame (StatisticsFrame): The Frame itself to access
    """

    def __init__(self, statistics_frame: StatisticsFrame) -> None:
        self.statistics_frame: StatisticsFrame = statistics_frame

        # Setup starting values
        self.update_labels(0, 0, 0)

    def update_labels(self,
                      packets_sent: int,
                      packets_dropped: int,
                      packets_received: int,
                      ) -> None:
        """
        Updates the values in the statistics_frame

        Parameters:
        packets_sent    (int): The total Packets sent
        packets_dropped (int): The total Packets dropped
        """
        sent: str = f"Packets sent:     {packets_sent}"
        dropped: str = f"Packets dropped:  {packets_dropped}"
        received: str = f"Packets received: {packets_received}"
        self.statistics_frame.update_labels(sent, dropped, received)
