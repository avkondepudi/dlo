dlo
========

``dlo`` is a lightweight, dynamic Python client to pull NBA data from stats.nba.com_.

Overview
____________________

This client utilizes error messages from the stats.nba.com API to:

* check whether parameter passed is valid
* check whether endpoint is valid or possibly deprecated
* return list of parameters for endpoint
* return list of possible values for any parameters and whether required for endpoint
* automatically pass required parameters with default value if not given

It is possible to build a documentation of the API given possible endpoints with this client.

Inspired by nba_py_.

Installation
____________________

.. code-block:: bash

    # stable version
    pip install dlo

    # latest version
    git clone https://github.com/avkondepudi/dlo.git
    cd ./dlo
    pip install .

Dependencies
____________________

* requests_ (required)
* pandas_ (recommended)

Usage
____________________

A list of endpoints can be found here_. IDs (PlayerID, GameID, etc.) can be found on stats.nba.com_.

.. code-block:: python

    >>> from dlo import Data                            # import module
    >>> LOCAL = {                                       # set local parameters
    ... "PlayerID": 1626156,                            
    ... "Season": "2018-19",
    ... "SeasonType": "Regular Season"
    ... }
    >>> d = Data(**LOCAL)                               # create instance of Data class with local parameters
    >>> d.local = LOCAL                                 # another way to pass local parameters (recommended; deletes previous local parameters)
    >>> d.local                                         # returns local parameters passed
    {"PlayerID": 1626156, "Season": "2018-19", "SeasonType": "Regular Season"}
    >>> d.endpoint = "playergamelog"                    # set endpoint
    >>> d.endpoint                                      # returns current endpoint
    "playergamelog" 
    >>> d.getEndpointParams()                           # returns list of parameters for current endpoint
    ['PlayerID', 'Season', 'SeasonType']
    >>> d.getParamInfo("SeasonType")                    # returns list of values for parameter and whether required
    {'regex': '^(Regular Season)|(Pre Season)|(Playoffs)|(All-Star)|(All Star)$', 'values': ['Regular Season', 'Pre Season', 'Playoffs', 'All-Star', 'All Star'], 'required': True}
    >>> d.getParam("Season")                            # returns parameter value if passed
    "2018-19"
    >>> d.removeParam("Season")                         # value for Season (2018-19) removed
    >>> d.setParam("Season", "2018-19")                 # two ways to set/add parameters
    >>> d.Season = "2018-19"
    >>> data = d.getData()                              # returns data (game log of D'Angelo Russell for the 2018-19 Regular Season)
    >>> data_in_pandas_format = d.getData(pandify=True)

.. _stats.nba.com: https://stats.nba.com/ 
.. _nba_py: https://github.com/seemethere/nba_py
.. _requests: https://github.com/psf/requests
.. _pandas: https://github.com/pandas-dev/pandas
.. _here: https://any-api.com/nba_com/nba_com/docs/API_Description
