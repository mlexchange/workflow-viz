import pandas as pd
import typer

app = typer.Typer()


def format_with_min_precision(val):
    """
    Format a number with at least one digit after the decimal point.
    Keep original decimal precision if it's higher.
    """
    if isinstance(val, float):
        s = f"{val:.10f}".rstrip("0").rstrip(".")
        if "." not in s:
            s += ".0"
        return s
    return val  # leave strings and non-numeric as-is


@app.command()
def reformat_csv(
    input_path: str = typer.Argument(..., help="Path to the input CSV file"),
    output_path: str = typer.Argument(..., help="Path to save the formatted CSV file"),
):
    """
    Reads a CSV and rewrites it with all numeric columns having at least 1 decimal.
    """
    df = pd.read_csv(input_path)

    for col in df.select_dtypes(include=["float", "int"]).columns:
        df[col] = df[col].apply(format_with_min_precision)

    df.to_csv(output_path, index=False)
    typer.echo(f"Formatted CSV saved to: {output_path}")


if __name__ == "__main__":
    app()
