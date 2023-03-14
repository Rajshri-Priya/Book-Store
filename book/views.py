from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from book.models import Book
from book.serializers import BookSerializer
from logging_config.logger import get_logger

# logging config
logger = get_logger()


# Create your views here.
class BookAPI(APIView):
    serializer_class = BookSerializer

    @swagger_auto_schema(request_body=BookSerializer, operation_summary='POST Book Created')
    def post(self, request):
        try:
            request.data.update({'user': request.user.id})
            serializer = BookSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"Message": "Book created successfully", 'data': serializer.data, 'status': 201})
        except Exception as e:
            logger.error(e)
            return Response({"message": str(e)}, status=400)

    def get(self, request):
        try:
            books = Book.objects.all()
            serializer = BookSerializer(books, many=True)
            return Response({"Message": "All Books are", 'data': serializer.data, 'status': 200})
        except Exception as e:
            logger.error(e)
            return Response({"message": str(e)}, status=400)

    @swagger_auto_schema(request_body=BookSerializer, operation_summary='Book Updated')
    def put(self, request, pk):
        try:
            request.data.update({'user': request.user.id})
            book = Book.objects.get(id=pk)
            serializer = BookSerializer(book, request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"Message": "Book updated successfully", 'data': serializer.data, 'status': 200})
        except Exception as e:
            logger.error(e)
            return Response({"message": str(e)}, status=400)

    @swagger_auto_schema(request_body=BookSerializer, operation_summary='Book Deleted')
    def delete(self, request, pk):
        try:
            book = Book.objects.get(id=pk, user=request.user)
            book.delete()
            return Response({"Message": "Book deleted successfully", 'status': 200})
        except Exception as e:
            logger.error(e)
            return Response({"message": str(e)}, status=400)
