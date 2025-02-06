from gmf.tools.logger import setup_logger

log = setup_logger()

class InputModule:

    runtime_input = True

    def __init__(self, tag=None, **options):
        
        if tag is None:
            raise ValueError(f"{self.__class__.__name__} requires a 'tag' to be set during instantiation.")
        
        self.set_tag(tag)
        self.options = options

    def set_tag(self, tag):
        """
        Sets the tag for the module. This can be overridden or extended if needed.
        """
        if not isinstance(tag, str) or not tag:
            raise ValueError("Tag must be a non-empty string.")
        self.tag = tag