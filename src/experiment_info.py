#--------------------------------------------------------------------------
# File and Version Information:
#  $Id:$
#
# Description:
#  The API for inquering various information about instruments and
#  experiments registered at PCDS.
#
#------------------------------------------------------------------------

"""
The API for inquering various information about instruments and
experiments registered at PCDS.

This software was developed for the LCLS project.  If you use all or
part of it, please give an appropriate acknowledgment.

This is orinally from the RegDB package. This was copied into the
CalibManager package to eliminate the RegDB ( and hence MySQL dependency ) 

@version $Id:$

@author Igor Gaponenko
"""
from __future__ import print_function
from __future__ import division

#------------------------------
#  Module's version from SVN --
#------------------------------
__version__ = "$Revision:$"
# $Source:$

#--------------------------------
#  Imports of standard modules --
#--------------------------------

import sys
import time
import logging
import requests

logger = logging.getLogger(__name__)

server_url_prefix = "https://pswww.slac.stanford.edu/ws/lgbk/"

def active_experiment(instr, station=0):
    """
    Get a record for the latest experiment activated for the given instrument.
    The function will return a tuple of:

      (instrument, experiment, activated, activated_local_str, user)

    Where:

      instrument - the name of the instrument

      experiment - the name of the experiment

      activated_local_str - a human-readable repreentation of the activation time
                            in the local timezone

      user - a UID of a user who's requested the activation

    The function wil return None if no record database was found for the requested
    instrument name. This may also be an indication that the instrument name is not valid.
    """

    resp = requests.get(server_url_prefix + "lgbk/ws/activeexperiment_for_instrument_station", params={"instrument_name": instr, "station": station})
    resp.raise_for_status()
    swinfo = resp.json().get("value", None)
    if not swinfo:
        return None

    return (instr, swinfo["name"], swinfo["switch_time"], swinfo["requestor_uid"])

def experiment_runs(instr, exper=None, station=0):
    """
    Return a list of runs taken in a context of the specified experiment.

    Each run will be represented with a dictionary with the following keys:
      'num'             : a run number
      'begin_time_unix' : a UNIX timestamp (32-bits since Epoch) for the start of the run
      'end_time_unix'   : a UNIX timestamp (32-bits since Epoch) for the start of the run.

    NOTES:

      1. if no experiment name provided to the function then  the current
      experiment for the specified station will be assumed. The station parameter
      will be ignored if the experiment name is provided.

      2. if the run is still going on then its 'end_time_unix' will be set to None

    PARAMETERS:

      @param instr: the name of the instrument
      @param exper: the optional name of the experiment (default is the current experiment of the instrument)
      @param station: the optional station number (default is 0)
      @return: the list of run descriptors as explained above

    """

    if exper is None:
        e = active_experiment(instr, station)[1]
        if e is None: return []
    else:
        e = exper

    logger.debug("Looking for runs for experiment is %s", e)
    runs = []
    resp = requests.get(server_url_prefix + "/lgbk/" + e + "/ws/runs_for_calib")
    resp.raise_for_status()
    rinfos = resp.json().get("value", None)
    if not rinfos:
        return runs
    for rinfo in rinfos:
        run = {}
        run["num"] = rinfo["run_num"]
        run["begin_time_unix"] = rinfo["begin_time"]
        if "end_time" in rinfo:
            run["end_time_unix"] = rinfo["end_time"]
        if "type" in rinfo:
            run["type"] = rinfo["type"]
        runs.append(run)

    return runs

def unique_detector_names():

    """
    Return a list of all known detector names configured in the DAQ system
    accross all known experiments and runs
    """
    resp = requests.get(server_url_prefix + "/lgbk/ws/get_params_matching_prefix?prefix=DAQ_Detectors&prefix=DAQ%20Detectors")
    resp.raise_for_status()
    detectors = resp.json().get("value", None)
    if not detectors:
        return []
    return [x.replace("DAQ_Detectors/", "").replace("DAQ Detectors/", "") for x in detectors]


def detectors(instr, exper, run):

    """
    Return a list of detector names configured in the DAQ system for a particular
    experiment and a run.

    PARAMETERS:

      @param instr: the name of the instrument
      @param exper: the name of the experiment
      @param run: the run number
      @return: the list of detector names

    """
    resp = requests.get(server_url_prefix + "/lgbk/" + exper + "/ws/" + str(run) + "/get_params_matching_prefix?prefix=DAQ_Detectors&prefix=DAQ%20Detectors")
    resp.raise_for_status()
    detectors = resp.json().get("value", None)
    if not detectors:
        return []
    return [x.replace("DAQ_Detectors/", "").replace("DAQ Detectors/", "") for x in detectors]

