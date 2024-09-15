import json

class Iperf3Stream:
    def __init__(self):
        self.omitted = True
        self.sender = False
        self.seconds = 0.0
        self.start = 0.0
        self.end = 0.0
        self.bps = 0.0
        self.bytes = 0
        
        # Only exist if sender = true
        self.retransmits = 0
        
        self.snd_cwnd = 0
        #self.snd_wnd = 0

        self.rtt = 0
        self.rttvar = 0
        self.pmtu = 0

    def parse(self, jsonfile: json):
        self.sender = jsonfile["sum"]["sender"]
        self.omitted = jsonfile["sum"]["omitted"]
        self.seconds = jsonfile["sum"]["seconds"]
        self.start = jsonfile["sum"]["start"]
        self.bps = jsonfile["sum"]["bits_per_second"]
        self.bytes = jsonfile["sum"]["bytes"]
        self.end = jsonfile["sum"]["end"]

        # Sender statistics
        if self.sender:
            self.retransmits = jsonfile["sum"]["retransmits"]

            self.snd_cwnd = jsonfile["streams"][0]["snd_cwnd"]
            #self.snd_wnd = jsonfile["streams"][0]["snd_wnd"]

            self.rtt = jsonfile["streams"][0]["rtt"]
            self.rttvar = jsonfile["streams"][0]["rttvar"]
            self.pmtu = jsonfile["streams"][0]["pmtu"]

class Iperf3DataTCP:
    def __init__(self):
        # True = Uploadtest, False = Downloadtest
        self.is_upload = False
        
        # Test type
        self.target_bps = 0.0
        self.duration = 0.0
        self.interval = 0
        self.cookie = ""
        self.num_streams = 0
        
        # Sender statistics
        self.bps = 0.0
        self.retransmits = 0
        self.bytes = 0
        self.max_snd_cwnd = 0
        self.max_rtt = 0
        self.min_rtt = 0
        self.mean_rtt = 0
        
        # Receiver statistics
        self.bps_received = 0.0
        self.bytes_received = 0

        #self.sender_intervals = []
        #self.receiver_intervals = []
        #self.relevant_intervals = []
        self.download_streams = []
        self.upload_streams = []
        self.server_streams = []
        self.client_streams = []
        
    
    
    def parse(self, jsonfile: json):
        self.is_upload          = jsonfile['end']['streams'][0]['sender']['sender']
        
        # Some generic test info
        self.target_bps         = jsonfile['start']['target_bitrate']
        self.num_streams        = jsonfile['start']['test_start']['num_streams']
        self.duration           = jsonfile['start']['test_start']['duration']
        self.interval           = jsonfile['start']['test_start']['interval']
        self.cookie             = jsonfile['start']['cookie']
        
        # Sender statistics. Depend on wether test is upload- or download test
        # TODO: This only works for one stream! If the iperf3 test had multiple streams
        #       the others will be ignored. This should be fixed in the future.
        if self.is_upload:
            send_stats = jsonfile['end']['streams'][0]['sender']
        else:
            send_stats = jsonfile['server_output_json']['end']['streams'][0]['sender']
            
        self.bps            = send_stats['bits_per_second']
        self.retransmits    = send_stats['retransmits']
        self.max_snd_cwnd   = send_stats['max_snd_cwnd']
        self.max_rtt        = send_stats['max_rtt']
        self.min_rtt        = send_stats['min_rtt']
        self.mean_rtt       = send_stats['mean_rtt']
        
        if not self.is_upload:
            recv_stats = jsonfile['end']['streams'][0]['receiver']
        else:
            recv_stats = jsonfile['server_output_json']['end']['streams'][0]['receiver']
        
        self.bps_received           = recv_stats['bits_per_second']
        self.bytes_received         = recv_stats['bytes']
 
        # Gather individual stream data
        #for j in jsonfile["intervals"]:
        #    s = Iperf3Stream()
        #    s.parse(j)
        #    if s.sender:
        #        self.sender_intervals.append(s)
        #    else:
        #        self.receiver_intervals.append(s)
        #for j in jsonfile["server_output_json"]["intervals"]:
        #    s = Iperf3Stream()
        #    s.parse(j)
        #    if s.sender:
        #        self.sender_intervals.append(s)
        #    else:
        #        self.receiver_intervals.append(s)
            
        for j in jsonfile['intervals']:
            s = Iperf3Stream()
            s.parse(j)
            self.client_streams.append(s)
            
        for j in jsonfile["server_output_json"]["intervals"]:
            s = Iperf3Stream()
            s.parse(j)
            self.server_streams.append(s)

class Iperf3DataUDP:
    def __init__(self):
        self.is_upload = False
        
        # Test type
        self.target_bps = 0.0
        self.duration = 0.0
        self.interval = 0
        self.cookie = ""
        self.num_streams = 0
        
        self.jitter_ms = 0.0
        self.bps = 0.0
        self.bytes = 0
        self.packets = 0
        self.lost_percent = 0.0
        self.lost_packets = 0
        self.out_of_order = 0
        
    def parse(self, jsonfile: json):
        #print(jsonfile['end']['streams'][0]['udp'])
        self.is_upload          = jsonfile['end']['streams'][0]['udp']['sender']
        
        # Some generic test info
        self.target_bps         = jsonfile['start']['target_bitrate']
        self.num_streams        = jsonfile['start']['test_start']['num_streams']
        self.duration           = jsonfile['start']['test_start']['duration']
        self.interval           = jsonfile['start']['test_start']['interval']
        self.cookie             = jsonfile['start']['cookie']
        
        # Sender statistics. Depend on wether test is upload- or download test
        # TODO: This only works for one stream! If the iperf3 test had multiple streams
        #       the others will be ignored. This should be fixed in the future.
        if self.is_upload:
            send_stats = jsonfile['end']['streams'][0]['udp']
        else:
            send_stats = jsonfile['server_output_json']['end']['streams'][0]['udp']
            
        self.bps            = send_stats['bits_per_second']
        # Jitter is always in the same place
        self.jitter_ms      = jsonfile['end']['streams'][0]['udp']['jitter_ms']
        self.bytes          = send_stats['bytes']
        self.packets        = send_stats['packets']
        self.lost_percent   = send_stats['lost_percent']
        self.lost_packets   = send_stats['lost_packets']
        self.out_of_order   = send_stats['out_of_order']
        
        if not self.is_upload:
            recv_stats = jsonfile['end']['streams'][0]['udp']
        else:
            recv_stats = jsonfile['server_output_json']['end']['streams'][0]['udp']
        
        self.bps_received           = recv_stats['bits_per_second']
        self.bytes_received         = recv_stats['bytes']