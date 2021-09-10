from . import models
from django.shortcuts import render
import cv2


def uploadFile(request):
    if request.method == "POST":
        # Fetching the form data
        fileTitle = request.POST["fileTitle"]
        uploadedFile = request.FILES["uploadedFile"]

        # Saving the information in the database
        document = models.Document(
            title = fileTitle,
            uploadedFile = uploadedFile
        )

        document.save()
        change_file(str(document.uploadedFile).split('/')[1])


    documents = models.Document.objects.all()

    return render(request, "Core/upload-file.html", context = {
        "files": documents
    })

def change_file(uploadedFile):

    rgb_image = cv2.imread('./Core/Uploaded Files/'+uploadedFile)

    image_gray = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('./Core/change files/'+uploadedFile, image_gray)



