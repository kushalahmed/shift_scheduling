import os
from paste.deploy import appconfig

here = os.path.dirname(__file__)
settings = appconfig('config:' + os.path.join(here, '../../', 'test.ini'))






