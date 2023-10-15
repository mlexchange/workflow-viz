def detect_mimetype(filepath, mimetype):
    if mimetype is None:
        # If we are here, detection based on file extension came up empty.
        ...
        mimetype = "text/csv"
    return mimetype
