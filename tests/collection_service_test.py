from __future__ import annotations

from unittest.mock import Mock

import pytest
from statikk.core.application.services.collection_service import CollectionService
from statikk.core.domain.entities.collection import Collection
from statikk.core.domain.repositories.collection_repository import CollectionRepository
from statikk.core.domain.value_objects.collection_id import CollectionID


@pytest.fixture
def mock_collection_repository():
    return Mock(spec=CollectionRepository)


@pytest.fixture
def collection_service(mock_collection_repository):
    return CollectionService(mock_collection_repository)


def test_create_collection(collection_service, mock_collection_repository):
    # Act
    collection = collection_service.create_collection(
        name='New Collection',
        schema={'field1': 'string', 'field2': 'integer'},
    )

    # Assert
    assert collection.name == 'New Collection'
    assert collection.schema == {'field1': 'string', 'field2': 'integer'}
    mock_collection_repository.save.assert_called_once_with(collection)


def test_get_collection(collection_service, mock_collection_repository):
    collection_id = 'col-123'
    mock_collection = Collection(
        collection_id=CollectionID(collection_id),
        name='Existing Collection',
        schema={'field1': 'string'},
    )
    mock_collection_repository.get_by_id.return_value = mock_collection

    # Act
    collection = collection_service.get_collection(collection_id)

    # Assert
    assert collection.name == 'Existing Collection'
    assert str(collection.collection_id) == collection_id
    mock_collection_repository.get_by_id.assert_called_once_with(CollectionID(collection_id))


def test_update_collection(collection_service, mock_collection_repository):
    collection_id = 'col-123'
    new_schema = {'field1': 'string', 'field2': 'integer'}
    mock_collection = Collection(
        collection_id=CollectionID(collection_id),
        name='Old Collection',
        schema={'field1': 'string'},
    )
    mock_collection_repository.get_by_id.return_value = mock_collection

    # Act
    updated_collection = collection_service.update_collection(
        collection_id=collection_id,
        name='Updated Collection',
        schema=new_schema,
    )

    # Assert
    assert updated_collection.name == 'Updated Collection'
    assert updated_collection.schema == new_schema
    mock_collection_repository.update.assert_called_once_with(updated_collection)


def test_delete_collection(collection_service, mock_collection_repository):
    collection_id = 'col-123'
    mock_collection_repository.get_by_id.return_value = Collection(
        collection_id=CollectionID(collection_id),
        name='Collection to Delete',
        schema={'field1': 'string'},
    )

    # Act
    collection_service.delete_collection(collection_id)

    # Assert
    mock_collection_repository.delete.assert_called_once_with(CollectionID(collection_id))


def test_list_all_collections(collection_service, mock_collection_repository):
    mock_collection_repository.list_all.return_value = [
        Collection(
            collection_id=CollectionID('col-123'),
            name='Collection One',
            schema={'field1': 'string'},
        ),
        Collection(
            collection_id=CollectionID('col-456'),
            name='Collection Two',
            schema={'field2': 'integer'},
        ),
    ]

    # Act
    collections = collection_service.list_all_collections()

    # Assert
    assert len(collections) == 2
    assert collections[0].name == 'Collection One'
    assert collections[1].name == 'Collection Two'
    mock_collection_repository.list_all.assert_called_once()
