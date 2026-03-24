# Fourier Image Matching Exam Guide

## 1) What the "actual image" and "Fourier transform image" mean

An actual image is in the spatial domain: pixel intensity by position $(x, y)$.
A Fourier transform image is in the frequency domain: how much low/high frequency content exists at each orientation.

You can think of it as:

- Spatial image: "Where are objects/edges located?"
- Fourier image: "What scales and directions are repeated?"

For a grayscale image $I(x, y)$, the 2D Fourier transform is:

$$
F(u,v)=\sum_x\sum_y I(x,y)e^{-j2\pi(ux/M+vy/N)}
$$

In practice, we usually inspect the log magnitude spectrum:

$$
\log(1+|F(u,v)|)
$$

That is the bright/dark spectrum image you see in outputs.

## 2) Core visual rules you must remember

1. Center brightness = low frequencies
- Strong bright center means smooth/blurred or large smooth regions.

2. Far from center = high frequencies
- Bright outer energy means many sharp edges, noise, or fine texture.

3. Orientation is perpendicular to structures
- Horizontal lines in the spatial image create vertical concentration in the spectrum.
- Vertical lines in the spatial image create horizontal concentration in the spectrum.

4. Periodic patterns create symmetric peaks
- Repeating stripes/grids produce clear bright points/rings away from center.

5. Spectrum is symmetric around center
- Real-valued images produce conjugate symmetry, so energy appears mirrored.

## 3) Fast mapping between image traits and Fourier traits

- Smooth sky/face/large flat background
  - Fourier: very bright center, weak outer area.

- Very sharp object boundaries/text
  - Fourier: stronger outer energy, less center dominance.

- Fine texture (grass, fabric, hair)
  - Fourier: broad medium/high-frequency spread.

- Repeated bars/stripes
  - Fourier: pair(s) of bright points, often on one axis.

- Checkerboard or dense grid
  - Fourier: multiple symmetric peaks in both directions.

- Motion blur in one direction
  - Fourier: compressed/squeezed energy pattern with directional emphasis.

## 4) How to match 5 images to 5 Fourier spectra in an exam

Use this process in order. Do not try to guess all at once.

1. Rank all 5 spatial images by smoothness vs edge density
- Most smooth image should match the spectrum with the most center-heavy energy.
- Most edgy/noisy image should match the spectrum with strongest outer energy.

2. Find obvious periodic images first
- If one image has repeating pattern (tiles, bars, windows), match it with the spectrum that has isolated bright peaks.

3. Use direction cue
- If spatial image has dominant horizontal structures, choose spectrum with vertical dominance.
- If spatial image has dominant vertical structures, choose spectrum with horizontal dominance.

4. Use texture bandwidth
- Coarse texture -> energy closer to center (mid frequencies).
- Fine texture -> energy farther out (high frequencies).

5. Final consistency check
- Every pair should make sense under center-vs-outer energy and orientation rule.
- If one pairing breaks both rules, swap with the nearest competing candidate.

## 5) Practical exam checklist (30-60 second per pair)

For each spatial image, quickly note:

- Smooth or detailed?
- Any strong line direction?
- Any repeating pattern?
- Coarse or fine texture?

For each Fourier spectrum, quickly note:

- Center-heavy or edge-heavy?
- Any strong axis or orientation?
- Any isolated symmetric peaks?
- Broad ring/band or narrow concentration?

Then match by elimination.

## 6) Common mistakes

1. Confusing brightness in spatial image with brightness in Fourier image
- Spatial brightness does not directly mean frequency brightness.

2. Forgetting perpendicular orientation rule
- This causes many wrong matches.

3. Ignoring that one outlier pattern can be matched immediately
- Repetitive texture images are usually the easiest anchor pair.

4. Over-focusing on tiny details
- First match global traits (smoothness, direction, periodicity), then refine.

## 7) Memory trick

- Center = smooth
- Outer = sharp
- Peaks = repetition
- Rotate by 90 degrees for direction intuition

If you apply those four cues, matching 5 images to 5 Fourier spectra becomes a structured elimination task instead of guessing.

## 8) Practice Set: 5 Matching Questions

Each question has 5 spatial-domain images (A-E) and 5 Fourier spectra (1-5).
Your task is to match each letter to one number.

### Question 1

Spatial images:

- A: Smooth portrait with soft background blur.
- B: Brick wall with repeating rectangular pattern.
- C: Text page with many sharp letters.
- D: Grass field with fine random texture.
- E: Road scene with strong horizontal lane markings.

Fourier spectra:

