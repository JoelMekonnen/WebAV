from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
import os
from .forms import UploadFileForm
from .classifier_tools import ClassifierTools
from django.conf import settings
from django.core.files.storage import default_storage, FileSystemStorage
from .malware_model import avPredict

# Create your views here.
def index(request):
    return render(request, 'index.html')

# lets use a class based view
class WebAV(View):
    def loadAv(self, filename):
        fileLocation = os.path.join(settings.BASE_DIR, 'media\\antivirus\\')
        avInit = ClassifierTools(fileLocation, filename)
        avInit.hex_generator()
        imageName = avInit.image_generator()
        result = avPredict(imageName)
        return result

    def post(self, request):
        file = request.FILES['uploadedFile']
        fs = FileSystemStorage(location="media/antivirus/")
        file_name = fs.save(file.name, file)
        file_url = fs.url(file_name)   
        res = self.loadAv(file_name)
        return HttpResponse(res)




