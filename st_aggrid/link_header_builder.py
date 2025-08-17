"""
Link Header Builder for st-aggrid

This module provides utilities to create column definitions with custom header components
that display a link icon and allow clicking to navigate to a URL.
"""

from typing import Dict, Any, Optional
from st_aggrid.shared import JsCode


class LinkHeaderBuilder:
    """
    Builder class for creating column definitions with link header components.
    """

    @staticmethod
    def create_link_column(
        field: str, header_name: str, url: str, **kwargs
    ) -> Dict[str, Any]:
        """
        Create a column definition with link functionality

        Args:
            field: Data field name
            header_name: Column header name
            url: URL to navigate to when clicking the link
            **kwargs: Other column configuration parameters

        Returns:
            Column definition dictionary containing custom headerComponent
        """
        # Ensure sorting and filtering features are enabled
        default_config = {
            "sortable": True,
            "filter": True,
            "resizable": True,
            "suppressHeaderContextMenu": False,  # Show column menu (including filter options)
        }

        # Merge default configuration with user-provided configuration
        column_config = {**default_config, **kwargs}

        column_def = {
            "field": field,
            "headerName": header_name,
            "headerComponentParams": {
                "innerHeaderComponent": "linkHeaderComponent",
                "url": url,
                "headerName": header_name,
            },
            **column_config,
        }

        return column_def

    @staticmethod
    def create_link_columns_from_dict(
        link_config: Dict[str, str], **default_kwargs
    ) -> Dict[str, Dict[str, Any]]:
        """
        Batch create link column definitions from dictionary configuration

        Args:
            link_config: Dictionary in format {field_name: url}
            **default_kwargs: Default column configuration parameters

        Returns:
            Dictionary of column definition dictionaries
        """
        columns = {}

        for field, url in link_config.items():
            # Use field name as default header_name
            header_name = field.replace("_", " ").title()

            columns[field] = LinkHeaderBuilder.create_link_column(
                field=field, header_name=header_name, url=url, **default_kwargs
            )

        return columns


def add_link_headers_to_grid_options(
    grid_options: Dict[str, Any], link_config: Dict[str, str], **default_kwargs
) -> Dict[str, Any]:
    """
    Add link column configuration to existing gridOptions

    Args:
        grid_options: Existing gridOptions configuration
        link_config: Dictionary in format {field_name: url}
        **default_kwargs: Default column configuration parameters

    Returns:
        Updated gridOptions
    """
    if "columnDefs" not in grid_options:
        grid_options["columnDefs"] = []

    # Create link column definitions
    link_columns = LinkHeaderBuilder.create_link_columns_from_dict(
        link_config, **default_kwargs
    )

    # Add link columns to columnDefs
    for field, column_def in link_columns.items():
        # Check if column definition for this field already exists
        existing_index = None
        for i, col in enumerate(grid_options["columnDefs"]):
            if col.get("field") == field:
                existing_index = i
                break

        if existing_index is not None:
            # Update existing column definition
            grid_options["columnDefs"][existing_index].update(column_def)
        else:
            # Add new column definition
            grid_options["columnDefs"].append(column_def)

    return grid_options


# Convenience functions
def create_link_column(
    field: str, header_name: str, url: str, **kwargs
) -> Dict[str, Any]:
    """Convenience function: Create a single link column definition"""
    return LinkHeaderBuilder.create_link_column(field, header_name, url, **kwargs)


def create_link_columns(
    link_config: Dict[str, str], **default_kwargs
) -> Dict[str, Dict[str, Any]]:
    """Convenience function: Batch create link column definitions"""
    return LinkHeaderBuilder.create_link_columns_from_dict(
        link_config, **default_kwargs
    )
