from dash import Input, Output, callback
import urllib.parse

@callback(
    Output("scan-uri-input", "value"),
    Input("scan-selector", "selectedLinks")
)
def update_selected_scan_uri(selected_links):
    print(f"DEBUG - Selected scan links: {selected_links}")  # Debug print
    
    if selected_links:
        # Extract the 'self' key from the dictionary
        if isinstance(selected_links, dict) and 'self' in selected_links:
            full_uri = selected_links['self']
            
            # Parse the URI to extract just the path
            parsed_uri = urllib.parse.urlparse(full_uri)
            path = parsed_uri.path
            
            # Remove the /api/v1/metadata prefix if present
            if path.startswith('/api/v1/metadata'):
                path = path[len('/api/v1/metadata'):]
            
            return path
        # Fall back to string representation if we can't extract 'self'
        return str(selected_links)
    return None

@callback(
    Output("mask-uri-input", "value"),
    Input("mask-selector", "selectedLinks")
)
def update_selected_mask_uri(selected_links):
    print(f"DEBUG - Selected mask links: {selected_links}")  # Debug print
    
    if selected_links:
        # Extract the 'self' key from the dictionary
        if isinstance(selected_links, dict) and 'self' in selected_links:
            full_uri = selected_links['self']
            
            # Parse the URI to extract just the path
            parsed_uri = urllib.parse.urlparse(full_uri)
            path = parsed_uri.path
            
            # Remove the /api/v1/metadata prefix if present
            if path.startswith('/api/v1/metadata'):
                path = path[len('/api/v1/metadata'):]
                
            return path
        # Fall back to string representation if we can't extract 'self'
        return str(selected_links)
    return None