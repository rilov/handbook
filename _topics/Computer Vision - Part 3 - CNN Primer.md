---
title: "Computer Vision - Part 3: CNNs for Computer Vision"
category: Computer Vision
order: 3
permalink: /topics/computer-vision-cnn-primer/
tags:
  - computer-vision
  - cnn
  - convolutional-neural-networks
  - feature-maps
  - backbone
  - transfer-learning
  - beginners
  - friendly
summary: "A very simple, picture-heavy primer on convolutional neural networks written specifically for computer vision, explained the way you'd explain it to a curious kid: learned filters, feature maps, pooling, the hierarchy of features, and the idea of a pretrained CNN backbone, just enough to understand the object detectors covered later in this series."
date: 2026-09-07
---

# Computer Vision — Part 3: CNNs for Computer Vision

[Part 1]({{ site.baseurl }}/topics/computer-vision-image-processing-fundamentals/) showed you how to build filters by hand. A Sobel filter for edges. A Gaussian filter for blur. A median filter for cleaning up noise. Every one of those filters used numbers that a person chose, in advance, by hand.

That works great for "make it blurry" or "find the edges." It does not work at all for "find the cat." Nobody on Earth can sit down and hand-write a filter for "cat-ness." So instead of a person choosing the numbers, we let the computer figure out its own numbers, by looking at a huge pile of example photos. That's the whole idea behind a **CNN**, short for **Convolutional Neural Network**.

This part is a short, simple primer. Just enough to understand the object detectors later in this series (Region-Based Detectors, Anchor Boxes, YOLO, and SSD all lean on the ideas here). If you want the full deep dive, with exact formulas and a real architecture explained layer by layer, see the Deep Learning section's [Part 9: Convolutional Neural Networks]({{ site.baseurl }}/topics/Convolutional%20Neural%20Networks%20-%20A%20Friendly%20Guide/).

## 1. A filter you invent yourself, vs a filter a robot invents

Imagine you carve your own rubber stamp. It always stamps the exact same shape, forever. That's a hand-designed filter, like the Sobel filter from Part 1. It's great at its one job and terrible at everything else.

Now imagine instead you hand a robot ten thousand photos of cats, dogs, cars, and trees, and you ask it, "invent your own rubber stamp, whatever helps you tell these apart." The robot tries random stamp shapes, checks how well each one helps, and keeps nudging the shape until it becomes genuinely useful, maybe it turns into an edge detector, maybe a "patch of orange fur" detector, maybe something a person would never have thought to design. Nobody told it what to look for. It found something useful on its own.

<img src="{{ site.baseurl }}/assets/img/learned-vs-handdesigned-filter.svg" alt="Comparison of a hand-designed filter, where a person picks fixed numbers and it always finds only edges, versus a CNN's learned filter, where the computer invents its own numbers from thousands of photos and might find edges, fur patches, or anything useful" width="100%" />

That's really all a **convolutional layer** is: the exact same sliding, multiply-and-add operation from Part 1, except the little grid of numbers, the filter, is no longer chosen by a person. It's a bunch of adjustable numbers that the network tweaks, bit by bit, every time it gets something wrong during training, until the filter becomes genuinely useful.

## 2. Many filters means many maps

A CNN never uses just one filter. It uses a whole bunch at once, often 32, 64, or more, all learning something different, side by side, on the very same photo.

Think of each filter as its own highlighter pen. One highlighter only lights up edges. Another only lights up orange, fur-like patches. Another only lights up rounded curves. Run all these highlighters over the same photo, and each one draws its own separate map of "here's where I found my thing." That map is called a **feature map**.

<img src="{{ site.baseurl }}/assets/img/cnn-many-filters-feature-maps.svg" alt="One cat photo passed through three different learned filters, one hunting for edges, one for orange fur, one for curves, each producing its own feature map, and all three feature maps then stacked together for the next layer" width="100%" />

If a layer has 64 filters, you get 64 feature maps out, stacked together like 64 see-through sheets of tracing paper laid on top of each other. That whole stack moves on to the next layer as its input.

## 3. Stack the layers and watch understanding grow

One layer of filters can only notice simple things: an edge here, a colour there. The real magic happens when you stack many convolutional layers, one after another. Each new layer doesn't look at raw pixels anymore, it looks at the *previous* layer's feature maps, so it's really looking at combinations of edges and colours.

Think of it like building with LEGO. First you have loose bricks (edges). Then you snap a few bricks into small pieces (a corner, a fuzzy patch). Then those pieces become recognisable parts (an eye, a paw). Finally the parts come together into the whole finished model (a cat!).

