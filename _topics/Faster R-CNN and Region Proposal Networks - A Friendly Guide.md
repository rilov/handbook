---
title: "Part 14: Faster R-CNN and Region Proposal Networks (RPN) - A Friendly Guide"
category: Deep Learning
order: 14
tags:
  - deep-learning
  - cnn
  - computer-vision
  - object-detection
  - r-cnn
  - fast-r-cnn
  - faster-r-cnn
  - region-proposal-network
  - rpn
  - anchors
  - beginners
  - friendly
summary: A zero-background, kid-friendly walkthrough of the actual Faster R-CNN paper (Ren, He, Girshick, and Sun, 2015). Explains why finding objects in a photo is harder than just naming what's in it, how R-CNN and Fast R-CNN worked and where they got stuck, and how the paper's big idea, the Region Proposal Network, lets one single network both find and name objects almost for free. Diagrams throughout, plus a real example straight from the paper.
---

# Part 14: Faster R-CNN and Region Proposal Networks — A Friendly Guide

This guide explains one specific, famous research paper: **"Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks"** by Shaoqing Ren, Kaiming He, Ross Girshick, and Jian Sun (2015). We are going to demystify it completely, using very simple words and pictures, the kind of explanation you could give to a curious kid.

If you have already read [Part 9: Convolutional Neural Networks (CNNs)]({{ site.baseurl }}/topics/Convolutional%20Neural%20Networks%20-%20A%20Friendly%20Guide/), you already know the main character of this story, the CNN. This guide picks up right where that one left off.

## First, a game everyone knows: "I Spy"

Imagine you are playing "I Spy" with a photo of a busy park. Someone asks you, "Do you see a dog anywhere in this photo?" You look at the whole photo and say "yes!" That is easy.

Now imagine they ask something harder: "Point at exactly where the dog is. Now point at the person. Now point at the car." That is a much harder game. You are not just saying what you see, you are also saying **where** it is, for **every single thing** in the photo.

That harder game is called **object detection**, and it is exactly the problem this paper is trying to solve, quickly and accurately.

<img src="{{ site.baseurl }}/assets/img/classification-vs-object-detection.svg" alt="Diagram comparing image classification, where a CNN looks at a whole photo and gives one label like 'there is a dog somewhere in here', against object detection, where Faster R-CNN finds every object and draws a box around each one with its own label and confidence score" width="100%" />

A plain CNN (from Part 9) is great at the easy game, "what is in this picture?" It looks at the whole photo and gives you one answer. But a plain CNN, by itself, has no idea **where** things are. Faster R-CNN is a system built specifically to play the harder game well, and to play it fast.

## Why is "where" so much harder than "what"?

Here is the problem in the simplest possible terms. A photo does not come with little labels floating over each object saying "look here." The computer has to somehow guess, all by itself, which small rectangles inside the big photo are worth a closer look.

The most naive idea you could try is this: cut out every possible rectangle, of every possible size, at every possible position in the photo, and run your CNN classifier separately on each and every one of those cutouts, asking "is this a dog? is this a cat? is this nothing at all?"

This actually works, technically. But think about how many possible rectangles there are in even a small photo, easily millions. Running a full CNN on millions of tiny cutouts, one at a time, for every single photo, would be painfully slow. This is the actual problem that an entire family of research papers, including this one, exists to solve.

## Meet the family: R-CNN, Fast R-CNN, and Faster R-CNN

This paper does not start from nothing. It is the third and cleverest member of a small family of methods, and understanding the first two makes the punchline of this paper much easier to appreciate.

<img src="{{ site.baseurl }}/assets/img/rcnn-family-speed-comparison.svg" alt="Diagram comparing R-CNN, Fast R-CNN, and Faster R-CNN pipelines. R-CNN runs the CNN separately about 2000 times per photo, one per candidate box, which is very slow. Fast R-CNN runs the CNN once to get a shared feature map and only crops regions from it, but still waits about 2 seconds per photo for Selective Search to suggest candidate boxes. Faster R-CNN replaces Selective Search with a Region Proposal Network, a small extra part of the same shared network, so proposing boxes costs only about 10 milliseconds, nearly free" width="100%" />

**R-CNN (2014).** First, an old-fashioned, non-learning computer vision trick called **Selective Search** looks at the raw photo and groups similar-looking little patches of pixels together, guessing about 2,000 rectangles that might contain something interesting. Think of Selective Search as a slow, careful friend who circles about 2,000 "maybe something is here" spots on the photo with a marker, just by looking at colors and textures, without any deep learning at all. Then, R-CNN runs a full CNN separately on **each one** of those 2,000 cropped rectangles, one at a time, to decide what is actually inside each one. Running a big CNN 2,000 separate times on one photo is extremely slow, easily tens of seconds per photo.

