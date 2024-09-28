import logging

from django.db import DatabaseError
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import UploadedFile
from .serializers import FileUploadSerializer
from .services import reconcile_files
from .utils import format_report

logger = logging.getLogger(__name__)

class ReconciliationViewSet(viewsets.ViewSet):
    """
    A ViewSet for uploading CSV files and generating reconciliation reports.
    """

    def create(self, request):
        """
        Handle file upload with enhanced error handling and logging.
        """
        serializer = FileUploadSerializer(data=request.data)
        print("-----t-tt--tt-", request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response({'message': 'Files uploaded successfully.'}, status=status.HTTP_201_CREATED)
            except DatabaseError as db_err:
                logger.error(f"Database error during file upload: {db_err}")
                return Response({'error': 'Database error occurred while saving the files.'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as e:
                logger.error(f"Unexpected error during file upload: {e}")
                return Response({'error': 'An unexpected error occurred during file upload.'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            logger.warning(f"Invalid file upload data: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='report')
    def generate_report(self, request):
        """
        Generates a reconciliation report based on the most recent uploaded CSV files.
        Handles query parameter errors and unexpected issues gracefully.
        """
        try:
            report_format = request.query_params.get('report_type', 'json').lower()
            if report_format not in ['json', 'csv', 'html']:
                logger.warning(f"Unsupported report type requested: {report_format}")
                return Response({'error': 'Unsupported report type requested, check the available report types.'},
                                status=status.HTTP_400_BAD_REQUEST)

            latest_upload = UploadedFile.objects.latest('uploaded_at')

            report = reconcile_files(latest_upload.source_file, latest_upload.target_file)

            formatted_report = format_report(report, report_format)

            content_type = (
                'text/html' if report_format == 'html' else
                'text/csv' if report_format == 'csv' else
                'application/json'
            )

            return Response(formatted_report, content_type=content_type, status=status.HTTP_200_OK)

        except UploadedFile.DoesNotExist:
            logger.error("No files found for reconciliation.")
            return Response({'error': 'No files found for reconciliation'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Unexpected error during report generation: {e}")
            return Response({'error': 'An unexpected error occurred during report generation'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