- 1: Very bright center, weak outer content.
- 2: Several strong symmetric peaks on both axes.
- 3: Strong high-frequency spread with no dominant axis.
- 4: Broad outer ring and medium/high energy.
- 5: Dominant vertical streak through center.

### Question 2

Spatial images:

- A: Vertical fence bars (periodic vertical lines).
- B: Night sky gradient (mostly smooth).
- C: Checkerboard floor.
- D: Slightly blurred city skyline.
- E: Fabric with diagonal weave pattern.

Fourier spectra:

- 1: Bright center only, almost no outer energy.
- 2: Horizontal pair of bright off-center peaks.
- 3: Grid-like symmetric peak pattern in both directions.
- 4: Center-heavy but with moderate mid-frequency spread.
- 5: Diagonal dominant energy bands.

### Question 3

Spatial images:

- A: Horizontal blinds (repeating horizontal stripes).
- B: Dense tree leaves with fine detail.
- C: Cartoon icon with clean smooth regions and sharp edges.
- D: White wall with soft shadow gradient.
- E: Window building facade with periodic squares.

Fourier spectra:

- 1: Vertical off-center peaks (strong periodic cue).
- 2: High-frequency cloud-like spread across outer region.
- 3: Mixed center + edge energy, but no periodic isolated peaks.
- 4: Strong center concentration with weak outskirts.
- 5: Multiple symmetric peaks on both axes.

### Question 4

Spatial images:

- A: Motion-blurred car moving left-right.
- B: Printed halftone dots in a regular pattern.
- C: Very smooth foggy landscape.
- D: Hair close-up with directional strands.
- E: Plain logo with bold edges on flat background.

Fourier spectra:

- 1: Directional concentration indicating blur orientation.
- 2: Repeated sharp symmetric peaks from periodic dots.
- 3: Dominant bright center with minimal outer energy.
- 4: Directional anisotropic spread without clear periodic points.
- 5: Strong edge-related outer energy plus moderate center.

### Question 5

Spatial images:

- A: Vertical text columns.
- B: Rippled water (quasi-periodic waves).
- C: Smooth face photo.
- D: Gravel road (coarse texture).
- E: Chain-link fence.

Fourier spectra:

- 1: Horizontal dominant energy band through center.
- 2: Ring-like periodic structure with symmetric peaks.
- 3: Center-dominant spectrum.
- 4: Mid-frequency weighted spread with coarse texture signature.
- 5: Distinct repeated lattice-like symmetric peak arrangement.

## 9) Answer Key with Reasoning

### Question 1 Answers

- A -> 1: Smooth portrait gives strongest center dominance.
- B -> 2: Brick repetition produces multiple symmetric peaks.
- C -> 3: Text adds strong high-frequency content.
- D -> 4: Fine texture creates broad medium/high spread.
- E -> 5: Horizontal lanes map to vertical spectral dominance.

### Question 2 Answers

- A -> 2: Vertical bars produce horizontal off-center peaks.
- B -> 1: Smooth gradient keeps energy near center.
- C -> 3: Checkerboard generates 2-axis symmetric peak pattern.
- D -> 4: Slight blur keeps center-heavy with moderate spread.
- E -> 5: Diagonal weave creates diagonal frequency dominance.

### Question 3 Answers

- A -> 1: Horizontal stripes produce vertical periodic peaks.
- B -> 2: Leaves create distributed high-frequency content.
- C -> 3: Cartoon mixes smooth zones and edge boundaries.
- D -> 4: Wall gradient is mostly low-frequency center energy.
- E -> 5: Facade periodicity yields multi-peak symmetry.

### Question 4 Answers

- A -> 1: Motion blur gives a strong directional spectrum.
- B -> 2: Halftone periodic dots produce clear symmetric peaks.
- C -> 3: Foggy smooth scene has dominant center.
- D -> 4: Hair texture is directional but less periodic than dots.
- E -> 5: Bold logo edges increase outer high frequencies.

### Question 5 Answers

- A -> 1: Vertical text columns map to horizontal spectral dominance.
- B -> 2: Ripples create ring/peak periodic signatures.
- C -> 3: Smooth face remains center-heavy.
- D -> 4: Coarse gravel emphasizes mid frequencies.
- E -> 5: Fence lattice gives strong symmetric repeated peaks.

## 10) How to Use This in Revision

1. Cover the answer key and solve all 5 sets once.
2. Re-solve with a 5-minute timer for all matches.
3. For each mistake, label which rule failed: center/outer, orientation, or periodicity.
4. Repeat until you can justify every mapping in one sentence.
