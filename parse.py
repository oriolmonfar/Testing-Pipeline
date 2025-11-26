from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any
import json
import logging

#Define logger print warnings or errors
logger = logging.getLogger(__name__)



@dataclass
class Test: #Dataclass for each test
    name: str
    status: str
    duration: float

@dataclass
class Session: #Dataclass for each DUT
    dut: str
    session_id: str
    tests: List[Test]

class ParseError(ValueError):
    pass


def _parse_test(obj: Dict[str, Any]) -> Test:

    """
    This function arranges the tests from the sessions in the mock data file into the dataclass Test.
    Includes error management to ensure good understanding and easy debugging.

    """

    #Check if the parameter is a dictionary
    if not isinstance(obj, dict):
        raise ParseError("test entry is not a dictionary")

    #Gets the name of the test
    name = obj.get("name")
    #Checks if "name" exists
    if name is None:
        raise ParseError (f"The test name is missing: {obj!r}")
    #Checks if "name" is a string
    elif  not isinstance(name, str):
        raise ParseError(f"The test name is not a string: {obj!r}")
    #Checks if "name" is empty
    elif name.strip() == "":
        raise ParseError(f"The test name is empty: {obj!r}")
    

    #Gets status of the test. If there is no value associated, it is set to "skipped"
    status = obj.get("status", "skipped")
    #Checks if "status" is a string
    if not isinstance(status, str):
        raise ParseError(f"The test status is not a string: {obj!r}")
    #Normalizes "status" to lower case
    status = status.lower()
    #Checks if the "status" value is one of the possible options, if not, set to "skipped"
    if status not in {"passed", "failed", "skipped"}:
        logger.warning("Unknown test status '%s' for test '%s'. Defining as 'skipped'.", status, name)
        status = "skipped"


    #Gets duration of the test. If there is no value associated, the value is set to 0.0
    raw_duration = obj.get("duration", 0.0)
    try:
        #Casts duration into float
        duration = float(raw_duration)
        #Checks if "duration" is a negative value and sets to 0.0
        if duration < 0:
            logger.warning("Negative duration %s for test %s. Setting to 0.0", raw_duration, name)
            duration = 0.0
        #Check if "duration" is valid, if not set to 0.0
    except (TypeError, ValueError):
        logger.warning("Invalid duration %r for test %s. Using 0.0", raw_duration, name)
        duration = 0.0

    #Return the test dataclass with the corresponding values
    return Test(name=name, status=status, duration=duration)


def _parse_session(obj: Dict[str, Any]) -> Session:

    """
    This function arranges the DUTs sessions in the mock data file into the dataclass Session.
    Includes error management to ensure good understanding and easy debugging.

    """

    #Check if the parameter is object/dictionary
    if not isinstance(obj, dict):
        raise ParseError("session entry is not an object/dict")
    
    
    #Gets the name of the DUT
    dut = obj.get("dut")
    #Checks if "dut" exists
    if dut is None:
        raise ParseError(f"The Session DUT is missing: {obj!r}") 
    #Checks if "dut" is a string
    elif not isinstance(dut, str):
        raise ParseError(f"The Session DUT is not a string: {obj!r}")
    #Checks if "dut" is empty
    elif dut.strip()== "":
        raise ParseError(f"The Session DUT is empty: {obj!r}")
    

    #Gets the session_id of the test. If there is no value associated, it is set to ""
    session_id = obj.get("session_id")
    #Checks if "session_id" exists, if it does not, it is set to an empty string
    if session_id is None: 
        logger.warning("session_id missing for DUT '%s'. Using empty (\"\") string as session_id.", dut)
        session_id = ""
    #Casts "session_id" into a string if it is not a string
    elif not isinstance(session_id, str):
        session_id = str(session_id)
        
        
    #Gets value of "tests"
    raw_tests = obj.get("tests")
    if raw_tests is None:
        raise ParseError(f"The Session tests are missing for DUT '{dut}'")
    if not isinstance(raw_tests, list):
        raise ParseError(f"The Session tests are not a list for DUT '{dut}'")
    #Declare empty Test list
    tests: List[Test] = []
    #Add each test of the DUT in the list of tests in the corresponding dataclass
    for test in raw_tests:
        tests.append(_parse_test(test))

    #Return the Sessions dataclass with the corresponding values
    return Session(dut=dut, session_id=session_id, tests=tests)


def load_sessions_from_file(path: Path) -> List[Session]:

    """
    Load the sessions from the mock_data.json file and coverts it into a list of sessions dataclass

    """
    #load json file
    text = path.read_text(encoding="utf-8")
    raw = json.loads(text)

    #Check how many sessions are in the file, one (dict) or multiple (list), and append to the sessions list
    sessions: List[Session] = []
    if isinstance(raw, list):
        for item in raw:
            sessions.append(_parse_session(item))
    elif isinstance(raw, dict):
        sessions.append(_parse_session(raw))
    else:
        raise ParseError("The data file must be an object (single session) or a list (multiple sessions).")

    #Return sessions list
    return sessions


def load_sessions(paths: List[Path]) -> List[Session]:

    """
    Given a list of json paths, processes each json file using the load_sessions_from_file function 

    """

    #Declares an empty list of dataclass Session
    all_sessions: List[Session] = []
    #For each path, load the sessions from the file and append them to all_sessions
    for p in paths:
        try:
            loaded = load_sessions_from_file(p)
            all_sessions.extend(loaded)
        #Handle json file errors
        except json.JSONDecodeError as e:
            logger.error("Invalid JSON in file %s: %s", p, e)
            raise
        #Handle parsing errors defined previously
        except ParseError:
            logger.exception("Failed to parse session file %s", p)
            raise
    #Return the final list
    return all_sessions