**Fast R-CNN (2015).** The people who invented R-CNN quickly noticed something wasteful: those 2,000 cropped rectangles overlap each other constantly, so the CNN keeps re-examining the same patches of sky, grass, and pavement over and over again in slightly different crops. Fast R-CNN fixes this by running the CNN only **once**, on the whole photo, producing one shared "understanding" of the entire image, called a **feature map**. Then, for each of the 2,000 candidate rectangles (still supplied by that same slow Selective Search friend), it simply crops the matching little patch **out of the already-computed feature map**, using a trick called **RoI pooling**, instead of recomputing everything from scratch. This is much faster than R-CNN. But there is still a catch: Selective Search itself takes about 2 whole seconds per photo, and now it is the slowest part of the entire pipeline.

**Faster R-CNN (this paper, 2015).** Here is the key question the authors asked: *why are we still relying on that old, slow, non-learning Selective Search friend to suggest where to look, when we already have a powerful CNN that has looked at the whole photo anyway?* Their answer, and the entire point of this paper, is to teach the network itself to also suggest the candidate rectangles, using a small additional piece bolted onto the same shared feature map. They call this small piece the **Region Proposal Network**, or **RPN**. Because the RPN reuses the feature map that was going to be computed anyway, proposing boxes now costs only about 10 milliseconds instead of 2 whole seconds, practically free.

## The big idea in one sentence

> Instead of paying a slow, separate, non-learning method to guess "look here" spots, teach the same neural network that is already looking at the photo to also whisper "look here" to itself, using knowledge it already has.

The paper itself describes this using the popular idea of **attention**: the RPN module tells the Fast R-CNN detector module **where to look**, and both modules share the exact same underlying CNN, so the expensive part, actually looking closely at the picture, only happens once.

## How does the RPN actually guess "look here"?

This is the cleverest part of the whole paper, so let's slow right down and build it up piece by piece.

**Step 1: the feature map is a grid.** After the shared CNN looks at the whole photo, its output is not a photo anymore, it is a grid of numbers, a bit like a much smaller, blurrier checkerboard version of the photo, where each little square of the checkerboard has "noticed" a small patch of the original photo.

**Step 2: at every single square of that checkerboard, try 9 different guess-shapes.** At each grid position, the RPN doesn't just try one rectangle, it tries 9 different rectangle shapes all at once, all centered on that same spot. These 9 guess-shapes are called **anchors**. There are 3 different sizes (small, medium, large) and 3 different shapes (tall and narrow, square, short and wide), and 3 times 3 makes 9. This way, whether the real object at that spot is a thin lamppost, a round ball, or a wide bus, one of the 9 anchors is already roughly the right shape to start from.

**Step 3: for every one of those 9 anchors, ask two quick questions.** The RPN does not try to fully identify the object yet, that job is left for later. It only asks two much simpler questions for each anchor:

<img src="{{ site.baseurl }}/assets/img/rpn-anchors-explained.svg" alt="Diagram showing the Region Proposal Network process. First, the shared feature map is shown as a grid, with one grid cell highlighted as a sliding window spot. Second, at that one spot, 9 overlapping anchor boxes of 3 sizes and 3 aspect ratios are drawn, all centered on the same point. Third, for each of the 9 anchors the network outputs a classification score answering 'is something probably here, object versus not an object' using 2 numbers, and a regression output answering 'nudge the box a little, shift and stretch it slightly' using 4 numbers" width="100%" />

1. **"Is there probably something here at all?"** This is called the **objectness score** (the paper calls this the `cls`, or classification, output). It is just a yes-ish or no-ish confidence number, it does not yet ask *what* the object is, only whether an object of *any* kind seems to be sitting inside that anchor.
2. **"If yes, please nudge this box a little to fit better."** The real object is rarely in exactly the perfect position and size that one of the 9 fixed anchors predicted. So the RPN also predicts 4 small numbers (the paper calls this the `reg`, or regression, output) that shift the box left, right, up, or down a bit, and stretch or shrink it a bit, so it hugs the real object more snugly.

Do this at every single grid position, for all 9 anchors, and one photo ends up with roughly 20,000 candidate boxes suggested automatically, all computed from that one shared feature map that was going to be calculated anyway. That is the "nearly free" magic trick.

