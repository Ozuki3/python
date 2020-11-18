## 1.0 The mission
Rebel Alliance Intelligence has detected the presence of Imperial probe
[droids](https://starwars.fandom.com/wiki/Probe_droid/Legends) in the Hoth system. The Rebel
Alliance base named Echo Base is located on the ice planet Hoth. If the Imperial probes
discover the location of the base an Imperial assault is likely to be initiated. Your job is to
write a Python program capable of producing two JSON documents that contain enriched data sourced
from local files (provided) and the [Star Wars API](https://swapi.co/).

The Python program you write will be capable of producing two JSON files:

1. a document comprising a list of uninhabited planets on which a new based could be located
2. an updated and enriched Echo Base document that includes an evacuation plan for base personnel

## 2.0 General assignment outline
You will perform the following steps:

- Analyze this document, two JSON files that serve as default documents, and two JSON solution
files. The program you write _must_ be capable of producing JSON files that match the solution JSON
files.

- Read local JSON files (provided), returning dictionaries that represent default collections
of key-value pairs.

- Enrich default data whenever possible by combining it with data sourced from SWAPI.

- Refine the data by creating new dictionaries featuring an ordered subset of key-value
pairs by filtering on named keys.

- Clean values by converting strings to more appropriate data types such as `float`, `int`, `list`,
or `None`.

- write enriched, refined, and cleaned data to JSON files.

- submit the program file to Rebel Alliance Intelligence.
