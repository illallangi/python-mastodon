"""
Swim is a DiffSyncModel that represents a swimming record in a Mastodon application.

Attributes:
    _modelname (str): The name of the model.
    _identifiers (tuple): The unique identifiers for the model.
    _attributes (tuple): The attributes of the model.
    pk (int): The primary key of the swimming record.
    url (str): The URL of the swimming record.
    date (str): The date of the swimming record.
    laps (float): The number of laps in the swimming record.
    distance (int): The distance covered in the swimming record.

Methods:
    create(cls, adapter, ids, attrs):
        Creates a new swimming record or updates an existing one based on the URL.
        Args:
            cls: The class itself.
            adapter: The adapter instance.
            ids (dict): The identifiers for the swimming record.
            attrs (dict): The attributes for the swimming record.
        Returns:
            item: The created or updated DiffSyncModel instance.

    update(self, attrs):
        Updates the attributes of the swimming record.
        Args:
            attrs (dict): The attributes to update.
        Returns:
            The updated DiffSyncModel instance.

    delete(self):
        Deletes the swimming record.
        Returns:
            The deleted DiffSyncModel instance.
"""

import diffsync


class Swim(diffsync.DiffSyncModel):
    """
    Swim is a DiffSyncModel that represents a swimming activity.

    Attributes:
        url (str): URL identifier for the swim record.
        date (str): Date of the swim.
        laps (float): Number of laps swum.
        distance (int): Distance swum in meters.
    Class Attributes:
        _modelname (str): Name of the model.
        _identifiers (tuple): Identifiers for the model.
        _attributes (tuple): Attributes of the model.
    Methods:
        create(cls, adapter, ids, attrs):
            Creates or updates a swim record in the database and returns the created item.
            Args:
                adapter: The adapter instance.
                ids (dict): Dictionary containing the identifiers.
                attrs (dict): Dictionary containing the attributes.
            Returns:
                Swim: The created or updated swim item.
        update(self, attrs):
            Updates the swim record in the database with the given attributes.
            Args:
                attrs (dict): Dictionary containing the attributes to update.
            Returns:
                Swim: The updated swim item.
        delete(self):
            Deletes the swim record from the database.
            Returns:
                Swim: The deleted swim item.
    """

    _modelname = "Swim"
    _identifiers = ("url",)
    _attributes = (
        "date",
        "laps",
        "distance",
    )

    url: str
    date: str
    laps: float
    distance: int

    @classmethod
    def create(
        cls,
        adapter: diffsync.Adapter,
        ids: dict,
        attrs: dict,
    ) -> "Swim":
        """
        Create a Swim instance.

        This method updates or creates a ModelSwim object using the provided ids and attrs,
        then creates a Swim instance with the updated or created ModelSwim object's
        primary key and the provided ids and attrs.
        Args:
            cls: The class that this method is called on.
            adapter: The adapter to use for creating the Swim instance.
            ids (dict): A dictionary containing the identifiers for the ModelSwim object.
            attrs (dict): A dictionary containing the attributes for the ModelSwim object.
        Returns:
            Swim: The created Swim instance.
        """
        raise NotImplementedError

    def update(
        self,
        attrs: dict,
    ) -> "Swim":
        """
        Update the current Swim instance with the provided attributes.

        Args:
            attrs (dict): A dictionary of attributes to update the instance with.
        Returns:
            Swim: The updated Swim instance.
        """
        raise NotImplementedError

    def delete(
        self,
    ) -> "Swim":
        """
        Delete the current Swim instance from the database.

        This method first deletes the associated ModelSwim object using its primary key (pk),
        and then calls the superclass's delete method to remove the Swim instance.
        Returns:
            Swim: The deleted Swim instance.
        """
        raise NotImplementedError
