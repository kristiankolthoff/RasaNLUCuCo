import typing
from typing import Any, Optional, Text, Dict

import logging

from rasa.nlu.tokenizers import Token
from rasa.nlu.training_data import Message
from rasa.nlu.components import Component

from spellchecker import SpellChecker

if typing.TYPE_CHECKING:
    from rasa.nlu.model import Metadata


class SpellCheckerCorrection(Component):
    """A new component"""

    # Defines what attributes the pipeline component will
    # provide when called. The listed attributes
    # should be set by the component on the message object
    # during test and train, e.g.
    # ```message.set("entities", [...])```
    provides = ["tokens"]

    # Which attributes on a message are required by this
    # component. e.g. if requires contains "tokens", than a
    # previous component in the pipeline needs to have "tokens"
    # within the above described `provides` property.
    requires = ["tokens"]

    # Defines the default configuration parameters of a component
    # these values can be overwritten in the pipeline configuration
    # of the model. The component should choose sensible defaults
    # and should be able to create reasonable results with the defaults.
    defaults = {"language":"en",
                "distance":2,
                "word_freq_file":None}

    # Defines what language(s) this component can handle.
    # This attribute is designed for instance method: `can_handle_language`.
    # Default value is None which means it can handle all languages.
    # This is an important feature for backwards compatibility of components.
    language_list = ["en", "es", "de", "fr", "pt"]

    def __init__(self, component_config=None):
        super(SpellCheckerCorrection, self).__init__(component_config)
        # Set the language in order to use the default word 
        # frequency file for the set language
        self.language = self.component_config["language"]
        # Set the distance that should be used in the 
        # spellchecking algorithm
        self.distance = self.component_config["distance"]
        # Provides a custom word frequency file
        self.word_freq_file = self.component_config["word_freq_file"]
        logging.error("Language : {}, Distance : {}, File : {}".format(self.language, \
                    self.distance, self.word_freq_file))
        self.spellcheck = SpellChecker(language=self.language, distance=self.distance)
        # if custom word frequency file is provided use this
        # in the spellchecking algorithm to retrieve candidates
        if self.word_freq_file:
            self.spellcheck.word_frequency.load_text_file(self.word_freq_file)



    def process(self, message, **kwargs):
        """Process an incoming message.

        This is the components chance to process an incoming
        message. The component can rely on
        any context attribute to be present, that gets created
        by a call to :meth:`components.Component.pipeline_init`
        of ANY component and
        on any context attributes created by a call to
        :meth:`components.Component.process`
        of components previous to this one."""
        tokens = message.get("tokens")
        corrected_tokens = []
        act_corrected_tokens = []
        running_offset_adaption = 0
        for token in tokens:
            corr_token_text = self.spellcheck.correction(token.text)
            if len(corr_token_text) != len(token.text):
                act_corrected_tokens.append((token.text, corr_token_text))
            corrected_tokens.append(Token(corr_token_text, token.offset \
                    + running_offset_adaption))
            len_diff = len(corr_token_text) - len(token.text)
            running_offset_adaption += len_diff
        if act_corrected_tokens:
            logging.error("Corrected tokens : {}".format(act_corrected_tokens))
        else:
            logging.error("No spelling corrections took place")
        message.set("tokens", corrected_tokens)
        

    @classmethod
    def load(
        cls,
        meta: Dict[Text, Any],
        model_dir: Optional[Text] = None,
        model_metadata: Optional["Metadata"] = None,
        cached_component: Optional["Component"] = None,
        **kwargs: Any
    ) -> "Component":
        """Load this component from file."""

        if cached_component:
            return cached_component
        else:
            return cls(meta)