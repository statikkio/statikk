from __future__ import annotations

from unittest.mock import Mock

import pytest
from statikk.core.application.services.cloud_function_service import CloudFunctionService
from statikk.core.domain.entities.cloud_function import CloudFunction
from statikk.core.domain.repositories.cloud_function_repository import CloudFunctionRepository
from statikk.core.domain.value_objects.cloud_function_id import CloudFunctionID


@pytest.fixture
def mock_cloud_function_repository():
    return Mock(spec=CloudFunctionRepository)


@pytest.fixture
def cloud_function_service(mock_cloud_function_repository):
    return CloudFunctionService(mock_cloud_function_repository)


def test_create_cloud_function(cloud_function_service, mock_cloud_function_repository):
    # Act
    cloud_function = cloud_function_service.create_cloud_function(
        name='New Function',
        code='def handler(): pass',
        triggers=['http'],
    )

    # Assert
    assert cloud_function.name == 'New Function'
    assert cloud_function.code == 'def handler(): pass'
    assert cloud_function.triggers == ['http']
    mock_cloud_function_repository.save.assert_called_once_with(cloud_function)


def test_get_cloud_function(cloud_function_service, mock_cloud_function_repository):
    function_id = 'func-123'
    mock_cloud_function = CloudFunction(
        function_id=CloudFunctionID(function_id),
        name='Existing Function',
        code='def handler(): pass',
        triggers=['http'],
    )
    mock_cloud_function_repository.get_by_id.return_value = mock_cloud_function

    # Act
    cloud_function = cloud_function_service.get_cloud_function(function_id)

    # Assert
    assert cloud_function.name == 'Existing Function'
    mock_cloud_function_repository.get_by_id.assert_called_once_with(CloudFunctionID(function_id))


def test_update_cloud_function(cloud_function_service, mock_cloud_function_repository):
    function_id = 'func-123'
    new_code = 'def handler(): return "updated"'
    mock_cloud_function = CloudFunction(
        function_id=CloudFunctionID(function_id),
        name='Function',
        code='def handler(): pass',
        triggers=['http'],
    )
    mock_cloud_function_repository.get_by_id.return_value = mock_cloud_function

    # Act
    updated_function = cloud_function_service.update_cloud_function(
        function_id=function_id,
        new_code=new_code,
        triggers=['http'],
    )

    # Assert
    assert updated_function.code == new_code
    mock_cloud_function_repository.update.assert_called_once_with(updated_function)


def test_delete_cloud_function(cloud_function_service, mock_cloud_function_repository):
    function_id = 'func-123'
    mock_cloud_function_repository.get_by_id.return_value = CloudFunction(
        function_id=CloudFunctionID(function_id),
        name='Function to Delete',
        code='def handler(): pass',
        triggers=['http'],
    )

    # Act
    cloud_function_service.delete_cloud_function(function_id)

    # Assert
    mock_cloud_function_repository.delete.assert_called_once_with(CloudFunctionID(function_id))


def test_list_all_cloud_functions(cloud_function_service, mock_cloud_function_repository):
    mock_cloud_function_repository.list_all.return_value = [
        CloudFunction(
            function_id=CloudFunctionID('func-123'),
            name='Function One',
            code='def handler(): pass',
            triggers=['http'],
        ),
        CloudFunction(
            function_id=CloudFunctionID('func-456'),
            name='Function Two',
            code='def handler(): pass',
            triggers=['cron'],
        ),
    ]

    # Act
    cloud_functions = cloud_function_service.list_all_cloud_functions()

    # Assert
    assert len(cloud_functions) == 2
    assert cloud_functions[0].name == 'Function One'
    assert cloud_functions[1].name == 'Function Two'
    mock_cloud_function_repository.list_all.assert_called_once()
