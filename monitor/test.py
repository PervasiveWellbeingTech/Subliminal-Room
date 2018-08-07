import libs
import serial
import platform

import zephyr
from zephyr.testing import simulation_workflow


def callback(value_name, value):
    print(value_name, value)

def main():
    zephyr.configure_root_logger()

    serial_port_dict = {"Darwin": "/dev/cu.BHBHT001931-iSerialPort1",
                        "Windows": 23}

    serial_port = serial_port_dict[platform.system()]
    ser = serial.Serial(serial_port)

    zephyr.configure_root_logger()

    collector = MeasurementCollector()

    rr_signal_analysis = BioHarnessSignalAnalysis([], [collector.handle_event])

    signal_packet_handler_bh = BioHarnessPacketHandler([collector.handle_signal, rr_signal_analysis.handle_signal],
                                                       [collector.handle_event])

    payload_parser = MessagePayloadParser([signal_packet_handler_bh.handle_packet])
    # payload_parser = MessagePayloadParser([signal_packet_handler_bh.handle_packet,
                                               # signal_packet_handler_hxm.handle_packet])

    message_parser = MessageFrameParser(payload_parser.handle_message)


    delayed_stream_thread = DelayedRealTimeStream(collector, callbacks, 1.2)
    # delayed_stream_thread = DelayedRealTimeStream(collector, callbacks, 1)


    protocol = BioHarnessProtocol(ser, [message_parser.parse_data])
    # protocol.enable_periodic_packets()
    protocol.enable_breathing_waveform()


    delayed_stream_thread.start()

    try:
        protocol.run()
    except EOFError:
        pass

    delayed_stream_thread.terminate()
    delayed_stream_thread.join()


if __name__ == "__main__":
    main()
