"""
A namespace for oscilloscope string commands
"""

import enum
query = lambda cmd : cmd  + "?"

def add_arg(cmd, arg):
    """
    Add an argument to a command string

    Args:
        cmd (str)
        arg (str)
    """
    if not isinstance(arg,str):
        arg = str(arg)

    if len(cmd.split()) != 1:
        cmd = cmd + "," + arg
    else:
        cmd = cmd + " " + arg
    return cmd


def concat(*cmd):
    """
    Combine several commands

    Args:
        cmd: list of commands

    Returns:
        str
    """
    cmd = list(cmd)
    cmd[0].replace(":","")
    concated = cmd[0] + ";"
    cmd.remove(cmd[0])
    for c in cmd:
        concated += ":" + str(c) + "; "
    return concated


def decode(response):
    """
    Decode osciloscope response to a nice string

    Args:
        response (bytes): recieved from oscilloscope
    """
    if response is None:
        return response
    if isinstance(response,bytes):
        response = response.decode("utf8")
    response = clean_response(response)
    if not response or response == "\r\n" or response == "\n\r":
        response = None
    return response


def clean_response(response):
    """
    Remove some remainders from the resulting scope response

    Args:
        response (str): response from the scope

    Returns:

    """

    response = response.replace("\r\n>", "")
    response = response.replace("\r\n", "")
    response = response.replace("\n\r", "")
    response = response.replace(">", "")
    response = response.replace("<", "")
    response = response.replace("\n", "")
    return response


def parse_curve_data(header, curve):
    """
    Make sense out of that what is returned by CURVE

    Args:
        header (dict): a parsed header
        curv (str): returned by CURVE?

    Returns:
        tuple: np.ndarray xs, np.ndarray values
    """

    # Value in YUNit units = ((curve_in_dl - YOFf) * YMUlt) + YZEro

    curve.replace("#", "")


def encode(cmd):
    """
    Append trailing return carriage and convert
    to bytes

    Args:
        cmd (str): command to be sanitized

    """

    if not cmd.endswith("\r\n"):
        cmd = cmd + "\r\n"

    # python3 needs byterepresentation for socket
    return cmd.encode("utf8")

def histbox_coordinates(left, top, right, bottom):
    """
    Create a string for the box cordinates for the
    histo

    Args:
        left (int):
        top (int):
        right (int):
        bottom (int):

    Returns:

    """
    command = concat([left, top, right, bottom])
    return command


def parse_custom_wf_header(head):
    """
    Parse a waveform header send by our custom WF_HEADER command
    The reason why we are not using WFM:Outpre is that the documentation
    was not so sure about how its response might look

    Args:
        head (str): the result of a WF_HEADER command

    Returns:
        dict
    """
    head = head.split(";")
    keys = ["bytno", "enc", "npoints", "xzero", "xincr", "yzero", "yoff", \
     "ymult", "xunit", "yunit"]

    assert len(head) == len(keys), "Cannot read out all the header info I want!"
    parsed = dict(zip(keys,head))
    for k in parsed:
        try:
            f = float(parsed[k])
            parsed[k] = f
        except ValueError:
            continue


        # get rid of extra " in units
        parsed["xunit"] = parsed["xunit"].replace('"','')
        parsed["yunit"] = parsed["yunit"].replace('"', '')

    return parsed

#
# COMMANDS!
#
#

WHOAMI = "*IDN?"
SOURCE = "DATa:SOUrce"
DATA_START = "DATa:STARt"
DATA_STOP = "DATa:STOP"
DATA_STARTQ = query(DATA_START)
DATA_STOPQ = query(DATA_STOP)
SOURCEQ = query(SOURCE)
HISTSTART = "HIStogram:STARt"
HISTEND = "HIStogram:END"
HISTDATA = "HIStogram:DATa?"
WAVEFORM = "WAVFrm?"
CURVE = "CURVe?"
WF_OUTPREQ = "WFMOutpre?"
WF_XINCRQ = "WFMOutpre:XINcr?"
WF_XUNITQ = "WFMOutpre:XUNit?"
WF_XZEROQ = "WFMOutpre:XZEro?"
WF_YOFFQ = "WFMOutpre:YOFf?"
WF_YZEROQ = "WFMOutpre:YZEro?"
WF_YMULTQ = "WFMOutpre:YMUlt?"
WF_YUNITQ = "WFMOutpre:YUNit?"
WF_ENC = "WFMOutpre:ENCdg"
WF_ENCQ = query(WF_ENC)
WF_NPOINTS = "WFMOutpre:NR_Pt"
WF_NPOINTSQ = query(WF_NPOINTS)
ACQUIRE = "ACQuire"
ACQUIRE_FAST_STATE = "ACQuire:FASTAcq:STATE"
ACQUIRE_MAX_SAMPLERATEQ = "ACQuire:MAXSamplerate?"
RUN = "ACQuire:STATE"
WF_BYTQ = "WFMOutpre:BYT_Nr?" # 1 or 2 for single or double prec
ACQUIRE_STOP = "ACQuire:STOPAfter"
HISTBOX = "HIStogram:BOX"
TRG_RATEQ = "TRIGger:FREQuency?"
# command arguments

RUN_CONTINOUS = "RUNSTop"
RUN_SINGLE = "SEQuence"
SNAP = "SNAP"
DATA = "DATA"
OFF = "0"
ON = "1"
CH1,CH2,CH3,CH4 = "CH1", "CH2", "CH3", "CH4"
ASCII = "ASCii"
BINARY = "BINary"
SINGLE_ACQUIRE = "1"

# combined commands

WF_HEADER = concat(WF_BYTQ, WF_ENCQ, WF_NPOINTSQ, WF_XZEROQ, WF_XINCRQ,\
                   WF_YZEROQ, WF_YOFFQ, WF_YMULTQ,\
                   WF_XUNITQ, WF_YUNITQ)