from itertools import islice
from kulka.response.responsepacket import response_packet_parser
from kulka.response.asyncpacket import async_packet_parser


def parser(data):
    for consumed, _ in enumerate(data):
        for func in [response_packet_parser, async_packet_parser]:
            response = func(islice(data, consumed, None))

            if response is not None:
                return response, consumed + response.size

    raise ValueError()
