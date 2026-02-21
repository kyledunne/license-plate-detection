import os
from pathlib import Path
from PIL import Image

splits = [
    {
        "label_src": "data/license_plates/labels/train_wrong_format",
        "label_dst": "data/license_plates/labels/train",
        "image_dir": "data/license_plates/images/train",
    },
    {
        "label_src": "data/license_plates/labels/val_wrong_format",
        "label_dst": "data/license_plates/labels/val",
        "image_dir": "data/license_plates/images/val",
    },
]

for split in splits:
    src_dir = Path(split["label_src"])
    dst_dir = Path(split["label_dst"])
    img_dir = Path(split["image_dir"])
    split_name = dst_dir.name

    os.makedirs(dst_dir, exist_ok=True)

    label_files = list(src_dir.glob("*.txt"))
    total = len(label_files)
    processed = 0

    for label_path in label_files:
        img_path = img_dir / (label_path.stem + ".jpg")

        if not img_path.exists():
            print(f"Warning: image not found for {label_path.name}, skipping.")
            continue

        with Image.open(img_path) as img:
            img_w, img_h = img.size

        lines_out = []
        for line in label_path.read_text().splitlines():
            line = line.strip()
            if not line:
                continue
            tokens = line.split()
            # Format: "Vehicle registration plate x_min y_min x_max y_max"
            # tokens[0:3] = label words, tokens[3:7] = coordinates
            x_min, y_min, x_max, y_max = (float(t) for t in tokens[3:7])

            x_c = (x_min + x_max) / 2 / img_w
            y_c = (y_min + y_max) / 2 / img_h
            w = (x_max - x_min) / img_w
            h = (y_max - y_min) / img_h

            lines_out.append(f"0 {x_c:.6f} {y_c:.6f} {w:.6f} {h:.6f}")

        (dst_dir / label_path.name).write_text("\n".join(lines_out) + "\n")
        processed += 1

    print(f"Processed {processed}/{total} files for {split_name}")
