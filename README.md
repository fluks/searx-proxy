## Description

This web page chooses randomly one of the public Searx instances and redirects your search to the selected instance.

## Usage

```
virtualenv --python python3 venv
. venv/bin/activate
pip3 install -r requirements.txt
./run.sh
```

Go to one of the public instances and add a keyword for its search (in Firefox right click on search input and select "Add a keyword for this Search"). 
Then from its bookmark properties change the location to `http://localhost:5000`. Now, using that keyword should go to the proxy page and redirect the search
to one of the public instances. If you chose `sxp` as the keyword, `sxp searx` should do it.
