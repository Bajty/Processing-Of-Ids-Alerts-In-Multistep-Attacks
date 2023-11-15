import json
import uuid

import numpy as np

from tasks import time_diff


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


class E:
    def __init__(
            self, timestamp=None, datetime=None, sig_generator=None, sid=None, sig_rev=None, rule_name=None, proto=None,
            from_addr=None, from_port=None, to_addr=None, to_port=None,
            ethsrc=None, ethdst=None, ethlen=None, tcpflags=None, tcpseq=None, tcpack=None, tcpln=None,
            tcpwindow=None, ttl=None, tos=None, id=None, dgmlen=None, iplen=None,
            icmptype=None, icmpcode=None, icmpid=None, icmpseq=None, default=None
    ):
        self.datetime = datetime
        self.timestamp = timestamp
        self.sig_generator = sig_generator
        self.sid = sid
        self.sig_rev = sig_rev
        self.rule_name = rule_name
        self.proto = proto
        self.from_addr = from_addr
        self.from_port = from_port
        self.to_addr = to_addr
        self.to_port = to_port
        self.ethsrc = ethsrc
        self.ethdst = ethdst
        self.ethlen = ethlen
        self.tcpflags = tcpflags
        self.tcpseq = tcpseq
        self.tcpack = tcpack
        self.tcpln = tcpln
        self.tcpwindow = tcpwindow
        self.ttl = ttl
        self.tos = tos
        self.id = id
        self.dgmlen = dgmlen
        self.iplen = iplen
        self.icmptype = icmptype
        self.icmpcode = icmpcode
        self.icmpid = icmpid
        self.icmpseq = icmpseq
        self.default = default

    def __str__(self) -> str:
        return str(self.datetime) + ", " + str(self.from_addr) + ", " + str(self.to_addr) + ", " + str(
            self.from_port) + ", " + str(self.to_port) + ", " + str(self.rule_name) + ", " + str(self.sid)

    def __repr__(self) -> str:
        return str(self.datetime) + ", " + str(self.from_addr) + ", " + str(self.to_addr) + ", " + str(
            self.from_port) + ", " + str(self.to_port) + ", " + str(self.rule_name) + ", " + str(self.sid)

    def serialize(self) -> dict:
        dict = self.__dict__.copy()
        dict['tcpflags'] = str(['tcpflags'])
        dict['datetime'] = dict['datetime'].strftime('%Y-%m-%d %X')
        dict = {k: None if not v else str(v) for k, v in dict.items()}

        return dict

    # aggregated meta-alert


class A:
    def __init__(self):
        self.sid = None
        self.class_name = None
        self.rule_name = None
        self.from_addr = set()
        self.to_addr = set()
        self.from_port = set()
        self.to_port = set()
        self.from_addr_count = 0
        self.to_addr_count = 0
        self.from_port_count = 0
        self.to_port_count = 0
        self.start_time = None
        self.end_time = None
        self.mean = None
        self.median = None
        self.std = None
        self.min = None
        self.max = None
        self.events = []
        self.uuid = uuid.uuid4()

    def __str__(self):
        return str(self.sid) + ", " + str(self.from_addr) + ", " + str(self.to_addr) + ", " + str(
            self.from_port) + ", " + str(self.to_port) + ", " + str(self.rule_name) + ", " + str(
            self.start_time) + ", " + str(self.end_time) + ", " + str(len(self.events))

    def __repr__(self) -> str:
        return str(self.sid) + ", " + str(self.from_addr) + ", " + str(self.to_addr) + ", " + str(
            self.from_port) + ", " + str(self.to_port) + ", " + str(self.rule_name) + ", " + str(
            self.start_time) + ", " + str(self.end_time) + ", " + str(len(self.events))

    def __eq__(self, other):
        if self.sid == other.sid and self.from_addr == other.from_addr and self.to_addr == other.to_addr and \
                self.from_port == other.from_port and self.to_port == other.to_port and \
                self.start_time == other.start_time and self.end_time == other.end_time and self.events == other.events:
            return True
        else:
            return False

    def compute_stats(self):
        times = []
        for event in self.events:
            times.append(event.datetime)
        times = np.array(times)
        delta_times = np.diff(times)
        delta_times = [x.total_seconds() for x in delta_times]
        if len(delta_times) > 1:
            self.mean = np.mean(delta_times)
            self.median = np.median(delta_times)
            self.std = np.std(delta_times)
            self.min = np.min(delta_times)
            self.max = np.max(delta_times)

    def serialize(self) -> dict:
        dict = self.__dict__.copy()
        dict['uuid'] = str(dict['uuid'])
        dict['class_name'] = str(dict['class_name'])
        dict['start_time'] = dict['start_time'].strftime('%Y-%m-%d %X')
        dict['end_time'] = dict['end_time'].strftime('%Y-%m-%d %X')
        dict['events'] = [event.serialize() for event in self.events]
        dict['from_addr'] = list(self.from_addr)
        dict['to_addr'] = list(self.to_addr)
        dict['from_port'] = list(self.from_port)
        dict['to_port'] = list(self.to_port)
        return dict


