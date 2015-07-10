Python Examples
==================

These examples are scripts that can be run independently to demonstrate the Rosette API functionality.

Prerequisite: Either run `pip install rosette_api` or run `python setup.py install` in the python top level folder.

You can now run your desired _endpoint_.py file to see it in action.
For example, run `python/examples/categories.py` if you want to see the categories
functionality demonstrated.

All files require you to input your Rosette API User Key after --key to run.  
For example: `python ping.py --key 1234567890`  
All also allow you to input your own service URL if desired.  
For example: `python ping.py --key 1234567890 --service_url http://www.myurl.com`    
Some (specified below) allow an additional input of either a file (.html or .txt) or a URL with `--file` or `--url`

Each example, when run, prints its output to the console.

| File Name                     | What it does                                          | 
| -------------                 |-------------                                        | 
| categories.py                    | Gets the category of a document at a URL              | 
| entities.py                      | Gets the entities from a piece of text                | 
| entities_linked.py               | Gets the linked (to Wikipedia) entities from a piece of text |
| info.py                          | Gets information about Rosette API                    | 
| language.py                      | Gets the language of a piece of text                  | 
| matched-name.py                  | Gets the similarity score of two names                | 
| morphology_complete.py               | Gets the complete morphological analysis of a piece of text| 
| morphology_compound-components.py    | Gets the de-compounded words from a piece of text     | 
| morphology_han-readings.py           | Gets the Chinese words from a piece of text           | 
| morphology_lemmas.py                 | Gets the lemmas of words from a piece of text         | 
| morphology_parts-of-speech.py        | Gets the part-of-speech tags for words in a piece of text | 
| ping.py                          | Pings the Rosette API to check for reachability       | 
| sentences.py                     | Gets the sentences from a piece of text               |
| sentiment.py                     | Gets the sentiment of a local file                    | 
| tokens.py                        | Gets the tokens (words) from a piece of text          | 
| translated-name.py               | Translates a name from one language to another        |

