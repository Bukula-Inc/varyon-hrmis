# REPORT UTILS
def build_report_column(column_title, column_name, column_type, columns=4, classname="", doctype="", is_figure=False):
    """
    GENERATING REPORT COLUMNS FOR THE DYNAMIC REPORT. FIELDS INCLUDING
        column_title
        column_name
        column_type
        columns
        width
        classname
        doctype
        is_figure
    """
    return {
        "column_title": column_title,
        "column_name": column_name,
        "column_type": column_type,
        "columns": columns,
        "width": columns,
        "classname": classname,
        "doctype":doctype,
        "is_figure":is_figure
    }