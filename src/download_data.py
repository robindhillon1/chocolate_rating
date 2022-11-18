# Author: DSCI_522_Group_5
# Date: 2022-11-18

"""Downloads data (html table) from the web, convert and save it as a csv to a local filepath.

Usage: download_data.py --url=<url> --out_file=<out_file> 
 
Options:
--url=<url>             URL from where to download the data (must be in html table)
--out_file=<out_file>   Path (including filename) of where to locally write the file
"""

import os
import pandas as pd
from docopt import docopt

opt = docopt(__doc__)

def main(url, out_file):
    data = pd.read_html(url)[0]
    try:
        data.to_csv(out_file, index=False)
    except:
        os.makedirs(os.path.dirname(out_file))
        data.to_csv(out_file, index=False)


if __name__ == "__main__":
    main(opt["--url"], opt["--out_file"])
