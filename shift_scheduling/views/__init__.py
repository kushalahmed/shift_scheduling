
class BaseView(object):

    """basic view class."""

    def __init__(self, request):
        """Common init for views."""
        self.request = request