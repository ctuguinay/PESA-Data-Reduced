# Labeling Subdirectory

Make sure you are in the current directory with the following command: 
```
cd labeling
```

## Quickstart

Run the following to sample some of the combined data:
```
python labeling_sample.py
```

Run the following to initiliaze translated text:
```
python labeling_translation.py
```

Run the following to run the labeling tool:
```
python labeling_tool.py
```

Use ``--media_source``  command to further specify the nature of the data and which folder it is in.

Use ``--make_new_labeled`` to use previous labeled data or to start from a blank slate.

Use ``--use_translator`` to use a translator while labeling text.

Use ``labeling_category`` to choose the category that is being labeled.

More information for these commands can be found in the ``argparse_create`` function in ``labeling_tool.py``.