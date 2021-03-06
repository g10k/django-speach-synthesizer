# Create your views here.
import subprocess
import os
import uuid

from django.http import JsonResponse
from django.http import HttpResponse
from django.core.files import File
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from . import models
from . import serializers

@api_view(['post'])
def generate(request):
    """
    ---
    parameters:
    - name: text
      description: Text for generation
      required: true
      paramType: form
    """
    serializer = serializers.Generation(data=request.data)
    serializer.is_valid(raise_exception=True)
    text = serializer.validated_data['text']
    tmp_dir = '/tmp/voice/'
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

    file_uuid = str(uuid.uuid4())
    tmp_path = '%s/%s.wav' % (tmp_dir, file_uuid)

    command = 'echo %s | RHVoice-test -p elena -o %s' % (text, tmp_path)
    status_code, output = subprocess.getstatusoutput(command)
    if status_code != 0:
        return Response(
            {'error': 'File generation error', 'output': output},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    with open(tmp_path, 'rb') as tmp_file:
        models.SoundFile.objects.create(
            uuid=file_uuid,
            text=text,
            command=command,
            file=File(tmp_file),
            type='wav',
            user=request.user if not request.user.is_anonymous() else None
        )

    os.unlink(tmp_path)
    return JsonResponse({'status': status_code, 'uuid': file_uuid})


@api_view()
def get_file(request):
    """
    ---
    parameters:
    - name: uuid
      description: uuid of generated file
      required: true
      paramType: query
    """
    serializer = serializers.GetFile(data=request.query_params)
    serializer.is_valid(raise_exception=True)

    sound_file = models.SoundFile.objects.get(uuid=serializer.validated_data['uuid'])

    response = HttpResponse()
    response.write(sound_file.file.read())

    response['Content-Type'] = 'audio/vnd.wave'
    response['Content-Length'] = sound_file.file.size
    response['Content-Disposition'] = 'attachment; filename=%s' % sound_file.file.name.split('/')[-1]

    return response