def create_events(filtered_data) -> [E]:
    all_filtered_events = []
    for index, row in filtered_data.iterrows():
        event = E(
            rule_name=row['rule_name'],
            from_addr=row['from_addr'],
            to_addr=row['to_addr'],
            from_port=row['from_port'],
            to_port=row['to_port'],
            sid=row['sid'],
            datetime=row['datetime'],
            proto=row['proto'],
            tcpflags=row['tcpflags'],
            tos=row['tos'],
            sig_rev=row['sig_rev'],
            default=row['default'],
            icmpseq=row['icmpseq'],
            dgmlen=row['dgmlen'],
            ethdst=row['ethdst'],
            ethlen=row['ethlen'],
            ethsrc=row['ethsrc'],
            icmpid=row['icmpid'],
            tcpack=row['tcpack'],
            tcpseq=row['tcpseq'],
            icmpcode=row['icmpcode'],
            icmptype=row['icmptype'],
            tcpwindow=row['tcpwindow'],
            timestamp=row['timestamp'],
            sig_generator=row['sig_generator'],
            iplen=row['iplen'],
            tcpln=row['tcpln'],
            ttl=row['ttl'],
            id=row['id'],
        )
        all_filtered_events.append(event)
    return all_filtered_events


def aggregtion(all_filtered_events, delta, classes):
    agg_events = []
    actual = []
    for event in all_filtered_events:
        added = False
        for agg_event in actual:
            if (event.datetime >= agg_event.end_time and time_diff(event.datetime, agg_event.end_time) <= delta) or (
                    event.datetime >= agg_event.start_time and event.datetime <= agg_event.end_time):
                if ((event.from_addr in agg_event.from_addr and len(agg_event.from_addr) == 1) or (
                        event.to_addr in agg_event.to_addr and
                        len(agg_event.to_addr) == 1)) and event.sid == agg_event.sid:
                    added = True
                    agg_event.from_addr.add(event.from_addr)
                    agg_event.to_addr.add(event.to_addr)
                    agg_event.from_port.add(event.from_port)
                    agg_event.to_port.add(event.to_port)
                    agg_event.end_time = event.datetime
                    agg_event.events.append(event)
                    break
            else:
                agg_events.append(agg_event)
                actual.remove(agg_event)
        if not added:
            a = A()
            a.from_addr.add(event.from_addr)
            a.class_name = classes.loc[classes['sid'] == event.sid]['stage'].values[0]
            a.rule_name = event.rule_name
            a.to_addr.add(event.to_addr)
            a.sid = event.sid
            a.from_port.add(event.from_port)
            a.to_port.add(event.to_port)
            a.end_time = event.datetime
            a.start_time = event.datetime
            a.events.append(event)
            actual.append(a)

    for agg_event in actual:
        agg_events.append(agg_event)

    for agg_event in agg_events:
        agg_event.from_addr_count = len(agg_event.from_addr)
        agg_event.to_addr_count = len(agg_event.to_addr)
        agg_event.from_port_count = len(agg_event.from_port)
        agg_event.to_port_count = len(agg_event.to_port)
        agg_event.events.sort(key=lambda u: u.datetime)

    agg_events = sorted(agg_events, key=lambda agg_event: (agg_event.start_time, agg_event.end_time))
    for agv in agg_events:
        agv.events.sort(key=lambda u: u.datetime)
        agv.compute_stats()

    return agg_events
