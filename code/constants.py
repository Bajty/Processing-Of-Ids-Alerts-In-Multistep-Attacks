HEADER = [
    "timestamp",
    "sig_generator",
    "sid",
    "sig_rev",
    "rule_name",
    "proto",
    "from_addr",
    "from_port",
    "to_addr",
    "to_port",
    "ethsrc",
    "ethdst",
    "ethlen",
    "tcpflags",
    "tcpseq",
    "tcpack",
    "tcpln",
    "tcpwindow",
    "ttl",
    "tos",
    "id",
    "dgmlen",
    "iplen",
    "icmptype",
    "icmpcode",
    "icmpid",
    "icmpseq",
    "default"
]

INPUTS_PATH = 'inputs/'
BENIGN_INPUTS = 'benign/'
CLASSES = 'classes/'
PERC_DIFF_MIN = 0.0
PERC_DIFF_MAX = 2.0
COUNT_MIN = 0
COUNT_MAX_HOURS = 24

SUB_MEAN_OPTIONS = [True, False]
FROM_MEAN_OPTIONS = ['all_days', 'benign_days']
ADDR_OPTIONS = ['from_addr', 'to_addr']
TIME_DELTA_FUNCTION_OPTIONS = ['+', '-']
