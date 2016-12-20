"""CLI for electronic parts catalog"""
import os

import click

import catalog as c
from google import GoogleSpreadsheetHelper

class GoogleSpreadsheet(object):
    """Decorator which is passed to commands by Click library"""
    def __init__(self):
        self.helper = GoogleSpreadsheetHelper('spreadsheet-electronic-catalogue.json')


PASS_GOOGLE_SPREADSHEET = click.make_pass_decorator(GoogleSpreadsheet,
                                                    ensure=True)

@click.group()
def cli():
    """Do nothing - just an entry-point"""
    pass

@cli.command()
@click.argument('cells', nargs=-1)
@click.option('--file_id', help='Id of the spreadsheet.', required=True)
@click.option('--catalog_name', help='Id of the spreadsheet.', required=True)
@PASS_GOOGLE_SPREADSHEET
def add(google_spreadsheet, file_id, catalog_name, cells):
    """Adds a cells to a catalogue"""
    if not cells:
        range_name = "%s!A1:Z" % catalog_name
        last_index = google_spreadsheet.helper.get_last_index(file_id, range_name)
        range_name = "%s!A1:Z1" % catalog_name
        headers = google_spreadsheet.helper.get_headers(file_id, range_name)
        cells = c.prompt(headers, last_index)

    range_name = "%s!A2" % catalog_name
    google_spreadsheet.helper.append_row(file_id, range_name, cells)

@cli.command()
@click.argument('definition', type=click.Path(exists=True))
@PASS_GOOGLE_SPREADSHEET
def init(google_spreadsheet, definition):
    """Creates new document in google spreadsheet"""

    schema = c.load_schema(definition)

    # schema["sheets"][0].
    name = os.path.splitext(os.path.basename(definition))[0]

    sheets = []
    for sh in schema['sheets']:
        sheets.append(sh['name'])

    file_id = google_spreadsheet.helper.create_new(name, sheets)

    for sh in schema['sheets']:
        range_name = "%s!A1" % sh['name']
        cells = sh['headers']
        google_spreadsheet.helper.append_row(file_id, range_name, cells)
    # google_spreadsheet.helper.append_row(file_id, range_name, cells)
    click.echo("Created file %s (id: %s)" %(name, file_id))


if __name__ == '__main__':
    cli()