<img src="{{ site.baseurl }}/assets/img/cnn-hierarchy-edges-to-objects.svg" alt="Four stacked layers building understanding step by step: layer 1 finds edges and colours, layer 2 finds textures and corners, layer 3 finds object parts like an eye or a paw, layer 4 recognises the whole object, a cat, ending in a confident prediction" width="100%" />

Here's the genuinely useful part: the earliest layers (edges, colours) end up learning things that are useful for almost *any* photo, not just cats. Only the deeper layers get picky and specific. Keep that in mind, it matters a lot in a couple of sections.

## 4. Pooling: squint a little, on purpose

Between these stacked layers, a CNN usually shrinks its feature maps down a bit, on purpose. The most common way is called **max pooling**: look at each small 2×2 patch of the feature map, and keep only the biggest number, throwing the other three away.

<img src="{{ site.baseurl }}/assets/img/max-pooling-demo.svg" alt="A 4x4 feature map broken into four 2x2 coloured blocks, each block keeps only its largest number (bold), shrinking the map to 2x2 while keeping the strongest signal from each region" width="90%" />

Why deliberately throw information away? Two reasons. First, smaller feature maps are cheaper and faster for the next layer to process. Second, and more surprising, it makes the network a little forgiving about *exactly* where something was. If a cat's ear shifts two pixels to the left in a new photo, it still probably lands inside the same pooled square, so the network still notices it. It's a bit like squinting at a busy photo, you lose some fine detail, but the big important shapes still stand out clearly.

## 5. Put it all together: a backbone

Stack enough (learn filters → make feature maps → pool) blocks in a row, and you get a machine that takes a raw photo in one end, and hands out a small, deep stack of feature maps at the other end, a compact summary of "here's every pattern I noticed, and roughly where."

That whole stack, by itself, with no final decision bolted on yet, is often called a **backbone**. On its own, a backbone doesn't say "cat" or "dog." It just hands over its notes. Something else has to actually read those notes and make a decision.

Here's the really important trick this entire series depends on: nobody trains a fresh backbone from scratch every single time. Instead, people train one backbone *once*, on a giant, general pile of over a million photos (a famous one is called **ImageNet**, with a thousand different categories), until it gets genuinely excellent at noticing edges, textures, fur, wheels, and every other everyday visual pattern. Then that same, already-trained backbone gets reused, again and again, for completely different jobs.

<img src="{{ site.baseurl }}/assets/img/cnn-backbone-reuse.svg" alt="A single pretrained CNN backbone processes a new photo into a feature map once, then that same feature map is handed to three different task-specific heads, a classifier head answering what is the main object, a detector head answering where is each object and what is it, and a segmentation head answering which exact pixels belong to each object" width="100%" />

This is exactly like a photographer who takes one detailed photo, then hands prints to three different people: one just wants to know "what's the main subject," one wants to circle every object in it, one wants to cut out the exact outline of each object with scissors. All three people work from the very same photo. Only the small part on top, what to actually *do* with the backbone's notes, changes per job.

This is why, in the rest of this series, you'll keep running into a phrase like "a CNN pretrained on ImageNet." It means exactly this: somebody else's already-trained backbone, reused as the very first stage of a detector, so the detector doesn't have to relearn what an edge or a fur patch looks like from zero.

## 6. Summary

- A convolutional layer is Part 1's sliding filter, except now the filter's numbers are **learned** from photos, not chosen by hand.
- Many filters run at once, each one producing its own **feature map**, all stacked together.
- Stacking layers builds understanding step by step: edges → textures → parts → whole objects.
- **Pooling** shrinks the feature maps between layers, for speed, and for a little tolerance to things shifting slightly.
- A stack of convolution and pooling layers, with no final decision on top, is called a **backbone**, a reusable notebook of visual patterns.
- Detectors almost always start from a backbone **pretrained** on a huge, general dataset like ImageNet, rather than starting from nothing.

For the full mathematical depth behind everything above, exact output-size and parameter-count formulas, how learning actually flows backward through a filter, and a complete layer-by-layer walkthrough of a real architecture (VGG16), see [Part 9: Convolutional Neural Networks]({{ site.baseurl }}/topics/Convolutional%20Neural%20Networks%20-%20A%20Friendly%20Guide/) in the Deep Learning section.

**Next:** [Part 4: Object Detection Basics]({{ site.baseurl }}/topics/computer-vision-object-detection-basics/)
