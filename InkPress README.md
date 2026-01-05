# InkPress – Image Preparation for E-Ink Displays

InkPress is a small, purpose-built image preparation workflow for **e-ink displays**, designed around the constraints of the **Kindle 4 (600×800, grayscale)**.

It converts arbitrary images into e-ink-friendly assets with correct resolution, tone, and contrast, minimizing ghosting and preserving visual clarity.

InkPress does **not** handle display, installation, or device control.  
Its only responsibility is **image conversion**.

---

## Purpose

E-ink displays behave very differently from LCD or OLED screens:

- limited grayscale depth
- low contrast tolerance
- visible dithering artifacts
- poor handling of subtle gradients
- harsh results from uncontrolled scaling

InkPress exists to standardize image preparation so that final images:

- match the native screen resolution
- render crisply on e-ink
- avoid washed-out tones
- avoid excessive ghosting

---

## Directory Structure

InkPress assumes a simple, explicit folder layout:

InkPress/input_images/
InkPress/output_images/

- **`input_images/`**  
  Place original source images here.  
  These can be any size, format, or orientation.

- **`output_images/`**  
  Converted, e-ink-ready images are written here.  
  Only files from this directory should be copied to the Kindle.

This separation ensures that originals are never modified and that final assets are clearly identifiable.

---

## Scope

InkPress focuses exclusively on **offline image processing**:

- resizing
- orientation normalization
- grayscale conversion
- contrast tuning
- optional dithering

It is intentionally decoupled from any Kindle-specific tooling.

---

## Target Output

InkPress produces images suitable for:

- Kindle screensaver hacks
- static e-ink frames
- framebuffer-based display experiments
- archival e-ink artwork

Primary target device:

- Kindle 4 Non-Touch (600×800, portrait)

---

## Recommended Output Characteristics

Images produced by InkPress should conform to:

- Resolution: **600 × 800**
- Orientation: portrait
- Color space: grayscale
- Format: PNG (preferred) or JPEG
- DPI: irrelevant for e-ink (commonly set to 72 for compatibility)

---

## Conversion Philosophy

InkPress favors:

- explicit resizing over automatic scaling
- controlled contrast adjustment
- predictable grayscale mapping
- minimal post-processing

The goal is not photographic realism, but **clarity and presence** on e-ink.

---

## Typical Processing Flow

A standard InkPress workflow follows a simple pattern:

1. Place source images in `input_images/`
2. Process images using the chosen toolchain
3. Write converted results to `output_images/`
4. Review results visually
5. Deploy only the contents of `output_images/` to the device

Exact parameters vary depending on the artwork.
