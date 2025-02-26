---
layout: post
title: textual-pyfiglet
date: 2025-02-25
description: A library that makes it easy to integrate PyFiglet into Textual. It adds a 'FigletWidget' that handles all the hard stuff for you.
img: posts/textual-pyfiglet.png
tags: [BigText, ASCII]
---

Textual-PyFiglet is an implementation of [PyFiglet](https://github.com/pwaller/pyfiglet) for Textual.

It provides a `FigletWidget` class which handles all the hard stuff for you. Any text generated will automatically crop to the container that it's inside of - so you can just set the size of the FigletWidget where you need, and it'll handle the alignment and cropping automatically.

It can also write or update in real time - It can be tied to an Input or TextArea widget, or have text fed into it programmatically.

See the Github page for full information and to give it a star if you find it useful.

## GITHUB:

https://github.com/edward-jazzhands/textual-pyfiglet

## DEMO:

![Demo GIF](https://raw.githubusercontent.com/edward-jazzhands/textual-pyfiglet/refs/heads/main/demo.gif)

## INSTALLATION:

Base package - includes 10 fonts (71kb):   
```
pip install textual-pyfiglet
```
Install with extended fonts collection - 519 fonts (1.6mb):   
```
pip install textual-pyfiglet[fonts]
```