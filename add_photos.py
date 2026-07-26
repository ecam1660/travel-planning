#!/usr/bin/env python3
"""
add_photos.py — Add new bird photos for the flashcards game.

HOW TO USE
  1. Drop new photo files into the `photo_inbox` folder (created automatically
     inside your travel-planning repo folder), named after the species slug —
     same convention the site already uses, e.g.:
       great_argus.jpg
       laced_woodpecker.jpg
     (Slug = species name, lowercased, spaces/punctuation replaced with "_".)
  2. Run:  python3 add_photos.py
  3. It will:
       - Move each new file into photos/, auto-numbering it _2, _3, etc. if a
         photo for that species already exists.
       - Rebuild the PHOTO_VARIANTS lookup inside flashcards.html to match
         whatever photos actually exist in photos/ — fully automatic, no
         manual script edits needed.
  Nothing on index.html / nonbirds.html is touched — only flashcards.html.
"""
import os, re, shutil, sys, glob

# Adjust this if your live site files live somewhere else.
REPO_DIR = os.path.expanduser("~/Desktop/github/travel-planning")
PHOTOS_DIR = os.path.join(REPO_DIR, "photos")
INBOX_DIR = os.path.join(REPO_DIR, "photo_inbox")
FLASHCARDS = os.path.join(REPO_DIR, "flashcards.html")
LOCATION_CSV = os.path.join(REPO_DIR, "location.csv")

IMG_EXTS = (".jpg", ".jpeg", ".png")


def photo_slug(name):
    s = name.lower()
    s = re.sub(r"[‘’']", "", s)
    s = re.sub(r"[^a-z0-9]+", "_", s)
    return s.strip("_")


def split_row(line):
    out, cur, inq = [], "", False
    for ch in line:
        if ch == '"':
            inq = not inq
        elif ch == "," and not inq:
            out.append(cur)
            cur = ""
        else:
            cur += ch
    out.append(cur)
    return out


def load_species_names():
    """Read location.csv and return the list of species display names."""
    if not os.path.exists(LOCATION_CSV):
        return []
    with open(LOCATION_CSV, encoding="utf-8") as f:
        lines = f.read().splitlines()
    if len(lines) < 2:
        return []
    heads = [h.strip().lower() for h in split_row(lines[0])]
    name_idx = heads.index("malaysia & singapore") if "malaysia & singapore" in heads else 0
    names = set()
    for line in lines[1:]:
        cells = split_row(line)
        if len(cells) > name_idx and cells[name_idx].strip():
            names.add(cells[name_idx].strip())
    return sorted(names)


def main():
    os.makedirs(INBOX_DIR, exist_ok=True)
    os.makedirs(PHOTOS_DIR, exist_ok=True)

    if not os.path.exists(FLASHCARDS):
        print(f"Couldn't find {FLASHCARDS} — check REPO_DIR at the top of this script.")
        sys.exit(1)

    inbox_files = sorted(
        f for f in os.listdir(INBOX_DIR)
        if f.lower().endswith(IMG_EXTS) and not f.startswith(".")
    )

    if not inbox_files:
        print(f"No new photos found in {INBOX_DIR}.")
    for fname in inbox_files:
        base, _ext = os.path.splitext(fname)
        slug = photo_slug(base)
        src = os.path.join(INBOX_DIR, fname)

        primary_exists = os.path.exists(os.path.join(PHOTOS_DIR, slug + ".jpg"))
        variants = glob.glob(os.path.join(PHOTOS_DIR, slug + "_*.jpg"))

        if not primary_exists and not variants:
            dest_name = slug + ".jpg"
        else:
            nums = [1]
            for p in variants:
                m = re.search(r"_(\d+)\.jpg$", p)
                if m:
                    nums.append(int(m.group(1)))
            dest_name = f"{slug}_{max(nums) + 1}.jpg"

        dest = os.path.join(PHOTOS_DIR, dest_name)
        shutil.move(src, dest)
        print(f"  {fname}  ->  photos/{dest_name}")

    # Rebuild PHOTO_VARIANTS from whatever now actually exists in photos/
    names = load_species_names()
    variant_counts = {}
    for name in names:
        slug = photo_slug(name)
        if not os.path.exists(os.path.join(PHOTOS_DIR, slug + ".jpg")):
            continue
        count = 1
        n = 2
        while os.path.exists(os.path.join(PHOTOS_DIR, f"{slug}_{n}.jpg")):
            count = n
            n += 1
        if count > 1:
            variant_counts[name] = count

    with open(FLASHCARDS, encoding="utf-8") as f:
        html = f.read()

    lines = ["var PHOTO_VARIANTS = {"]
    for name in sorted(variant_counts):
        esc = name.replace("\\", "\\\\").replace("'", "\\'")
        lines.append(f"  '{esc}': {variant_counts[name]},")
    lines.append("};")
    new_block = "\n".join(lines)

    pattern = re.compile(r"var PHOTO_VARIANTS = \{.*?\};", re.DOTALL)
    if not pattern.search(html):
        print("Couldn't find a PHOTO_VARIANTS block in flashcards.html — no changes made.")
        sys.exit(1)

    html = pattern.sub(new_block, html, count=1)
    with open(FLASHCARDS, "w", encoding="utf-8") as f:
        f.write(html)

    if variant_counts:
        print("\nPHOTO_VARIANTS now includes:")
        for name in sorted(variant_counts):
            print(f"  {name}: {variant_counts[name]} photos")
    else:
        print("\nNo species currently have more than 1 photo.")

    print("\nDone. flashcards.html updated. To publish:")
    print(f"  cd {REPO_DIR} && git add photos flashcards.html && git commit -m 'Add photo variants' && git push")


if __name__ == "__main__":
    main()
