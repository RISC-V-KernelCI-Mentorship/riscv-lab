from events.source.events_source import EventsSource

class ExampleEventsSource(EventsSource):
    
    def __init__(self):
        self.__returned_response = False

    def poll_events(self, timestamp: str, kind: str, arch: str) -> list[dict[str, str]]:
        response = []
        if not self.__returned_response:
            response = [{
                "id": "67d750c29e4e84ff5b51a65e",
                "node": {
                    "artifacts": {
                        "kernel": "http://mon.kernelci.org:3000/kbuild-gcc-12-riscv-67d74cdc9e4e84ff5b51a5d6/Image",
                        "kselftest_tar_gz": "http://mon.kernelci.org:3000/kbuild-gcc-12-riscv-67d74cdc9e4e84ff5b51a5d6/kselftest.tar.gz"
                    }
                },
                "timestamp": "2025-03-16T22:29:22.598000"
            }]
            self.__returned_response = True 
        return response
