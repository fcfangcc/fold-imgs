import exifread
import os
from pathlib import Path
import shutil
from typing import Optional
import re
import datetime
from dateutil import parser

comp = re.compile('(2\d{3})[-/]?(0[1-9]|1[0-2])[-/]?([0-2][0-9]|3[0-1])')


def match_date(string: str) -> Optional[datetime.datetime]:
    results = re.findall(comp, string)
    for y, m, d in results:
        try:
            return parser.parse(f'{y}-{m}-{d}', yearfirst=True)
        except ValueError as e:
            pass
    return


def find_img_date(path: Path, default: str) -> str:
    date = match_date(path.name)
    if date:
        return date.strftime('%Y-%m')
    else:
        try:
            with open(path, "rb") as f:
                tags = exifread.process_file(f)
            date = tags.get('Image DateTime', '0').values.split()[0].replace(":", "-")
            return parser.parse(date).strftime('%Y-%m')
        except AttributeError as e:
            return default


def clean_mov_file(path):
    imgs = path.glob("*")
    del_num = 0
    for img in imgs:
        if img.suffix.lower() in ['.png', '.jpg']:
            mov_file = Path(str(img).split('.')[0] + ".MOV")
            if mov_file.exists():
                os.remove(str(mov_file))
                del_num += 1
                continue
            mov_file = Path(str(img).split('.')[0] + ".mov")
            if mov_file.exists():
                os.remove(str(mov_file))
                del_num += 1
                continue
    print(f'Del file: {del_num}')


include_suffix_lower = (".png", ".jpg", ".mov", ".mp4", ".mpg")

if __name__ == '__main__':
    source_path = Path(r"")
    target_path = Path(r"")
    imgs = source_path.glob("*")
    for img in imgs:
        if img.suffix.lower() in include_suffix_lower:
            create_date = find_img_date(img, default="未知日期")
            file_path = target_path.joinpath(create_date)
            if not file_path.exists():
                file_path.mkdir()
            new_file = file_path.joinpath(img.name)
            shutil.copy(img, new_file)
            print(f"copy {img.as_posix()} to {new_file.as_posix()}")
        else:
            print(img)
