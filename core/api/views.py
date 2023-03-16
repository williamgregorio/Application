#from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Note
from .serializers import NoteSerializer
import math
from datetime import datetime


#Get and post
class Notes(generics.GenericAPIView):
    serializer_class = NoteSerializer
    queryset = Note.objects.all()

    def get(self, request):
        page_number = int(request.GET.get("page",1))
        limit_number = int(request.GET.get("limit", 10))
        start_number = (page_number - 1) * limit_number
        end_number = limit_number * page_number
        search_param = request.GET.get("search")
        notes = Note.objects.all()
        total_notes = notes.count()
        if search_param:
            notes = notes.filter(title__icontains=search_param)
        serializer = self.serializer_class(notes[start_number:end_number], many=True)
        return Response({
            "status" : "success",
            'total': total_notes,
            "page": page_number,
            "last_page": math.ceil(total_notes / limit_number),
            "notes": serializer.data
        })

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "note":serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "fail", "message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)






class NoteDetails(generics.GenericAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def get_note(self,pk):
        try:
            return Note.objects.get(pk=pk)
        except:
            return None

    def get(self, request, pk):
        note = self.get_note(pk=pk)
        if note == None:
            return Response({"status": "fail", "message": f"Note Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(note)
        return Response({"status": "success", "note":serializer.data})

    def patch(self,request,pk):
        note = self.get_note(pk)
        if note == None:
            return Response({"status": "fail", "message": f"Note Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(
            note, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.validated_data['updatedAt'] = datetime.now()
            serializer.save()
            return Response({"status": "success", "note":serializer.data})
        return Response({"status": "fail", "message":serializer.errors}, status=status.HTTP_400_REQUEST)
    
    def delete(self, request, pk):
        note = self.get_note(pk)
        if note == None:
            return Response({"status": "fail", "message": f"Note Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)
        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)