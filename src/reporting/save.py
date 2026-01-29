from pathlib import Path
import matplotlib.pyplot as plt


def save_figure(
    fig,
    name: str,
    output_dir: Path,
    dpi: int = 300
):
    """
    Save figure in both PNG and PDF formats.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    png_path = output_dir / f"{name}.png"
    pdf_path = output_dir / f"{name}.pdf"

    fig.savefig(png_path, dpi=dpi, bbox_inches="tight")
    fig.savefig(pdf_path, bbox_inches="tight")

    print(f"Saved figure: {png_path}")