def run_attributes(instr, exper, run, attr_class=None):

    """
    Return a list of attrubutes of the specified run of an experiment.
    The result set may be (optionally) narrowed to a class.
    Each entry in the result list will be represented by a dictionary of
    the following keys:

      'class' : the class of the attribute
      'name'  : the name of the attribute within a scope of its class
      'descr' : the descrption of the attribute (can be empty)
      'type'  : the type of the attribute's value ('INT','DOUBLE' or 'TEXT')
      'val'   : the value of the attribute (None if no value was set)

    PARAMETERS:

      @param instr: the name of the instrument
      @param exper: the name of the experiment
      @param run: the run number
      @param attr_class: the name of the attribute's class (optional)
      @return: the list of dictinaries representing attributes

    """

    resp = requests.get(server_url_prefix + "/lgbk/" + exper + "/ws/" + str(run) + "/daq_run_params")
    resp.raise_for_status()
    run_attrs = resp.json().get("value", None)
    if not run_attrs:
        return []
    def __guesstype__(v):
        if isinstance(v, int):
            return "INT"
        elif isinstance(v, float):
            return "DOUBLE"
        else:
            return "TEXT"
    if attr_class:
        return [{"name": k.split("/")[0], "class": "/".join(k.split("/")[1:]), "val": v, "type": __guesstype__(v), "descr": ""} for k, v in run_attrs.items() if k.startswith(attr_class+"/")]
    else:
        return [{"name": k.split("/")[0], "class": "/".join(k.split("/")[1:]), "val": v, "type": __guesstype__(v), "descr": ""} for k, v in run_attrs.items()]


def calibration_runs(instr, exper, runnum=None):

    """
    Return the information about calibrations associated with the specified run
    (or all runs of the experiment if no specific run number is provided).

    The result will be packaged into a dictionary of the following type:

      <runnum> : { 'calibrations' : [<calibtype1>, <calibtype2>, ... ] ,
                   'comment'      :  <text>
                 }

    Where:

      <runnum>     : the run number
      <calibtype*> : the name of the calibration ('dark', 'flat', 'geometry', etc.)
      <text>       : an optional comment for the run

    PARAMETERS:

      @param instr: the name of the instrument
      @param exper: the name of the experiment
      @param run: the run number (optional)

    """

    run_numbers = []
    if runnum is None:
        run_numbers = [run['num'] for run in experiment_runs(instr, exper)]
    else:
        run_numbers = [runnum]


    result = {}

    for runnum in run_numbers:
        run_info = {'calibrations': [], 'comment':''}
        for attr in run_attributes(instr, exper, runnum, 'Calibrations'):
            if   attr['name'] == 'comment': run_info['comment'] = attr['val']
            elif attr['val']              : run_info['calibrations'].append(attr['name'])
        result[runnum] = run_info

    return result

# -------------------------------
# Here folow a couple of examples
# -------------------------------

if __name__ == "__main__" :

    print(active_experiment("XCS"))
    print(active_experiment("CXI", 0))
    print(active_experiment("CXI", 1))
    print(experiment_runs("XCS"))
    print(experiment_runs("DIA", "diadaq13"))
    print(unique_detector_names())
    print(detectors("XPP", "xppn4116", 21))

    for attr in run_attributes('CXI', 'cxic0213', 215):
        attr_val = attr['val']
        if attr_val is None: attr_val = ''
        print("  %17s | %30s | %10s | %11s | %s" % (attr['class'],attr['name'],attr['type'],attr['descr'][:11],str(attr_val),))

    print("Only Calibrations")
    for attr in run_attributes('CXI', 'cxic0213', 215, "Calibrations"):
        attr_val = attr['val']
        if attr_val is None: attr_val = ''
        print("  %17s | %30s | %10s | %11s | %s" % (attr['class'],attr['name'],attr['type'],attr['descr'][:11],str(attr_val),))

    entries = calibration_runs('CXI', 'cxic0213')
    for run in sorted(entries.keys()):
        info = entries[run]
        comment = info['comment']
        calibtypes =  ' '.join([calibtype for calibtype in info['calibrations']])
        # report runs which have at least one calibratin type
        if calibtypes:
            print("   %4d  |  %-40s  |  %s"  % (run, calibtypes, comment,))
