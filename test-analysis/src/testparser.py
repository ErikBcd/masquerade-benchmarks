import json

class TCPStreamData:
    def __init__(self):
        self.seconds = 0.0
        self.start = 0.0
        self.end = 0.0
        
        self.bps_received = 0.0
        
        self.retransmits = 0
        self.snd_cwnd = 0
        self.rtt = 0
        self.rttvar = 0
        self.pmtu = 0
    
    def parse(self, sender, receiver):
        self.bps_received = receiver['sum']['bits_per_second']
        self.seconds = receiver['sum']['seconds']
        self.start = receiver['sum']['start']
        self.end = receiver['sum']['end']
        
        self.retransmits    = sender['sum']['retransmits']
        self.snd_cwnd       = sender['streams'][0]['snd_cwnd']
        self.rtt            = sender['streams'][0]['rtt']
        self.rttvar         = sender['streams'][0]['rttvar']
        self.pmtu           = sender['streams'][0]['pmtu']
        

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
        
        self.bps_received = 0.0
        self.retransmits = 0
        self.max_snd_cwnd = 0
        self.max_rtt = 0
        self.min_rtt = 0
        self.mean_rtt = 0

        self.intervals = []

    def parse(self, jsonfile: json):
        self.is_upload          = jsonfile['end']['sum_sent']['sender']
        
        # Some generic test info
        self.target_bps         = jsonfile['start']['target_bitrate']
        self.num_streams        = jsonfile['start']['test_start']['num_streams']
        self.duration           = jsonfile['start']['test_start']['duration']
        self.interval           = jsonfile['start']['test_start']['interval']
        self.cookie             = jsonfile['start']['cookie']
        
        self.bps_received       = jsonfile['end']['sum_received']['bits_per_second']
        self.retransmits        = jsonfile['end']['sum_sent']['retransmits']
        
        # Only the sender side has these statistics
        if self.is_upload:
            self.max_snd_cwnd   = jsonfile['end']['streams'][0]['sender']['max_snd_cwnd']
            self.max_rtt        = jsonfile['end']['streams'][0]['sender']['max_rtt']
            self.min_rtt        = jsonfile['end']['streams'][0]['sender']['min_rtt']
            self.mean_rtt       = jsonfile['end']['streams'][0]['sender']['mean_rtt']
        else:
            self.max_snd_cwnd   = jsonfile['server_output_json']['end']['streams'][0]['sender']['max_snd_cwnd']
            self.max_rtt        = jsonfile['server_output_json']['end']['streams'][0]['sender']['max_rtt']
            self.min_rtt        = jsonfile['server_output_json']['end']['streams'][0]['sender']['min_rtt']
            self.mean_rtt       = jsonfile['server_output_json']['end']['streams'][0]['sender']['mean_rtt']
        
        # Parse individual intervals
        server_intervals = len(jsonfile["server_output_json"]["intervals"])
        client_intervals = len(jsonfile['intervals'])
        #if client_intervals != server_intervals:
        #    print("WARNING: Intervals mismatch! Client len: " + str(client_intervals) + " Server len: " + str(server_intervals))
        
        interval_num = min(server_intervals, client_intervals)
        
        for i in range(2, interval_num):
            s = TCPStreamData()
            if self.is_upload:
                s.parse(sender=jsonfile['intervals'][i], receiver=jsonfile["server_output_json"]["intervals"][i])
            else:
                s.parse(sender=jsonfile["server_output_json"]["intervals"][i], receiver=jsonfile['intervals'][i])
            self.intervals.append(s)
        
class UDPStreamData:
    def __init__(self):
        self.seconds = 0.0
        self.start = 0.0
        self.end = 0.0
        
        self.bps_received = 0
        
        self.lost_packets = 0
        self.lost_percent = 0.0
        self.jitter_ms = 0.0
        
    def parse(self, receiver):
        self.bps_received   = receiver['sum']['bits_per_second']
        self.seconds        = receiver['sum']['seconds']
        self.start          = receiver['sum']['start']
        self.end            = receiver['sum']['end']
        
        self.lost_packets   = receiver['sum']['lost_packets']
        self.lost_percent   = receiver['sum']['lost_percent']
        self.jitter_ms      = receiver['sum']['jitter_ms']
        
class Iperf3DataUDP:
    def __init__(self):
        self.is_upload = False
        
        # Test type
        self.target_bps = 0.0
        self.duration = 0.0
        self.interval = 0
        self.cookie = ""
        self.num_streams = 0
        
        self.received_bps = 0
        
        # Upload only stats
        self.lost_packets = 0
        self.lost_percent = 0.0
        self.jitter_ms = 0.0
        
        self.intervals = []
        
    def parse(self, jsonfile: json):
        #print(jsonfile['end']['streams'][0]['udp'])
        self.is_upload          = jsonfile['end']['streams'][0]['udp']['sender']
        
        # Some generic test info
        self.target_bps         = jsonfile['start']['target_bitrate']
        self.num_streams        = jsonfile['start']['test_start']['num_streams']
        self.duration           = jsonfile['start']['test_start']['duration']
        self.interval           = jsonfile['start']['test_start']['interval']
        self.cookie             = jsonfile['start']['cookie']
        
        self.received_bps = jsonfile['end']['sum_received']['bits_per_second']
        
        if self.is_upload:
            self.lost_packets = jsonfile['end']['sum_received']['lost_packets']
            self.lost_percent = jsonfile['end']['sum_received']['lost_percent']
        self.jitter_ms = jsonfile['end']['sum_received']['jitter_ms']
        
        if not self.is_upload:
            ivals = jsonfile['intervals']
        else:
            ivals = jsonfile["server_output_json"]["intervals"]
        
        for i in range(2, len(ivals)):
            s = UDPStreamData()
            s.parse(ivals[i])
            self.intervals.append(s)
            
        
            