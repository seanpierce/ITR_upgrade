# (Yet Another) Intro To Rhythm Upgrade

This repo serves as the source for yet another Intro To Rhythm upgrade. The purpose of this is to upgrade can be described in three parts; to bring the platform versions up to the latest stable versions, to modernize existing features, and to scoop out deprecated or legacy features that were determined as unnecessary to the project. 

## What is Intro To Rhythm?

Intro To Rhythm is a freeform mix series and live-streaming audio station that has been running since 2017. Every episode and piece of content is created and owned by the individual artists, produced exclusively for Intro To Rhythm.

Beyond broadcasting, I2R supports open-source projects and the spirit of idea sharing that fuels collaboration and experimentation. If you’re interested in building your own live-streaming station or podcast platform, you’re welcome to explore I2R’s source code (MIT License).

Send questions and comments to hello@introtorhythm.com

## What's Changing?

Besides upgrading versions of Django (3.x.x to 4.x.x) and Vue (2.x.x to 3.x.x), as well as the build dependencies throughout the project, some existing, but depracated features are going away, while the remaining features are to be refactored and modernized.

### What's staying?

* Streaming live, pre-recorded, or syndicated shows
* The Chat! However, instead of relying on a Google Firebase real-time database, the chat will be re-developed using Socket.io as it's core. 
* Headless content API. Instead of a completely home-grown API and data-layer, I'll be using DRF and model serialization. While rolling my own completely custom API and data-layer was a great learning experience, working with indistry standards is just plain easier to maintain.

## Dependencies

* Python 3.13.7
* Node 26.7.0

## Project Versions

* Django 4.2
* Vue ^3.5.18