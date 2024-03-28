
from datetime import datetime
import humanize
import os.path as osp
import time
import winsound

duration = 1000  # milliseconds
freq = 880  # Hz
t0 = t1 = time.time()

# Get the Storage object
from .notebook_utils import NotebookUtilities
nu = NotebookUtilities(
    data_folder_path=osp.abspath('../data'),
    saves_folder_path=osp.abspath('../saves')
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

from neo4j.exceptions import ServiceUnavailable
try:
    version_str = cu.driver.get_server_info().agent
    print(f'======== {version_str} ========')
except ServiceUnavailable as e:
    print(f'You need to start Neo4j as a console')
    raise
except Exception as e:
    print(f'{e.__class__}: {str(e).strip()}')

# Get the IsHeaderSgdClassifier object
from .is_header_sgd_classifier import IsHeaderSgdClassifier
ihu = IsHeaderSgdClassifier(verbose=False)

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

duration_str = humanize.precisedelta(time.time() - t1, minimum_unit='seconds', format='%0.0f')
# winsound.Beep(freq, duration)
print(f'Utility libraries created in {duration_str}')