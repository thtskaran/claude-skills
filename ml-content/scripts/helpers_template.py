"""
ml-content — the per-video DOMAIN DSL template (manimGL).

This is the single most important discipline for non-slop output (SKILL.md Law 3).
Every 3b1b video defines ~6 custom Mobjects/Animations + ~6 scene-local factories in
a helpers.py, then the scene files just consume them. Reference for this template:
videos/_2024/transformers/helpers.py (NeuralNetwork, WeightMatrix, NumericEmbedding,
EmbeddingArray, Dial, MachineWithDials, ContextAnimation, show_matrix_vector_product).

Two kinds of thing live here:
  1. Mobject SUBCLASSES that build and arrange THEMSELVES in __init__   (the nouns)
  2. show_*(scene, ...) functions that choreograph reusable animations  (the verbs)

Import in a scene file with:  from helpers import *
"""

from manim_imports_ext import *   # standalone fallback: from manimlib import *


# =============================================================================
# Domain constants — physical/logical numbers live here, ONE conversion factor.
# Kills mutually-inconsistent eyeballed sizes across a multi-scene video.
# =============================================================================

NEURON_RADIUS = 0.12
LAYER_BUFF_RATIO = 6.0     # horizontal gap as a multiple of neuron width


def value_to_color(value, max_value=10.0):
    """Signed weight colormap: + blue, - red, magnitude -> lightness (helpers.py:51)."""
    alpha = clip(abs(value) / max_value, 0, 1)
    lo, hi = (BLUE_E, BLUE_B) if value >= 0 else (RED_E, RED_B)
    return interpolate_color(lo, hi, alpha)


# =============================================================================
# NOUN — a self-arranging Mobject. The 7-step recipe (SKILL.md Law 3):
#   1 subclass VGroup/VMobject   2 build sub-parts   3 lay out RELATIVELY
#   4 super().__init__(*parts)   5 name every meaningful part
#   6 a set_value/reset_* state mutator (geometry+style from the logical value)
#   7 animate_* methods that RETURN animations
# =============================================================================

class NeuronLayer(VGroup):
    """A vertical column of neurons whose activations drive their fill.

    Self-arranging: callers never position individual neurons.
    """
    def __init__(self, n, activations=None, radius=NEURON_RADIUS,
                 v_buff_ratio=1.0, **kwargs):
        super().__init__(**kwargs)                          # step 1
        # step 2 + step 3: build a grid that lays ITSELF out (no move_to([x,y,0]))
        neurons = Dot(radius=radius).get_grid(n, 1, v_buff_ratio=v_buff_ratio)
        for dot in neurons:
            dot.set_stroke(WHITE, 1).set_fill(WHITE, 0)
        self.add(neurons)                                   # step 4 (VGroup.add)
        self.neurons = neurons                              # step 5: named part
        self.set_activations(activations if activations is not None
                             else np.zeros(n))              # step 6

    def set_activations(self, activations):                 # step 6: value -> style
        for dot, a in zip(self.neurons, activations):
            dot.set_fill(WHITE, opacity=float(clip(a, 0, 1)))
        self.activations = np.asarray(activations, dtype=float)
        return self

    def pulse(self, **kw):                                  # step 7: returns an animation
        return LaggedStartMap(FlashAround, self.neurons, lag_ratio=0.05, **kw)


class MiniNetwork(VGroup):
    """Layers + connections, all relative. Connections derive endpoints from neurons."""
    def __init__(self, layer_sizes=(6, 9, 4), **kwargs):
        super().__init__(**kwargs)
        layers = VGroup(*(NeuronLayer(n) for n in layer_sizes))
        layers.arrange(RIGHT, buff=LAYER_BUFF_RATIO * layers[0].neurons[0].get_width())
        lines = VGroup(*(
            VGroup(*(
                Line(a.get_center(), b.get_center(), buff=a.get_width() / 2)
                .set_stroke(value_to_color(random.uniform(-10, 10)),
                            width=2 * random.random() ** 2)
                for a in l1.neurons for b in l2.neurons
            ))
            for l1, l2 in zip(layers, layers[1:])
        ))
        self.add(lines, layers)        # add lines first so neurons render on top
        self.layers, self.lines = layers, lines

    def forward_pass_anim(self, run_time=3):
        """A verb-as-method: light up layer by layer, left to right."""
        return LaggedStart(*(
            layer.pulse() for layer in self.layers
        ), lag_ratio=0.5, run_time=run_time)


# =============================================================================
# VERB — a show_*(scene, ...) choreography function. Recipe (SKILL.md Law 3):
#   • first arg is the scene; it calls scene.play / scene.wait internally
#   • owns its transient highlights via a last_rects / to_fade accumulator so
#     EXACTLY ONE highlight is ever on screen
#   • RETURNS the persistent mobjects it created
# Model: helpers.py:show_matrix_vector_product (97) + matrix_row_vector_product (132)
# =============================================================================

def show_weighted_sum(scene, input_layer, weights, output_neuron, run_time_per=0.5):
    """Walk a moving highlight across the inputs, accumulating into output_neuron.

    Shows the computation honestly and mechanically — never asserts a result.
    """
    running = 0.0
    last_rect = VGroup()                                    # the accumulator
    n = len(input_layer.neurons)
    for i, (dot, w) in enumerate(zip(input_layer.neurons, weights)):
        rect = SurroundingRectangle(dot, buff=0.04).set_stroke(YELLOW, 2)
        running += float(input_layer.activations[i] * w)
        scene.play(
            FadeOut(last_rect),                             # exactly one highlight
            ShowCreation(rect),
            output_neuron.animate.set_fill(WHITE, clip(running, 0, 1)),
            run_time=run_time_per, rate_func=linear,
        )
        last_rect = rect
    scene.play(FadeOut(last_rect))
    return output_neuron                                    # return what persists
