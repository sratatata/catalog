# About

This simple program is builded for simplification and automation of electronic parts catalog creation. 
As an backend google spreadsheets are used.

## Featurs:

* Initialization of new spreadsheet
* Adding rows in script style
* Adding rows in user prompt style

#Manual 
1. Create client_secret.json - follow [manual](https://developers.google.com/sheets/api/quickstart/python)

2. Run catalog_cli with init command, write down file_id, you would need it later for reference.

    ```
    #> python catalog_cli.py init passive.json
    Created file passive (id: 12YguWGnTfVCH4Got_vTXLS6eSL00000000000O6IHc)
    ```

    This will create new spreadsheet on your google account, with all sheets and header row initialized.

3. Now you can append rows: 

    ```
    #> python catalog_cli.py add --file_id=12YguWGnTfVCH4Got_vTXLS6eSL00000000000O6IHc --catalog_name=Resistors 1 102 10000 12 1 5W 10 0.20
    ```

    or with prompt:

    ```
    #> python catalog_cli.py add --file_id=12YguWGnTfVCH4Got_vTXLS6eSL00000000000O6IHc --catalog_nam    e=Resistors
    Enter #INDEX (2): 
    Enter Symbol: 102
    Enter Resistance: 12333
    Enter Row: 12
    Enter Precision: 1
    Enter Power: 5W
    Enter Amount: 10
    Enter Price: 0.20 PLN

    ```