**Step 4: keep only the best guesses.** Most of those ~20,000 candidate boxes are quickly thrown away because their objectness score is low, or because they overlap another, better-scoring box for the same object (a cleanup step called **non-maximum suppression**). What remains, usually around 300 boxes per photo, is handed off to the second half of the system, which is basically the same Fast R-CNN detector from before: it crops each surviving box out of the shared feature map and finally decides exactly **what** object it is, a dog, a cat, a car, or nothing at all, refining the box position once more.

## Seeing it work on real photos

This is not just theory, the paper shows real example photos with real detected boxes, straight from the actual paper (Figure 3):

<img src="{{ site.baseurl }}/assets/img/faster-rcnn-paper-figure3-examples.png" alt="Real example detections from the Faster R-CNN paper. A photo of a horse and rider correctly detects car, horse, and two separate people with confidence scores like person 0.992. A photo of a dog and cat on a couch correctly draws separate boxes for dog 0.994 and cat 0.982. A photo of a bus correctly detects bus 0.996 and a person 0.736 partly hidden behind the windshield. A photo of a sailboat correctly detects boat 0.970 and three separate people on deck" width="100%" />

Notice how the boxes are all different shapes and sizes, a tall thin box around a standing person, a wide box around a bus, a small square-ish box around a cat's face, exactly the kind of variety that the 9 differently-shaped anchors were designed to handle. Each box also comes with a confidence percentage, for example "person : 0.992" means the network is 99.2% sure a person is really there.

## Why does sharing the network make it so much faster?

Here is the "aha" moment, restated one more time with real numbers straight from the paper. Using a deep network called VGG-16:

- Old way (Selective Search + Fast R-CNN): about 1.5 seconds just for Selective Search to guess boxes, plus more time for the detector, adding up to roughly **0.5 photos per second**.
- New way (Faster R-CNN with RPN): proposing boxes now takes about **10 milliseconds** because it reuses the shared feature map, and the whole system, proposing boxes and then naming objects, runs at about **5 photos per second**, and with a smaller network called ZF, up to **17 photos per second**.

And importantly, this new, much faster way is not less accurate, it actually scores slightly **better** on standard tests (called PASCAL VOC and MS COCO, big public collections of labeled photos used to fairly compare different detection methods) than the old, slower Selective Search approach. Faster, and better. That combination is exactly why this paper became so influential, it was even the foundation of several first-place winning entries in major computer vision competitions the same year it was published.

## A simple recap, in plain words

- A plain **CNN** (Part 9) can say *what* is in a photo, but not *where*.
- **Object detection** needs both a label and a location, a box, for every object.
- **R-CNN** found boxes using a slow, old-fashioned trick called Selective Search, then ran a full CNN separately on each of about 2,000 boxes. Very slow.
- **Fast R-CNN** ran the CNN only once on the whole photo and reused that result for all 2,000 boxes, but still depended on the same slow Selective Search step to find those boxes in the first place.
- **Faster R-CNN**, this paper, replaces that slow step with a small learned piece called the **Region Proposal Network (RPN)**, which reuses the same shared feature map to propose boxes almost for free, using 9 differently-shaped **anchors** at every position and asking a quick "is something here, and how should I nudge this box" question.
- The result is a single, unified network that is both **faster** and **more accurate** than everything that came before it, running in near real time.

## Key terms in plain English

| Paper's term | What it really means |
|---|---|
| Region proposal | A guessed rectangle that might contain an object |
| Feature map | The CNN's "understanding" of the whole photo, as a grid of numbers |
| Anchor | One of 9 fixed guess-shapes (3 sizes &times; 3 aspect ratios) tried at every grid position |
| Objectness score (`cls`) | "Is something probably here?", not yet *what* it is |
| Box regression (`reg`) | The small nudge that shifts and resizes a box to fit better |
| RoI pooling | Cropping one region's features directly out of the shared feature map |
| mAP | "Mean Average Precision," the standard score used to compare how accurate two detectors are |
| fps | "Frames per second," how many photos (or video frames) the system can process every second |

If you enjoyed this, the [Part 13: CNN Applications]({{ site.baseurl }}/topics/CNN%20Applications%20Image%20Classification%20Object%20Detection%20Segmentation%20-%20A%20Friendly%20Guide/) guide gives a wider tour of everything CNNs are used for, including object detection, segmentation, facial recognition, and OCR, at a slightly higher level.

---

Previous: **[Part 13: CNN Applications]({{ site.baseurl }}/topics/CNN%20Applications%20Image%20Classification%20Object%20Detection%20Segmentation%20-%20A%20Friendly%20Guide/)**

Next: **[Part 15: RNN — Recurrent Neural Networks]({{ site.baseurl }}/topics/RNN%20Recurrent%20Neural%20Networks%20-%20A%20Friendly%20Guide/)**
