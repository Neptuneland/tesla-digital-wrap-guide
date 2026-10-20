# Tesla digital wrap guide and local PNG preflight

A practical checklist for creating **digital Paint Shop textures**, checking the file, and inspecting panel placement. These wraps change the vehicle visualization; they are not physical paint or vinyl.

Maintained by the maker of [Tesla Wrap AI](https://teslawrapai.com/?utm_source=github&utm_medium=referral&utm_campaign=tesla_wrap_launch&utm_content=guide_intro). This independent companion is not affiliated with Tesla, Inc. The Python script is free to run locally, needs no account, and does not upload files. The full website offers free gallery browsing, editing and PNG export; AI generation uses credits.

## 1. Choose the exact body map

Start with [Tesla's official templates and requirements](https://github.com/teslamotors/custom-wraps). Check the model, generation and trim before drawing. The original Model Y and 2025+ Model Y are different template choices; the official repository also distinguishes several newer variants.

The flat image is a UV map: separate regions correspond to body panels. A perspective car render is useful as an illustration, but it is not the texture file that the vehicle needs. Resizing a car photo into a square does not turn it into a compatible wrap.

## 2. Design for seams

Pick one focal area, such as the hood. Keep important lettering away from panel boundaries. A continuous stripe can appear broken if adjacent UV regions do not line up in the rendered view. Use larger shapes on small or curved panels and check both sides for mirrored text.

Three prompt starting points, to use with the correct template:

- **Minimal racing:** two broad graphite stripes on an ivory base; keep the hood motif centered, simplify small panels, and avoid text.
- **Sakura:** soft pink blossoms on a dark base; put the largest branch on the hood, keep doors quieter, and leave gaps near seams.
- **Geometric:** large teal and charcoal shapes; use a restrained palette and inspect transitions between the doors and fenders.

Ask the generator to preserve the supplied UV layout and canvas proportions. That instruction is a starting point, not proof that generation obeyed the template. Inspect the actual output afterward.

## 3. Check the PNG locally

With Python 3 installed, download `png_preflight.py`, then run:

```sh
python3 png_preflight.py /path/to/Wrap.png
```

The script checks the PNG signature, first IHDR chunk and its CRC, square dimensions from 512 to 1024 pixels, and a conservative 1,000,000-byte budget. It flags filename issues separately. It reads only the file header and file size; it does not decode image data, validate every PNG chunk, inspect the UV layout, or guarantee acceptance by a vehicle.

Example output:

```text
PASS: PNG signature and IHDR checksum
PASS: dimensions 1024 x 1024
PASS: size 42812 bytes (conservative 1 MB budget)
PASS: conservative filename check
Basic preflight passed. Still inspect UV mapping and vehicle compatibility.
```

Exit codes: `0` for these basic checks passing, `1` for a failed check, `2` for a file access error. A renamed JPEG or a truncated header fails. A plausible header with broken image data can still pass: open the file in an image viewer as an additional check.

Prefer a browser workflow? The free [Hugging Face companion](https://huggingface.co/spaces/larry-ai/Tesla-Wrap-AI) includes a local PNG checker and a prompt builder. It does not run AI inference.

## 4. Inspect before transferring

Use the [vehicle galleries](https://teslawrapai.com/gallery?utm_source=github&utm_medium=referral&utm_campaign=tesla_wrap_launch&utm_content=guide_gallery) to compare the flat texture with available rendered previews. Check the hood, doors, rear panels and lettering separately. Export the real PNG rather than saving a preview screenshot.

Tesla's official README, checked on 2026-10-20, describes mobile app transfer from Creations → Wrap → Upload with app v4.59.0 or later, or USB transfer using a root-level `Wraps` folder. Consult the official repository for current filesystem, filename and file-count rules, and check availability on the actual vehicle.

## Troubleshooting order

| Symptom | First checks |
|---|---|
| File is missing from the picker | PNG format, filename, size, transfer location and supported drive format |
| File imports but artwork looks misplaced | Exact vehicle template, canvas proportions and panel mapping |
| Letters read backward | Inspect both sides; adjust the texture rather than flipping the whole image |
| Preview looks good but import fails | Inspect the exported PNG; a preview does not validate the delivered file |

The [import troubleshooting guide](https://teslawrapai.com/blog/tesla-paint-shop-wrap-not-working?utm_source=github&utm_medium=referral&utm_campaign=tesla_wrap_launch&utm_content=guide_troubleshooting) walks through the file and template checks. Vehicle acceptance remains a separate final check.

## Scope and contributions

This repository contains an independently written guide and header checker. It does not distribute Tesla templates, vehicle models, the commercial website source, or private user data. Please include the model/template name and non-sensitive error details when reporting an issue; images are optional.
