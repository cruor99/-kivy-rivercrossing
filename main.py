print """
A farmer is to ferry across a river a goat, a cabbage, and a wolf.
Besides the farmer himself, the boat allows him to carry only
one of them at a time. Without supervision, the goat will gobble
the cabbage whereas the wolf will not hesitate to feast on the goat.
"""

# Solution snatched from the web:
#
# The farmer brings the goat to the right side then comes back alone.
# He then takes the cabbage to the right side and brings the goat back to the left.
# He now takes the wolf to the right side and comes back alone and then
# finally takes the goat back.

# A configuration is a nested tuple: ((left,right),desc)
# left and right are sets representing the entities on each shore
# and 'desc' is a description how this configuration was reached

farmer, goat, cabbage, wolf = ("farmer", "goat", "cabbage", "wolf")
carryables = (goat, cabbage, wolf, None)

# these combinations may not happen unsupervised
forbiddens = (set((goat, cabbage)), set((wolf, goat)))


# return wether a undesirable situation occurs
# TODO: Maybe can rewrite this with any() and all() and listcomps
def mayhem(cfg):
    for shore in cfg[0]:
        if farmer not in shore:
            for forbidden in forbiddens:
                if shore.issuperset(forbidden):
                    return True
    return False


# return True when the end condition is reached (when all entities are on the right shore)
def done(cfg):
    left, right = cfg[0]
    return left == set()


# Let the farmer ferry across the river, taking an item with him.
# 'item' can be None is the farmer is to take nothing with him.
# Return the new configuration, or None is the crossing can't be performed
# because the item is not on the same shore as the farmer.
def ferry(cfg, item):
    left, right = [set(x) for x in cfg[0]
                   ]  # make copies, because 'left' and 'right' will be mutated
    # determine on which shore the farmer is, and to which shore he will ferry
    if farmer in left:
        src, dst = left, right
    else:
        src, dst = right, left
    # make sure that if there's an item to carry, it is on the same shore as the farmer
    if item and not item in src:
        return None
    # cross the farmer and possibly the item
    desc = "Right" if farmer in left else "Left"
    src.remove(farmer)
    dst.add(farmer)
    if item:
        src.remove(item)
        dst.add(item)
        desc += ", " + item
    else:
        desc += " alone"
    return ((left, right), desc)  # return the resulting configuration


# pretty-print a configuration
def printcfg(cfg, level=0):
    left, right = cfg[0]
    verdict = "(Not allowed)" if mayhem(cfg) else "(Ok)"
    print "    " * level, ", ".join(left), "  ~~~  ", ", ".join(right), cfg[
        1], verdict


# given a certain configuration, generate the configurations that could result from it
def onegeneration(cfg):
    followups = []
    for item in carryables:
        followup = ferry(cfg, item)
        if not followup: continue
        followups.append(followup)
    return followups


# recursively generate from a given configuration
def generate(cfg, level=0):
    solutionstack.extend([None] * (level - len(solutionstack) + 1))
    solutionstack[level] = cfg[1]
    printcfg(cfg, level)
    childs = onegeneration(cfg)
    for child in childs:
        if mayhem(child):  # skip configurations which are not allowed
            continue
        if child[
                0] in previouscfgs:  # skip shore configurations which have been seen before
            continue
        previouscfgs.append(child[0])
        generate(child, level + 1)
    print solutionstack

# starting configuration
cfg = ((set((farmer, goat, cabbage, wolf)), set()), "")

# this records any previously encountered configurations
previouscfgs = [cfg[0]]

# keep a solution stack for later printing
solutionstack = []

# go!
print "Trace of the recursive solution-finding process:"
generate(cfg)

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics import Rectangle

import time
from functools import partial


class PuzzleRoot(FloatLayout):
    #Inserting the pictures
    goat = Image(source="goat.png")
    farmer = Image(source="farmer.png")
    wolf = Image(source="wolf.jpg")
    cabbage = Image(source="cabbage.png")

    #Initilize cordinates for the given pictures
    def __init__(self, **kwargs):
        super(PuzzleRoot, self).__init__(**kwargs)
        with self.canvas:
            Rectangle(size=(1200, 1200), source="river.JPG")
        self.goat.pos_hint = {"x": -0.4, "y": 0}
        self.add_widget(self.goat)
        self.farmer.pos_hint = {"x": -0.5, "y": 0}
        self.add_widget(self.farmer)
        self.wolf.pos_hint = {"x": -0.4, "y": -0.4}
        self.add_widget(self.wolf)
        self.cabbage.pos_hint = {"x": -0.4, "y": 0.4}
        self.add_widget(self.cabbage)
        Clock.schedule_once(self.printsolution)
#Prints the solution to the problem

    def printsolution(self, dt):
        print "\nThe solution to the problem:"
        timing = 1
        for step in solutionstack:
            if step:
                print step
                if str(step) == "Left, goat":
                    Clock.schedule_once(partial(self.goLeft, self.goat,
                                                self.goat.pos_hint, timing))
                    Clock.schedule_once(partial(self.goLeft, self.farmer,
                                                self.farmer.pos_hint, timing))
                elif str(step) == "Right, goat":
                    Clock.schedule_once(partial(self.goRight, self.goat,
                                                self.goat.pos_hint, timing))
                    Clock.schedule_once(partial(self.goRight, self.farmer,
                                                self.farmer.pos_hint, timing))
                if str(step) == "Left alone":
                    Clock.schedule_once(partial(self.goLeft, self.farmer,
                                                self.farmer.pos_hint, timing))
                elif str(step) == "Right, alone":
                    Clock.schedule_once(partial(self.goRight, self.farmer,
                                                self.farmer.pos_hint, timing))
                if str(step) == "Left, cabbage":
                    Clock.schedule_once(partial(self.goLeft, self.cabbage,
                                                self.cabbage.pos_hint, timing))
                    Clock.schedule_once(partial(self.goLeft, self.farmer,
                                                self.farmer.pos_hint, timing))
                elif str(step) == "Right, cabbage":
                    Clock.schedule_once(partial(self.goRight, self.cabbage,
                                                self.cabbage.pos_hint, timing))
                    Clock.schedule_once(partial(self.goRight, self.farmer,
                                                self.farmer.pos_hint, timing))
                if str(step) == "Left, wolf":
                    Clock.schedule_once(partial(self.goLeft, self.wolf,
                                                self.wolf.pos_hint, timing))
                    Clock.schedule_once(partial(self.goLeft, self.farmer,
                                                self.farmer.pos_hint, timing))
                elif str(step) == "Right, wolf":
                    Clock.schedule_once(partial(self.goRight, self.wolf,
                                                self.wolf.pos_hint, timing))
                    Clock.schedule_once(partial(self.goRight, self.farmer,
                                                self.farmer.pos_hint, timing))

                timing += 1

    def goLeft(self, image, originalpos, timing, dt):
        Clock.schedule_once(partial(self._goLeft, image), timing)

    def goRight(self, image, originalpos, timing, dt):
        Clock.schedule_once(partial(self._goRight, image), timing)

    def _goRight(self, image, dt):
        print image.source, "went right"
        image.pos_hint["x"] = 0.5
        self.do_layout()

    def _goLeft(self, image, dt):
        print image.source, "went left"
        image.pos_hint["x"] = -0.5
        self.do_layout()


class PuzzleApp(App):
    def build(self):
        return PuzzleRoot()


if __name__ == "__main__":
    PuzzleApp().run()
