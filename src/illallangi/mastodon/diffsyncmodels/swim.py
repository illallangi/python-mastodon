"""Swim is a DiffSyncModel that represents a swimming record in a Mastodon application."""

from datetime import date

import diffsync


class Swim(diffsync.DiffSyncModel):
    """
    Swim is a DiffSyncModel that represents a swimming activity.

    Attributes:
        url (str): URL identifier for the swim record.
        date (str): Date of the swim.
        distance (int): Distance swum in meters.
        laps (float): Number of laps swum.
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
        "distance",
        "laps",
    )

    url: str
    date: date
    distance: int
    laps: float

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
