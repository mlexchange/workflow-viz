import os
import typer

app = typer.Typer()


def sanitize_filename(filename: str) -> str:
    """
    Replace all dots ('.') in the filename except for the last one with underscores ('_').
    """
    name, ext = os.path.splitext(filename)
    sanitized_name = name.replace(".", "_")
    return sanitized_name + ext


@app.command()
def rename_files(
    root_folder: str = typer.Argument(..., help="Root folder to start renaming"),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Only show what would be renamed, do not actually rename",
    ),
):
    """
    Recursively traverse and rename files, fixing confusing dots in filenames.
    """
    if not os.path.isdir(root_folder):
        typer.echo(f"Error: {root_folder} is not a valid directory.")
        raise typer.Exit(code=1)

    rename_count = 0

    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            new_filename = sanitize_filename(filename)
            if filename != new_filename:
                old_path = os.path.join(dirpath, filename)
                new_path = os.path.join(dirpath, new_filename)
                if dry_run:
                    typer.echo(f"Would rename:\n  {old_path}\n  --> {new_path}")
                else:
                    typer.echo(f"Renaming:\n  {old_path}\n  --> {new_path}")
                    os.rename(old_path, new_path)
                rename_count += 1

    typer.echo("\nSummary:")
    if dry_run:
        typer.echo(f"[Dry Run] Total files that would be renamed: {rename_count}")
    else:
        typer.echo(f"Total files renamed: {rename_count}")


if __name__ == "__main__":
    app()
