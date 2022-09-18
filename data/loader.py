import os
import pandas

def load_data(source: str, card_set_name: str, split: str = "train"):
    data_parent_folder = os.environ.get("DATA_PATH", "data")

    if source == "wikipedia":
        csv_path = os.path.join(
            data_parent_folder,
            source,
            split,
            f"{card_set_name}.csv"
        )
        csv_data = pandas.read_csv(csv_path, sep="|")
        return csv_data["sentence"], csv_data["card"]
    else:
        raise ValueError(f"Unknown data source {source}")
