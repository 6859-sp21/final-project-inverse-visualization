# DeVIZ: Data Visualization Decompiler

![Website](https://img.shields.io/website?url=https%3A%2F%2Finverse.firemeet.io%2F)

[[Video]](https://www.youtube.com/watch?v=JmG8-sZFIbM) [[Website]](https://inverse.firemeet.io/) [[Paper]](FinalPaper.pdf)

![overview](system-overview.png)
#### Abstract

Creating static visualizations is a lossy process, a user's code and data is compiled in the form of a static image. These images are the default form of data visualizations, and are ubiquitous across both social media and academia. As visualization researchers, this lossy compilation into images makes it very challenging to experiment and tweak with design decisions of the original author. In this work, we present a novel deep-learning based algorithm that can _decompile_ an image visualization, allowing researchers to easily edit and inspect its visual design. Our method and domain-specific language is more general than previous approaches and is extensible to more types of data visualizations without the need for expert-tuned heuristics.

## Developmental Setup

### Pretrained Models

Pretrained models should be unzipped into `backend/marks`, structure should be something like,

```
backend/marks/
  box_model2/
    saved_model.pb
    assets/
    variables/
```

|Name|Link|
|----|-------------|
|`box_model`|[Download](https://www.dropbox.com/s/33xi78jockuvrsi/box_model.zip?dl=1)|
|`box_model2`|[Download](https://www.dropbox.com/s/aum7nifjmzhwlny/box_model2.zip?dl=1)|

### Running

Install Python Deps,

```
pip install -r requirements.txt
```

Unpack pretrained models as described in the next subsection.

Run dev server,

```
python serve.py
```

Inside `frontend/`, install deps,

```
npm install
```

And while the backend is running, finally,

```
npm run serve
```

Chrome extention launcher can be loaded as an unpacked web extention.

## Research Commentary

We were first inspired by Arvind's second lecture, where he mentioned how he had an idea for a web extention that can "undo" design decisions directly from images. We realized that this task was fairly challenging, especially the data extraction and recovery, so we scoped down to just being able to decompile design decisions from images. We were pretty stationary on this goal, and did not change much. Our MVP goal was to make it work with simple bar graphs from matplotlib.

We quickly realized that the current state of the art open-sourced models were not good enough to handle text labels. We tried multiple different models, papers, open-source repos, but didn't have much luck. The Google Cloud Vision API worked the best, but that too was subpar. Since this is a very specific problem, we think a domain-specific approach (like the rest of the project) would have worked better. We initially had plans for font maniuplation as well using generative models that can embed a font's features into a latent space, but since our OCR attempts took so long we had to drop that idea.

The encoding entity factorization also took a lot of effort. We tried a lot of different models, inference schemes. It was particularly hard to control the loss function for bounding box regression versus property regression. We finally took an approach where we first trained bounding box completelely and then fine tuned the property detector. We think our inverse graphics approach is actually much more extensible to handle many more types of plots.

For our final submission, we tried to show this last claim by also adding scatter plot abilities. We also added a hidden steganographic watermark based on the feedback on blackhat concerns. We also added the ability to manipulate series as suggested by one of our peers.

### Work Split

Shreyas worked on the shape encoding detector, and the frontend. Josh worked on the OCR and text layer. Moises worked on the web extention.
