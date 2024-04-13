# toy_sd_genetics
 This repository stores code and a blog post (this page) recording some experiments a friend and I did with using a toy genetics model to create prompts for image generators.
# background: 'genes' and image generation models
 Many image generators in hobbyist use in 2024 were trained using pairs of images and descriptions. Often those descriptions took the forms of lists of "tags" representing features visible in the image, as large pair datasets are already available in these formats, created as part of -booru imageboard culture. Prompting a model by providing a list of tags that the user wishes to see (or not see) in the resulting image is common.
 
 While this is an oversimplification in both directions, you could think about the use of tags in a prompt as analogous to Mendelian genes - they have discrete settings (although for tags this is only either 'present' or 'absent') and working together or alone they influence the traits in the result. There is even a very rough analogy for epigenetic or self-regulatory factors as the presence of a tag doesn't guarantee that the trait will appear in the final product.

 We thought it would be fun to experiment with this analogy by constructing a simplified genetics model, performing "DNA Profiling" on some existing images, and then using them to generate more. You can use the code in this repository to do the same with your own images too. It's fun to watch the images change over the generations, and it can be thought-provoking too (in a kind of low stakes way).
# some results
 Before we get underway, here's an example of an image we generated, along with its family tree.

![stack](https://github.com/curiousjp/toy_sd_genetics/assets/48515264/effad106-b27b-4798-b5ff-d7b82528b4be)

  A cool feature - the keyboard visible in the top image and its immediate ancestor to the left was a random mutation that was lucky enough to be both expressed and then propagated.
# how does it work?
 We have a very simplified model for genetics which is an analogy rather than a simulation of real biology. An individual has one or more 'chromosomes' in a 'genome'. Each chromosome has a number of loci on it, representing 'alleles' and each of these represent a single tag. (The chromosome representing the image dimensions works slightly differently - it has two alleles that are then combined into one expressed tag, which is then extracted during submission and used to set workflow parameters.) 
 
 Individuals can have multiple copies of each chromosome - most will have two of each.
 
 When it's time to convert the Individual's genome into a prompt that can be given to the image model, each chromosome is 'expressed'. Combining the expressions of each chromosome results in the prompt. When a chromosome is expressed, we look at each loci and randomly determine whether it takes part in the expression - the chance that it does is proportional to the number of copies of the chromosome that have that loci switched on. This is very different to real heritability, where there are patterns of dominance and recessivity, and where individual traits can be driven by groups of genes.

 Here is an example, taken from the "ST" chromosome on individual d10367c0-3310-47d0-a4bd-823a51910fce:
 | Chromosome Copy 0 | Chromosome Copy 1 | Likelihood | Random | Result |
 |-------------------|-------------------|--------------------------|--------|--------|
 |-|shoulder_armor|0.5|0.9974|-|
 |solo|solo|1.0|0.7522|solo|
 |-|standing|0.5|0.8244|-|
 |smile|-|0.5|0.0271|smile|
 |-|sword|0.5|0.0903|sword|
 |teeth|-|0.5|0.2390|teeth|

The code was written to support the injection of additional randomness during expression by perturbing the likelihood - but we didn't end up using this feature.

Once the genome is expressed and a prompt is made, a picture can be generated and scored - the primary source of selection pressure was 'subjective coolness', so the population wasn't forced to evolve in any particular direction. The image generation system we used was a local ComfyUI install with minimal face fixing and upscaling turned on. 

It's important to note that the images themselves cannot retroactively affect the genome. If the rendered picture has, for example, an unprompted element of a frog in it, this will not cause the 'frog' allele to be turned on in the linked individual. (This would be more akin to workflows where an image is generated from a prompt, then analysed by an LLM or tagger model to provide the prompt for the next round of generations.)

The 'best' images are selected, and the individuals that are linked to them are sent to the next stage - combining them to produce the next generation.

First, individuals are paired up. This is done using a system that weights the chance of being selected very heavily according to your ranking in the selected individuals list - this was probably set too strong in our example, see _what could we have done better?_ below for more details. Then for each pairing we walk through the chromosomes, asking each parent to contribute one of their copies to the new individual. For example, here is an example of the construction of the "AB" chromosome from 1ac8f34a-3ba1-41d0-b373-c4fc4ddb355b, whose immediate parents were 2cc8aa98-dbe6-405f-8eb9-45d776f3a407 and 2b64af1f-7456-4dd0-81e7-b66b8442822c:

|Parent A||Parent B||Child||
|-|-|-|-|-|-|
|Copy 0|Copy 1|Copy 0|Copy1|Copy 0|Copy1|
|||amulet|||amulet|
||arm_behind_back||arm_behind_back|||
|bare_shoulders||||bare_shoulders||
|||black_pants|||black_pants|
|||black_vest|||black_vest|
|blue_eyes||||blue_eyes||
|blue_hair||||blue_hair||
|||blush|||blush|
|breasts||breasts||breasts|breasts|
||brown_eyes||brown_eyes|||
|building||||building||

As you can see, in this case the child inherited copy 0 of Parent A to be its own copy 0, and copy 0 of Parent B as its own copy 1. Once the new chromosome is assembled in this way, it is randomly mutated - each loci has a small, independent, chance of being flipped to its opposite value. We had the probability of mutation set very low (as there are a very large number of loci), but we did see some mutations take hold and spread throughout the population.
# how do I do it myself?
You'll need to start by seeding the initial population - because we only selected ten individuals to propagate from at each stage, we just had ten images. We used SmilingWolf's [moat-v2](https://huggingface.co/SmilingWolf/wd-v1-4-moat-tagger-v2) to tag these, and stored the results in the `boot_population` function in _infrastructure.py_. Running this function with a filename as the first argument will construct a population for you and write it out as json. In our case, the very last image had a landscape aspect ratio, so you'll see that a choice is made as to which variation of the size chromosome to use. A more sophisticated solution would read a folder of images, tag them, and choose these settings automatically - perhaps a problem for a future update.

Once you have a json file representing the initial population, take a look at _main.py_ which is a combination of code and a notepad where I recorded what happened in the various generations. The basic workflow is to load a population of individuals using `unserialize_individuals`, create a new population by calling `breed_new_generation` with those individuals and a list of the winners, and then saving the new generation to a new file using `serialize_individuals`. 

Once this is done, the new population is iterated over, calling their expression function and handing off to `submit_job` to queue them to the local ComfyUI install. `submit_job` loads an api version of a simple ComfyUI workflow, tinkers with it, and submits it to a server assumed to be running at http://127.0.0.1:8188/. If you modify the workflow, you'll need to make modifications here as well - you may also want to add additional features like randomising the seed.

You'll return to _main.py_ after each generation, adjusting the parameters and rerunning it to continue the process.

# what could we have done better?
## making a better genome
Models like `moat-v2` know very large numbers of tags. I ended up separating them into feature chromosomes alphabetically, with each one being responsible for two letters of the alphabet and each tag that started with one of those two letters. (Note, I also edited the list of known tags to try and remove anything likely to produce overtly sexual or disturbing content, but there's a chance that I might have missed something that could be mutated back in - watch your mutation log carefully if this is something you want to avoid.) But this distribution of tags to chromosomes gives very unrealistic behaviour - the alleles for the tag 'red_eyes' and 'blue_eyes' are on entirely different chromosomes, even though they are functionally controlling the same trait.  Having large numbers of unrelated traits on a single chromosome also means that they tend to be inherited together as a package, which can be a bit boring.

A hand-picked genome could do better in this space. A better model could use multiple genes to represent a single expressed trait (see the size chromosome for an example of this) or implement dominance / recessivity. Chromosomes could also be written to control other workflow features like LoRA.
## selection
The current selection system is extremely punitive - the relative weighting of each successful individual is the reciprocal of their position in the rankings, meaning that the dropoff between successive places is extreme. A softmax function conditioned with a temperature factor would have been better here to avoid having a few candidates dominating the next generation (a function for this has been included in the code for those who would like to use it.)
## diverse inputs
We could have had a more diverse set of initial images. Across our initial ten, there were only 185 distinct tags, with an average jaccard similarity of 0.09.
## mutation rate
The mutation rate was quite low - although we saw a few mutations on each generation (which you can see logged in _main.py_), it might have been fun to have more. Especially considering how much ground each Chromosome covers, which makes small changes difficult.
## discovered the secret of frog
At some point we noticed that many of our images featured frogs, iguanas, or other small green animals, even though there was no direct tag calling for it. We never worked out what this was about, but we suspect it is something to do with either our model or the default lora we are using to give the images more visual cohesion.
