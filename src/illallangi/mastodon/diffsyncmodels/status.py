"""Status is a DiffSyncModel that represents a status record in a Mastodon application."""

from datetime import datetime

import diffsync


class Status(diffsync.DiffSyncModel):
    """
    Status is a DiffSyncModel that represents a status activity.

    Attributes:
        url (str): URL identifier for the status record.
        content (str): Content of the status.
        datetime (str): Date and Time of the status.
    Class Attributes:
        _modelname (str): Name of the model.
        _identifiers (tuple): Identifiers for the model.
        _attributes (tuple): Attributes of the model.
    Methods:
        create(cls, adapter, ids, attrs):
            Creates or updates a status record in the database and returns the created item.
            Args:
                adapter: The adapter instance.
                ids (dict): Dictionary containing the identifiers.
                attrs (dict): Dictionary containing the attributes.
            Returns:
                Status: The created or updated status item.
        update(self, attrs):
            Updates the status record in the database with the given attributes.
            Args:
                attrs (dict): Dictionary containing the attributes to update.
            Returns:
                Status: The updated status item.
        delete(self):
            Deletes the status record from the database.
            Returns:
                Status: The deleted status item.
    """

    _modelname = "Status"
    _identifiers = ("url",)
    _attributes = (
        "content",
        "datetime",
    )

    url: str
    content: str
    datetime: datetime

    @classmethod
    def create(
        cls,
        adapter: diffsync.Adapter,
        ids: dict,
        attrs: dict,
    ) -> "Status":
        """
        Create a Status instance.

        This method updates or creates a ModelStatus object using the provided ids and attrs,
        then creates a Status instance with the updated or created ModelStatus object's
        primary key and the provided ids and attrs.
        Args:
            cls: The class that this method is called on.
            adapter: The adapter to use for creating the Status instance.
            ids (dict): A dictionary containing the identifiers for the ModelStatus object.
            attrs (dict): A dictionary containing the attributes for the ModelStatus object.
        Returns:
            Status: The created Status instance.
        """
        raise NotImplementedError

    def update(
        self,
        attrs: dict,
    ) -> "Status":
        """
        Update the current Status instance with the provided attributes.

        Args:
            attrs (dict): A dictionary of attributes to update the instance with.
        Returns:
            Status: The updated Status instance.
        """
        raise NotImplementedError

    def delete(
        self,
    ) -> "Status":
        """
        Delete the current Status instance from the database.

        This method first deletes the associated ModelStatus object using its primary key (pk),
        and then calls the superclass's delete method to remove the Status instance.
        Returns:
            Status: The deleted Status instance.
        """
        raise NotImplementedError
