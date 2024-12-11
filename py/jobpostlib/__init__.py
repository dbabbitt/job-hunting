
import time
t0 = t1 = time.time()

# Add the path to the shared utilities directory
import os.path as osp

# Define the shared folder path using join for better compatibility
shared_folder = osp.abspath(osp.join(
    osp.dirname(__file__), '..', '..', '..', 'share'
))

# Add the shared folder to sys.path if it's not already included
import sys
if shared_folder not in sys.path:
    sys.path.insert(1, shared_folder)

# Attempt to import the Storage object
try:
    from notebook_utils import NotebookUtilities
except ImportError as e:
    print(f"Error importing NotebookUtilities: {e}")

# Initialize with data and saves folder paths
nu = NotebookUtilities(
    data_folder_path=osp.abspath(osp.join(
        osp.dirname(__file__), '..', '..', 'data'
    )),
    saves_folder_path=osp.abspath(osp.join(
        osp.dirname(__file__), '..', '..', 'saves'
    ))
)
secrets_json_path = osp.abspath(osp.join(nu.data_folder, 'secrets', 'jh_secrets.json'))

# Get the WebScrapingUtilities object
from .scrape_utils import WebScrapingUtilities
wsu = WebScrapingUtilities(
    secrets_json_path=secrets_json_path
)

# Get the HeaderAnalysis object
from .ha_utils import HeaderAnalysis
hau = HeaderAnalysis()

# Get the CypherUtilities object and Neo4j driver
from .cypher_utils import CypherUtilities
cu = CypherUtilities(
    uri=wsu.secrets_json['neo4j']['connect_url'],
    user=wsu.secrets_json['neo4j']['username'],
    password=wsu.secrets_json['neo4j']['password'],
    driver=None,
    secrets_json_path=secrets_json_path
)

import pyttsx3
speech_engine = pyttsx3.init()
duration = 1000  # milliseconds
freq = 880  # Hz

from neo4j.exceptions import ServiceUnavailable
try:
    version_str = cu.driver.get_server_info().agent
    print(f'======== {version_str} ========')
except ServiceUnavailable as e:
    speech_str = f'You need to start Neo4j as a console'
    print(speech_str)
    speech_engine.say(speech_str)
    speech_engine.runAndWait()
    raise
except Exception as e:
    print(f'{e.__class__}: {str(e).strip()}')

# Get the IsHeaderSgdClassifier object
from .is_header_sgd_classifier import IsHeaderSgdClassifier
ihu = IsHeaderSgdClassifier()

# Get the HeaderCategories object
from .hc_utils import HeaderCategories
hc = HeaderCategories(verbose=False)

# Get the LrUtilities object
from .lr_utils import LrUtilities
lru = LrUtilities(verbose=False)

# Get the SectionLRClassifierUtilities object
from .section_classifier_utils import SectionLRClassifierUtilities
slrcu = SectionLRClassifierUtilities(verbose=False)

# Get the SectionSGDClassifierUtilities object
from .section_classifier_utils import SectionSGDClassifierUtilities
ssgdcu = SectionSGDClassifierUtilities(verbose=False)

# Get the SectionCRFClassifierUtilities object
from .section_classifier_utils import SectionCRFClassifierUtilities
scrfcu = SectionCRFClassifierUtilities(verbose=False)

# Get the CrfUtilities object
from .crf_utils import CrfUtilities
crf = CrfUtilities(verbose=True)

# Get the SectionUtilities object
from .section_utils import SectionUtilities
su = SectionUtilities(verbose=False)

import humanize
duration_str = humanize.precisedelta(time.time() - t1, minimum_unit='seconds', format='%0.0f')
# wsu.beep(freq, duration)
speech_str = f'Utility libraries created in {duration_str}'
print(speech_str)
speech_engine.say(speech_str)
speech_engine.runAndWait()

from datetime import datetime

# print(f"from jobpostlib import ({', '.join(dir())})")
# print(r'\b(' + '|'.join(dir()) + r')\b')