class Dataset():

    """Dataset abstract class
    """

    def __init__(self, name, data):
        """Initialize dataset from name and data it should hold

        Args:
            name (str): Dataset's name
            data (pd.DataFrame): data to store
        """

        self.name = name
        self.data = data

    def get(self, key):
        """get the value for key

        Args:
            key (str): what we're looking for

        Raises:
            NotImplementedError: [abstract method here]

        .. note:: This function accepts only :class:`str` parameters.
        .. warning:: Not implementing this in child classes
             will cause :exc:`NotImplementedError` exception!
        """

        raise NotImplementedError('Method get is not implemented')


class COSI1(Dataset):
    """Very smart COSI1 dataset class
    """

    def get(self, key):
        """returns one only value: [key] yes

        Args:
            key (str): what we're looking for

        Returns:
            str: Dummy string
        """
        if key:
            return '[{}] yes'.format(key)
        return ''
