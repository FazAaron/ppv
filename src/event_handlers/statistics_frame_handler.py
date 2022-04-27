"""
This module makes StatisticsFrameHandler objects available for use when imported
"""
from src.graphic_handlers.statistics_frame import StatisticsFrame
from src.utils.logger import Logger


class StatisticsFrameHandler:

    def __init__(self, statistics_frame: StatisticsFrame, logger: Logger) -> None:
        self.statistics_frame: StatisticsFrame = statistics_frame
        self.logger: Logger = logger

    def update_labels(self, packets_sent: int, packets_dropped: int) -> None:
        """
        Updates the values in the statistics_frame

        Parameters:
        packets_sent    (int): The total Packets sent
        packets_dropped (int): The total Packets dropped
        """
        self.statistics_frame.update_labels(packets_sent, packets_dropped)

    def reset_statistics(self) -> None:
        """
        Resets the statistics in the statistics_frame
        """
        self.statistics_frame.update_labels(packets_sent=0, packets_dropped=0)
