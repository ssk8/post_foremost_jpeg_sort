import PIL.Image
import datetime
from pathlib import Path
import shutil
import re

# base_path = Path("/home/curt/tmp")
# base_path = Path("/home/curt/foremost/output_Fri_Aug_24_20_08_32_2018")
base_path = Path("/home/curt/foremost/output_Fri_Aug_24_23_01_55_2018")
source_path = base_path / "jpg"
date_format = "%Y:%m:%d %H:%M:%S"

for n, pic in enumerate(source_path.iterdir()):
    try:
        img = PIL.Image.open(pic)
    except OSError:
        continue
    try:
        img.verify()
    except:
        print(f"verify failed on {pic}")
        continue
    exif_data = img._getexif()
    new_name, new_dir = None, None
    if exif_data:
        if (date:=exif_data.get(306)):
            try:
                date = datetime.datetime.strptime(date, date_format)
                new_name = f"{date.strftime('%Y-%m-%d_%H:%M:%S')}.jpg"
                new_dir = base_path / "sorted_jpg" / f"{date.strftime('%Y-%m-%d')}"
            except ValueError:
                if (model:=exif_data.get(272)):
                    model = re.sub(r'[^A-Za-z0-9 ]+', '', model)
                    new_dir = base_path / model.replace(' ', '_')
                else:
                    new_dir = base_path / "no_data_jpg"
    if not new_name:
        new_name = pic.name
    if not new_dir:
        file_size = pic.stat().st_size
        fsp = round(file_size**(1/5))
        new_dir = base_path / "size_sorted_jpg" / f"{str(fsp).zfill(4)}"

    new_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(pic, new_dir/new_name)
    print(f"copied {n} total to {new_dir/new_name}")
