import logging

import pandas as pd

logger = logging.getLogger(__name__)


def format_report(report, report_format):
    """
    Formats the report based on the requested format (csv, html, json).
    Handles missing records and discrepancies separately.
    """
    try:
        # Separate missing_in_target and missing_in_source into DataFrames
        missing_in_target = pd.DataFrame(report.get('missing_in_target', []))
        missing_in_source = pd.DataFrame(report.get('missing_in_source', []))

        # Discrepancies are handled separately as a dictionary
        discrepancies = report.get('discrepancies', {})

        if report_format == 'csv':
            # Handle CSV format
            result = ""
            if not missing_in_target.empty:
                result += "Missing in Target:\n" + missing_in_target.to_csv(index=False) + "\n"
            if not missing_in_source.empty:
                result += "Missing in Source:\n" + missing_in_source.to_csv(index=False) + "\n"
            if discrepancies:
                result += "Discrepancies:\n"
                for column, discrepancy_data in discrepancies.items():
                    result += f"\nDiscrepancies in column '{column}':\n"
                    discrepancy_df = pd.DataFrame(discrepancy_data)
                    result += discrepancy_df.to_csv(index=False) + "\n"
            return result

        elif report_format == 'html':
            # Handle HTML format
            result = ""
            if not missing_in_target.empty:
                result += "<h2>Missing in Target</h2>" + missing_in_target.to_html(index=False) + "<br>"
            if not missing_in_source.empty:
                result += "<h2>Missing in Source</h2>" + missing_in_source.to_html(index=False) + "<br>"
            if discrepancies:
                result += "<h2>Discrepancies</h2>"
                for column, discrepancy_data in discrepancies.items():
                    result += f"<h3>Discrepancies in column '{column}'</h3>"
                    discrepancy_df = pd.DataFrame(discrepancy_data)
                    result += discrepancy_df.to_html(index=False) + "<br>"
            return result

        else:
            # Default to returning the original report (JSON format)
            return report

    except Exception as e:
        logger.error(f"Unexpected error during report formatting: {e}")
        raise ValueError(f"Unexpected error while formatting the report: {e}")
