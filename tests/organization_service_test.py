from __future__ import annotations

from unittest.mock import Mock
from unittest.mock import patch

import pytest
from statikk.core.application.services.organization_service import OrganizationService
from statikk.core.domain.entities.organization import Organization
from statikk.core.domain.entities.role import Role
from statikk.core.domain.repositories.organization_repository import OrganizationRepository
from statikk.core.domain.value_objects.organization_id import OrganizationID
from statikk.core.domain.value_objects.permissions import Permission
from statikk.core.domain.value_objects.role_id import RoleID
from statikk.core.domain.value_objects.user_id import UserID


@pytest.fixture
def mock_organization_repository():
    return Mock(spec=OrganizationRepository)


@pytest.fixture
def organization_service(mock_organization_repository):
    return OrganizationService(mock_organization_repository)


def test_create_organization(organization_service, mock_organization_repository):
    owner_id = 'user-123'
    org_name = 'Test Organization'

    # Act
    organization = organization_service.create_organization(name=org_name, owner_id=owner_id)

    # Assert
    assert organization.name == org_name
    assert str(organization.owner_id) == owner_id
    mock_organization_repository.save.assert_called_once_with(organization)


def test_get_organization(organization_service, mock_organization_repository):
    org_id = 'org-123'
    mock_organization = Organization(
        organization_id=OrganizationID(org_id),
        name='Existing Organization',
        owner_id=UserID('owner-123'),
    )
    mock_organization_repository.get_by_id.return_value = mock_organization

    # Act
    organization = organization_service.get_organization(org_id)

    # Assert
    assert organization.name == 'Existing Organization'
    assert str(organization.organization_id) == org_id
    mock_organization_repository.get_by_id.assert_called_once_with(OrganizationID(org_id))


@patch.object(OrganizationService, 'check_permission', return_value=True)
def test_update_organization(mock_check_permission, organization_service, mock_organization_repository):
    org_id = 'org-123'
    new_name = 'Updated Organization'
    mock_organization = Organization(
        organization_id=OrganizationID(org_id),
        name='Old Name',
        owner_id=UserID('owner-123'),
    )
    mock_organization_repository.get_by_id.return_value = mock_organization

    # Act
    updated_org = organization_service.update_organization(org_id, new_name, 'owner-123')

    # Assert
    assert updated_org.name == new_name
    mock_organization_repository.update.assert_called_once_with(updated_org)


@patch.object(OrganizationService, 'check_permission', return_value=True)
def test_delete_organization(mock_check_permission, organization_service, mock_organization_repository):
    org_id = 'org-123'
    mock_organization_repository.get_by_id.return_value = Organization(
        organization_id=OrganizationID(org_id),
        name='Organization to Delete',
        owner_id=UserID('owner-123'),
    )

    # Act
    organization_service.delete_organization(org_id, 'owner-123')

    # Assert
    mock_organization_repository.delete.assert_called_once_with(OrganizationID(org_id))


@patch.object(OrganizationService, 'check_permission', return_value=True)
def test_add_member(mock_check_permission, organization_service, mock_organization_repository):
    org_id = 'org-123'
    user_id = 'user-456'
    role = Role(RoleID(), 'member', [Permission('read'), Permission('write')])
    mock_organization = Organization(
        organization_id=OrganizationID(org_id),
        name='Org with Members',
        owner_id=UserID('owner-123'),
    )
    mock_organization_repository.get_by_id.return_value = mock_organization

    # Act
    updated_org = organization_service.add_member(org_id, user_id, role, 'owner-123')

    # Assert
    assert user_id in [str(uid) for uid in updated_org.members.keys()]
    print(updated_org.members)
    assert updated_org.members[user_id].name == 'member'
    mock_organization_repository.update.assert_called_once_with(mock_organization)


@patch.object(OrganizationService, 'check_permission', return_value=True)
def test_remove_member(mock_check_permission, organization_service, mock_organization_repository):
    org_id = 'org-123'
    user_id = 'user-456'
    mock_organization = Organization(
        organization_id=OrganizationID(org_id),
        name='Org with Members',
        owner_id=UserID('owner-123'),
        members={UserID(user_id).id: Role(RoleID(), 'member', [Permission('read')])},
    )
    mock_organization_repository.get_by_id.return_value = mock_organization

    # Act
    updated_org = organization_service.remove_member(org_id, user_id, 'owner-123')

    # Assert
    assert user_id not in [str(uid) for uid in updated_org.members.keys()]
    mock_organization_repository.update.assert_called_once_with(mock_organization)
