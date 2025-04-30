import difflib
import os
from typing import List, Optional

import pandas as pd
import typer
from dotenv import load_dotenv
from tiled.client import from_uri
from tiled.client.array import ArrayClient
from tiled.client.container import Container

app = typer.Typer()

# Load .env for Tiled access
load_dotenv()
TILED_URI = os.getenv("TILED_URI")
TILED_API_KEY = os.getenv("TILED_API_KEY")

if not TILED_URI or not TILED_API_KEY:
    raise ValueError("TILED_URI and TILED_API_KEY must be set in the .env file")

client = from_uri(TILED_URI, api_key=TILED_API_KEY)


def read_tiled_table(trimmed_table_uri: str) -> pd.DataFrame:
    """
    Load a table from a Tiled URI and return as a pandas DataFrame.
    """
    table_client = client[trimmed_table_uri]
    return table_client.read()


def traverse_and_update(
    container: Container,
    df: pd.DataFrame,
    key_column: str,
    metadata_columns: Optional[List[str]],
    dry_run: bool,
    prefix: str,
    updated_count: dict,
):
    """
    Recursively traverse container and update metadata for matching ArrayClients.
    """
    for key, item in container.items():
        if isinstance(item, ArrayClient):
            if key in df[key_column].values:
                row = df[df[key_column] == key].iloc[0]

                # Build metadata dictionary
                new_metadata = (
                    {col: row[col] for col in metadata_columns if col in row}
                    if metadata_columns
                    else row.drop(labels=[key_column]).to_dict()
                )

                typer.echo(f"Matched Array: {prefix}/{key}")
                typer.echo(f"New meta data: {new_metadata}")

                if not dry_run:
                    # Retrieve the current metadata
                    current_metadata = item.metadata
                    new_metadata = {
                        **current_metadata,
                        **new_metadata,
                    }
                    # Update the item with the new metadata
                    item.update_metadata(new_metadata)
                    typer.echo("Metadata updated.")
                else:
                    typer.echo("[Dry Run] Metadata would be updated.")

                updated_count["count"] += 1
            else:
                # If the key is not found in the DataFrame, log the closest match
                candidates = df[key_column].astype(str).unique()
                closest = difflib.get_close_matches(key, candidates, n=1)
                if closest:
                    typer.echo(
                        f"No Match for '{prefix}/{key}' found in table, "
                        + f"did you mean: '{closest[0]}'?"
                    )
                else:
                    typer.echo(
                        f"No Match for '{prefix}/{key}' found in table, "
                        + "and no close matches found."
                    )

        elif isinstance(item, Container):
            traverse_and_update(
                item,
                df,
                key_column,
                metadata_columns,
                dry_run,
                prefix=f"{prefix}/{key}",
                updated_count=updated_count,
            )


@app.command()
def update_metadata_from_tiled_table(
    container_name: str = typer.Argument(
        "raw", help="Name of root container, e.g., 'raw', 'processed' (default: raw)"
    ),
    trimmed_table_uri: str = typer.Argument(
        ...,
        help="Trimmed Tiled URI to table with metadata",
    ),
    key_column: str = typer.Argument(
        "Scan Key",
        help="Column name in table matching ArrayClient keys, e.g., 'Scan Key'",
    ),
    metadata_keys: Optional[List[str]] = typer.Option(
        None,
        "--keys",
        help="Columns to add as metadata fields from table, all if not specified",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Only show what would be updated, don't modify metadata",
    ),
):
    """
    Recursively traverse a Tiled container and update ArrayClient metadata from
    a Tiled-hosted table.
    """
    typer.echo("Reading table from Tiled...")
    df = read_tiled_table(trimmed_table_uri)

    if key_column not in df.columns:
        raise ValueError(f"'{key_column}' not found in table columns.")

    if metadata_keys:
        for key in metadata_keys:
            if key not in df.columns:
                raise ValueError(f"'{key}' not found in table columns.")

    if container_name not in client:
        raise ValueError(f"Container '{container_name}' not found in Tiled client.")

    container = client[container_name]
    updated_count = {"count": 0}

    typer.echo(f"Beginning recursive scan of '{container_name}'...")
    traverse_and_update(
        container,
        df,
        key_column,
        metadata_keys,
        dry_run,
        prefix=container_name,
        updated_count=updated_count,
    )

    typer.echo("\nSummary:")
    typer.echo(f"Total matched and updated: {updated_count['count']}")


if __name__ == "__main__":
    app()
